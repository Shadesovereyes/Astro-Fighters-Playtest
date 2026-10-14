// Character lab: the male paper doll assembled and driven by Phaser from the exported runtime sheets
// (docs/data/characters/male.json, written by tools/export-character-runtime.mjs).
// Movement is continuous (pixels per second, delta time, normalised diagonals); facing follows the four-direction rule;
// attacks follow combo.json (unarmed transitions, and the weapon combos keyed by the combo path); every layer, the
// weapon depth slots included, is its own sprite in the locked draw order.
(() => {
  'use strict';
  const VIEW_W = 320, VIEW_H = 180, ZOOM = 3;
  const GUARD_TIMEOUT = 15;           // seconds in the guard (or weapon stance) with no attack before the idle returns (user 2026-10-13)
  // weapon modes (Q cycles): the stance replaces the guard after an attack; the weapon shows in its stance and attacks
  // only (idle, walk and sprint are unarmed: draw and sheathe are not authored yet)
  const MODES = [
    { key: 'unarmed', label: 'unarmed' },
    { key: 'katana', label: 'katana', combo: 'twoHanded', stance: 'twoHandGuard', items: { main: 'katana' } },
    { key: 'wakizashi', label: 'wakizashi (one hand)', combo: 'oneHanded', stance: 'oneHandGuard', items: { main: 'wakizashi' } },
    { key: 'tanto', label: 'tanto (one hand)', combo: 'oneHanded', stance: 'oneHandGuard', items: { main: 'tanto' } },
    { key: 'dual', label: 'dual tanto', combo: 'dualWield', stance: 'oneHandDualGuard', items: { main: 'tanto', off: 'tanto' } }
  ];
  // weapon depth slots and where each sits in the doll: behind/trailBehind under the body, front over the clothing and
  // under the arms (the fists close over the hilt), top and trail over every character layer
  const WDEPTHS = ['behind', 'trailBehind', 'front', 'top', 'trail'], HANDS = ['main', 'off'];
  const HAIRS = ['fade-hair', 'long-hair', 'afro-hair'], EYES = ['brown-eyes', 'purple-eyes'];
  const OUTFIT_KEYS = ['base', 'gi', 'blueArmor', 'redArmor'];

  class Lab extends Phaser.Scene {
    constructor() { super('lab'); }

    preload() {
      this.load.json('def', 'data/characters/male.json');
      this.load.once('filecomplete-json-def', () => {
        const def = this.cache.json.get('def');
        for (const [state, s] of Object.entries(def.states)) {
          for (const [layer, file] of Object.entries(s.layers)) this.load.spritesheet(`${state}|${layer}`, file, { frameWidth: 64, frameHeight: 64 });
          const W = s.weapons;
          if (W) for (const it of W.items) for (const [depth, file] of Object.entries(it.layers)) {
            this.load.spritesheet(`${state}|w|${it.slot}|${it.item}|${depth}`, file, { frameWidth: W.frameSize[0], frameHeight: W.frameSize[1] });
          }
        }
        this.load.spritesheet('shadow', def.contactShadow, { frameWidth: 64, frameHeight: 64 });
      });
    }

    create() {
      const def = this.def = this.cache.json.get('def');
      this.cameras.main.setBackgroundColor('#3b3a33');
      // plain lab floor (not world art): a flat ground with faint stone joints so movement is readable
      const g = this.add.graphics();
      g.fillStyle(0x4a4840, 1).fillRect(0, 0, VIEW_W, VIEW_H);
      g.lineStyle(1, 0x413f38, 1);
      for (let x = 0; x < VIEW_W; x += 40) g.lineBetween(x + 0.5, 0, x + 0.5, VIEW_H);
      for (let y = 0; y < VIEW_H; y += 24) g.lineBetween(0, y + 0.5, VIEW_W, y + 0.5);
      g.setDepth(-10000);

      // training posts as hit targets (y-sorted with the player); footprint radius r and body height h in ground pixels
      this.posts = [[220, 110], [236, 132], [200, 78]].map(([x, y], i) => ({ id: i + 1, x, y, r: 4, w: 10, h: 54, flash: 0, g: this.add.graphics() }));
      // authored collision (independent of the posts' drawing): ground-plane boxes the player's foot point cannot enter
      this.solids = this.posts.map((p) => ({ x: p.x - 11, y: p.y - 4, w: 22, h: 7 }));
      this.target = null;
      this.posts.forEach((p) => this.drawPost(p));

      // paper doll: one sprite per slot, in draw order, inside a container placed at the pivot
      this.doll = this.add.container(120, 110);
      this.layers = {};
      const shadow = this.add.sprite(0, 0, 'shadow', 0).setOrigin(0.5, 63 / 64);
      this.doll.add(shadow); this.layers.shadow = shadow;
      // weapon sprites: 128x128 frames whose pivot [64, 95] is the body frame's pivot [32, 63]
      this.wsprites = {};
      const wsprite = (hand, depth) => {
        const spr = this.add.sprite(0, 0, `idle|body`, 0).setOrigin(64 / 128, 95 / 128).setVisible(false);
        this.doll.add(spr); (this.wsprites[hand] ??= {})[depth] = spr;
      };
      for (const depth of ['behind', 'trailBehind']) for (const h of HANDS) wsprite(h, depth);
      for (const { slot } of def.slots) {
        if (slot === 'arms') for (const h of HANDS) wsprite(h, 'front');
        const spr = this.add.sprite(0, 0, `idle|body`, 0).setOrigin(0.5, 63 / 64);
        this.doll.add(spr); this.layers[slot] = spr;
      }
      for (const depth of ['top', 'trail']) for (const h of HANDS) wsprite(h, depth);
      this.hitG = this.add.graphics().setDepth(10000);

      this.outfit = 'gi'; this.hair = 0; this.eyes = 0; this.showHits = false; this.mode = 0;
      this.facing = 'S';
      this.pos = { x: 120, y: 110 };
      this.state = { kind: 'idle', anim: 'idle', frame: 0, t: 0 };
      this.guardTimer = 0;
      this.buffered = null;

      const kb = this.input.keyboard;
      this.keys = kb.addKeys('W,A,S,D,UP,DOWN,LEFT,RIGHT,SHIFT');
      // discrete actions are queued from key events so a tap shorter than one frame is never lost
      this.pressQueue = [];
      const onKey = { J: 'light', K: 'heavy', L: 'weave', H: 'hitboxes', T: 'target', Q: 'weapon', ONE: 'outfit0', TWO: 'outfit1', THREE: 'outfit2', FOUR: 'outfit3', FIVE: 'hair', SIX: 'eyes' };
      for (const [key, action] of Object.entries(onKey)) kb.on(`keydown-${key}`, (e) => { if (!e.repeat) this.pressQueue.push(action); });
      // walk and sprint speeds come from the sheets' root motion so the planted foot stays planted
      this.speed = {};
      for (const anim of ['walk', 'sprint']) {
        const s = def.states[anim], rm = s.rootMotion.E;
        this.speed[anim] = rm.reduce((a, [dx]) => a + Math.abs(dx), 0) / s.frames * s.fps;
      }
      this.statusEl = document.getElementById('state');
      this.applyLayers();
    }

    drawPost(p) {
      const g = p.g, hit = p.flash > 0;
      g.clear();
      if (this.target === p) g.lineStyle(1, 0xf0d080, 1).strokeEllipse(p.x, p.y, 22, 7);
      g.fillStyle(0x1c1b18, 0.55).fillEllipse(p.x, p.y, 16, 4);
      g.fillStyle(hit ? 0xd9a441 : 0x7a5a3a, 1).fillRect(p.x - p.w / 2, p.y - p.h, p.w, p.h);
      g.fillStyle(hit ? 0xf0d080 : 0x8f6c47, 1).fillRect(p.x - p.w / 2, p.y - p.h, 3, p.h);
      g.lineStyle(1, 0x000000, 1).strokeRect(p.x - p.w / 2 + 0.5, p.y - p.h + 0.5, p.w - 1, p.h - 1);
      g.setDepth(p.y);
    }

    // T cycles the selected target through the posts and back to none
    cycleTarget() {
      const i = this.target ? this.posts.indexOf(this.target) + 1 : 0;
      this.target = i < this.posts.length ? this.posts[i] : null;
    }

    // frame index in a state's sheet for the current facing row
    frameIndex(anim, col) {
      const s = this.def.states[anim], row = s.rows.indexOf(this.facing);
      return row * s.frames + col;
    }

    applyLayers() {
      const { anim, frame } = this.state, def = this.def, outfit = def.outfits[this.outfit];
      const pick = { body: 'body', arms: 'arms', clothing: outfit.clothing, armAccessories: outfit.armAccessories, hair: HAIRS[this.hair], eyes: EYES[this.eyes] };
      const idx = this.frameIndex(anim, frame);
      for (const { slot } of def.slots) {
        const spr = this.layers[slot], layer = pick[slot];
        if (!layer) { spr.setVisible(false); continue; }
        spr.setVisible(true).setTexture(`${anim}|${layer}`, idx);
      }
      this.layers.shadow.setFrame(def.referenceFrameOrder.indexOf(this.facing));
      // weapons: the mode's item per hand, from the state's weapon sheets (none in unarmed states)
      const mode = MODES[this.mode], W = def.states[anim].weapons;
      for (const h of HANDS) {
        const it = mode.items?.[h] && W ? W.items.find((x) => x.slot === h && x.item === mode.items[h]) : null;
        for (const depth of WDEPTHS) {
          const spr = this.wsprites[h][depth];
          if (it && it.layers[depth]) spr.setVisible(true).setTexture(`${anim}|w|${h}|${it.item}|${depth}`, idx);
          else spr.setVisible(false);
        }
      }
      this.doll.setPosition(Math.round(this.pos.x), Math.round(this.pos.y)).setDepth(this.pos.y);
    }

    // four-direction facing: any horizontal component faces E or W, pure vertical faces N or S, no input keeps it
    faceFrom(vx, vy) {
      if (vx > 0) this.facing = 'E'; else if (vx < 0) this.facing = 'W';
      else if (vy > 0) this.facing = 'S'; else if (vy < 0) this.facing = 'N';
    }

    clipDef(key) { const [state, clip] = key.split('/'); return { state, clip, ...this.def.states[state].clips[clip] }; }

    // an attack press with a selected target turns the character to face it (dominant axis)
    faceTarget() {
      const t = this.target;
      if (!t) return;
      const dx = t.x - this.pos.x, dy = t.y - this.pos.y;
      if (dx === 0 && dy === 0) return;
      this.facing = Math.abs(dx) >= Math.abs(dy) ? (dx > 0 ? 'E' : 'W') : (dy > 0 ? 'S' : 'N');
    }

    // startAt: a clip entered from another clip's hold may start later (its entry rule, e.g. at the smear frame)
    startClip(key, path = '', startAt = null) {
      const c = this.clipDef(key), i = startAt !== null && c.frames.includes(startAt) ? c.frames.indexOf(startAt) : 0;
      if (c.state !== 'weave') this.faceTarget();
      this.state = { kind: c.state === 'weave' ? 'evade' : 'attack', anim: c.state, clipKey: key, clip: c, i, frame: c.frames[i], t: 0, path };
      this.buffered = null;
      this.applyRootMotion();
      this.checkHit();
    }

    activeFrame(c) {
      const ev = (this.def.states[c.state].events || {}).E || [];
      const a = ev.find((e) => e.clip === c.clip && e.type === 'active');
      return a ? a.frame : c.frames[0];
    }

    applyRootMotion() {
      const s = this.state, rm = this.def.states[s.anim].rootMotion[this.facing];
      if (!rm) return;
      const [dx, dy] = rm[s.frame] || [0, 0];
      this.moveBy(dx, dy);
    }

    blocked(x, y) { return this.solids.some((b) => x > b.x && x < b.x + b.w && y > b.y && y < b.y + b.h); }

    // move the foot point, sliding along solids axis by axis
    moveBy(dx, dy) {
      const x = Phaser.Math.Clamp(this.pos.x + dx, 16, VIEW_W - 16), y = Phaser.Math.Clamp(this.pos.y + dy, 40, VIEW_H - 4);
      if (!this.blocked(x, this.pos.y)) this.pos.x = x;
      if (!this.blocked(this.pos.x, y)) this.pos.y = y;
    }

    activeEvent() {
      const s = this.state;
      if (s.kind !== 'attack') return null;
      return ((this.def.states[s.anim].events || {}).E || []).find((x) => x.frame === s.frame && x.hitbox) || null;
    }

    // on-screen debug box (the hit test itself is the ground arc)
    hitbox() {
      const s = this.state;
      if (s.kind !== 'attack') return null;
      const ev = this.def.states[s.anim].events || {};
      let list = ev[this.facing], mirror = false;
      if (!list && this.facing === 'W') { list = ev.E; mirror = true; }
      const e = (list || []).find((x) => x.frame === s.frame && x.hitbox);
      if (!e) return null;
      let [x, y, w, h] = e.hitbox;
      if (mirror) x = 64 - x - w;
      return { x: Math.round(this.pos.x) - 32 + x, y: Math.round(this.pos.y) - 63 + y, w, h, move: e.move };
    }

    // hit test (combo.json hitArea + targeting): an arc on the ground plane in front of the facing, radius 25,
    // plus the move's height band from its E hitbox; one target per active frame: the selected target if inside,
    // otherwise the closest target inside
    inArc(p) {
      const a = this.def.combo.hitArea, [fx, fy] = { S: [0, 1], E: [1, 0], N: [0, -1], W: [-1, 0] }[this.facing];
      const dx = p.x - this.pos.x, dy = p.y - this.pos.y, d = Math.hypot(dx, dy);
      if (d - p.r > a.radius) return null;
      if (d > p.r) {
        const ang = Math.acos(Phaser.Math.Clamp((dx * fx + dy * fy) / d, -1, 1)), tol = Math.asin(Math.min(1, p.r / d));
        if (ang - tol > a.halfAngleDeg * Math.PI / 180) return null;
      }
      return Math.max(0, d - p.r);
    }

    checkHit() {
      const e = this.activeEvent();
      if (!e) return;
      const [, y, , h] = e.hitbox, band = [63 - (y + h), 63 - y];
      const inside = this.posts.map((p) => ({ p, d: this.inArc(p) }))
        .filter(({ p, d }) => d !== null && band[0] < p.h && band[1] > 0);
      if (!inside.length) { this.lastHit = `${e.move} → miss`; return; }
      const pick = inside.find(({ p }) => p === this.target) || inside.sort((a, b) => a.d - b.d)[0];
      pick.p.flash = 0.25;
      this.lastHit = `${e.move} → post ${pick.p.id}${pick.p === this.target ? ' (target)' : ''}`;
    }

    // weapon combos: transitions keyed by the combo path (presses so far, L light / H heavy)
    weaponCombo() { const m = MODES[this.mode]; return m.combo ? this.def.combo.weapons[m.combo] : null; }

    nextClip(s, input) {
      const wc = this.weaponCombo();
      if (!wc) return { key: (this.def.combo.transitions[s.clipKey] || {})[input] || null };
      const key = (wc.paths[s.path] || {})[input] || null;
      if (!key) return { key: null };
      const entry = this.clipDef(key).entry?.[s.clip.clip];
      return { key, path: s.path + (input === 'light' ? 'L' : 'H'), startAt: entry && entry.atFrames.includes(s.frame) ? entry.start : null };
    }

    // the unarmed weave/dodge (weave state), unarmed only (the weave has no weapon sheets yet). During a clip the press
    // goes through the combo table (jab -> weave -> heavy = spin roundhouse). From rest it is a solo weave in the current
    // facing: its root motion carries the body back, it ends in the guard and presses during it do nothing.
    weave() {
      if (MODES[this.mode].items) return;
      const s = this.state;
      if (s.kind === 'attack' || s.kind === 'evade') { this.press('weave'); return; }
      const c = this.clipDef('weave/weave');
      this.state = { kind: 'evade', solo: true, anim: c.state, clipKey: 'weave/weave', clip: c, i: 0, frame: c.frames[0], t: 0, path: '' };
      this.buffered = null;
      this.applyRootMotion();
    }

    press(input) {
      const s = this.state, tr = this.def.combo.transitions, wc = this.weaponCombo();
      if (s.kind === 'evade' && s.solo) return;
      if (s.kind !== 'attack' && s.kind !== 'evade' && wc) {
        const key = (wc.paths[''] || {})[input];
        if (key) this.startClip(key, input === 'light' ? 'L' : 'H');
        return;
      }
      if (s.kind !== 'attack' && s.kind !== 'evade') {
        const from = s.kind === 'guard' ? (tr.guard || tr.neutral) : tr.neutral;
        if (from[input]) this.startClip(from[input]);
        return;
      }
      // presses from the clip's active frame on are buffered and taken at its chain window
      if (s.frame >= this.activeFrame(s.clip)) this.buffered = input;
    }

    update(time, deltaMs) {
      const dt = Math.min(deltaMs / 1000, 0.05), k = this.keys;
      for (const action of this.pressQueue.splice(0)) {
        if (action === 'light' || action === 'heavy') this.press(action);
        else if (action === 'weave') this.weave();
        else if (action === 'hitboxes') this.showHits = !this.showHits;
        else if (action === 'target') this.cycleTarget();
        else if (action === 'hair') this.hair = (this.hair + 1) % HAIRS.length;
        else if (action === 'eyes') this.eyes = (this.eyes + 1) % EYES.length;
        else if (action === 'weapon') {
          // a mode change waits for rest (an attack in progress finishes with its own weapon)
          if (this.state.kind === 'attack' || this.state.kind === 'evade') continue;
          this.mode = (this.mode + 1) % MODES.length;
          if (this.state.kind === 'guard') { const st = MODES[this.mode].stance || 'guard'; this.state = { kind: 'guard', anim: st, frame: 0, t: 0 }; }
        }
        else this.outfit = OUTFIT_KEYS[Number(action.slice(6))];
      }

      const s = this.state;
      if (s.kind === 'attack' || s.kind === 'evade') {
        s.t += dt;
        const step = 1 / s.clip.fps;
        while (s.t >= step && this.state === s) {
          s.t -= step;
          const win = s.clip.chainWindow, next = this.buffered && win && s.frame >= win[0] && s.frame <= win[1]
            ? this.nextClip(s, this.buffered) : null;
          if (next && next.key) { this.startClip(next.key, next.path, next.startAt); break; }
          if (this.buffered && win && s.frame >= win[0] && s.frame <= win[1]) this.buffered = null;   // invalid press: dropped
          s.i += 1;
          if (s.i >= s.clip.frames.length) {
            const stance = MODES[this.mode].stance || 'guard';
            this.state = { kind: 'guard', anim: stance, frame: 0, t: 0 };
            this.guardTimer = GUARD_TIMEOUT;
            break;
          }
          s.frame = s.clip.frames[s.i];
          this.applyRootMotion();
          this.checkHit();
        }
      } else {
        let vx = (k.D.isDown || k.RIGHT.isDown ? 1 : 0) - (k.A.isDown || k.LEFT.isDown ? 1 : 0);
        let vy = (k.S.isDown || k.DOWN.isDown ? 1 : 0) - (k.W.isDown || k.UP.isDown ? 1 : 0);
        const moving = vx !== 0 || vy !== 0;
        if (moving) {
          const len = Math.hypot(vx, vy), anim = k.SHIFT.isDown ? 'sprint' : 'walk', sp = this.speed[anim];
          this.faceFrom(vx, vy);
          this.moveBy(vx / len * sp * dt, vy / len * sp * dt);
          if (s.anim !== anim) { this.state = { kind: anim, anim, frame: 0, t: 0 }; }
        } else {
          this.guardTimer = Math.max(0, this.guardTimer - dt);
          const rest = this.guardTimer > 0 ? (MODES[this.mode].stance || 'guard') : 'idle';
          if (s.anim !== rest) this.state = { kind: this.guardTimer > 0 ? 'guard' : 'idle', anim: rest, frame: 0, t: 0 };
        }
        const st = this.state, sd = this.def.states[st.anim];
        st.t += dt;
        while (st.t >= 1 / sd.fps) { st.t -= 1 / sd.fps; st.frame = (st.frame + 1) % sd.frames; }
      }
      for (const p of this.posts) { p.flash = Math.max(0, p.flash - dt); this.drawPost(p); }

      this.applyLayers();
      this.hitG.clear();
      if (this.showHits) {
        const hb = this.hitbox();
        const a = this.def.combo.hitArea, face = { S: 90, E: 0, N: 270, W: 180 }[this.facing], R = Phaser.Math.DegToRad;
        const live = !!this.activeEvent(), px = Math.round(this.pos.x), py = Math.round(this.pos.y);
        this.hitG.fillStyle(0xffd040, live ? 0.45 : 0.12).slice(px, py, a.radius, R(face - a.halfAngleDeg), R(face + a.halfAngleDeg)).fillPath();
        for (const b of this.solids) this.hitG.lineStyle(1, 0x40c0ff, 1).strokeRect(b.x + 0.5, b.y + 0.5, b.w - 1, b.h - 1);
        this.hitG.lineStyle(1, 0xff4040, 1).strokeRect(Math.round(this.pos.x) - 32 + 0.5, Math.round(this.pos.y) - 63 + 0.5, 63, 63);
        if (hb) this.hitG.lineStyle(1, 0xffd040, 0.8).strokeRect(hb.x + 0.5, hb.y + 0.5, hb.w - 1, hb.h - 1);
      }
      this.renderStatus();
    }

    renderStatus() {
      const s = this.state, rows = [
        ['state', s.kind === 'attack' ? `${s.clipKey} (frame ${s.frame})` : s.anim],
        ['facing', this.facing],
        ['weapon', MODES[this.mode].label],
        ['combo path', s.kind === 'attack' && s.path ? s.path.split('').join(' ') : '—'],
        ['outfit', this.outfit],
        ['buffered', this.buffered || '—'],
        ['guard timer', this.guardTimer.toFixed(1) + ' s'],
        ['target', this.target ? `post ${this.target.id}` : 'none'],
        ['last hit', this.lastHit || '—']
      ];
      const html = rows.map(([a, b]) => `<tr><td>${a}</td><td>${b}</td></tr>`).join('');
      if (html !== this.lastStatus) { this.statusEl.innerHTML = html; this.lastStatus = html; }
    }
  }

  window.characterLab = new Phaser.Game({
    type: Phaser.AUTO,
    parent: 'game',
    width: VIEW_W, height: VIEW_H, zoom: ZOOM,
    pixelArt: true, antialias: false, roundPixels: true,
    backgroundColor: '#3b3a33',
    scene: [Lab]
  });
})();
