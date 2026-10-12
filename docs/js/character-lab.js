// Character lab: the male paper doll assembled and driven by Phaser from the exported runtime sheets
// (docs/data/characters/male.json, written by tools/export-character-runtime.mjs).
// Movement is continuous (pixels per second, delta time, normalised diagonals); facing follows the four-direction rule;
// attacks follow combo.json; every layer is its own sprite in the locked draw order.
(() => {
  'use strict';
  const VIEW_W = 320, VIEW_H = 180, ZOOM = 3;
  const GUARD_TIMEOUT = 3;            // seconds in the guard with no attack before the idle returns (placeholder)
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

      // training post as a hit target (y-sorted with the player)
      this.post = { x: 220, y: 110, w: 10, h: 54 };   // head height, so every hit band can land
      // authored collision (independent of the post's drawing): a ground-plane box the player's foot point cannot enter
      this.solids = [{ x: this.post.x - 11, y: this.post.y - 4, w: 22, h: 7 }];
      this.postG = this.add.graphics();
      this.drawPost(false);

      // paper doll: one sprite per slot, in draw order, inside a container placed at the pivot
      this.doll = this.add.container(120, 110);
      this.layers = {};
      const shadow = this.add.sprite(0, 0, 'shadow', 0).setOrigin(0.5, 63 / 64);
      this.doll.add(shadow); this.layers.shadow = shadow;
      for (const { slot } of def.slots) {
        const spr = this.add.sprite(0, 0, `idle|body`, 0).setOrigin(0.5, 63 / 64);
        this.doll.add(spr); this.layers[slot] = spr;
      }
      this.hitG = this.add.graphics().setDepth(10000);

      this.outfit = 'gi'; this.hair = 0; this.eyes = 0; this.showHits = false;
      this.facing = 'S';
      this.pos = { x: 120, y: 110 };
      this.state = { kind: 'idle', anim: 'idle', frame: 0, t: 0 };
      this.guardTimer = 0;
      this.buffered = null;

      const kb = this.input.keyboard;
      this.keys = kb.addKeys('W,A,S,D,UP,DOWN,LEFT,RIGHT,SHIFT');
      // discrete actions are queued from key events so a tap shorter than one frame is never lost
      this.pressQueue = [];
      const onKey = { J: 'light', K: 'heavy', H: 'hitboxes', ONE: 'outfit0', TWO: 'outfit1', THREE: 'outfit2', FOUR: 'outfit3', FIVE: 'hair', SIX: 'eyes' };
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

    drawPost(hit) {
      const p = this.post, g = this.postG;
      g.clear();
      g.fillStyle(0x1c1b18, 0.55).fillEllipse(p.x, p.y, 16, 4);
      g.fillStyle(hit ? 0xd9a441 : 0x7a5a3a, 1).fillRect(p.x - p.w / 2, p.y - p.h, p.w, p.h);
      g.fillStyle(hit ? 0xf0d080 : 0x8f6c47, 1).fillRect(p.x - p.w / 2, p.y - p.h, 3, p.h);
      g.lineStyle(1, 0x000000, 1).strokeRect(p.x - p.w / 2 + 0.5, p.y - p.h + 0.5, p.w - 1, p.h - 1);
      g.setDepth(p.y);
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
      this.doll.setPosition(Math.round(this.pos.x), Math.round(this.pos.y)).setDepth(this.pos.y);
    }

    // four-direction facing: any horizontal component faces E or W, pure vertical faces N or S, no input keeps it
    faceFrom(vx, vy) {
      if (vx > 0) this.facing = 'E'; else if (vx < 0) this.facing = 'W';
      else if (vy > 0) this.facing = 'S'; else if (vy < 0) this.facing = 'N';
    }

    clipDef(key) { const [state, clip] = key.split('/'); return { state, clip, ...this.def.states[state].clips[clip] }; }

    startClip(key) {
      const c = this.clipDef(key);
      this.state = { kind: 'attack', anim: c.state, clipKey: key, clip: c, i: 0, frame: c.frames[0], t: 0 };
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

    checkHit() {
      const hb = this.hitbox(), p = this.post;
      // screen-space overlap; side-on (E/W) hits also need the target on roughly the same ground line
      // front/back (S/N) hits need the target on the facing side
      const f = this.facing, sameLine = f === 'S' ? p.y >= this.pos.y : f === 'N' ? p.y <= this.pos.y : Math.abs(this.pos.y - p.y) <= 8;
      const hit = hb && sameLine && hb.x < p.x + p.w / 2 && hb.x + hb.w > p.x - p.w / 2 && hb.y < p.y && hb.y + hb.h > p.y - p.h;
      this.drawPost(!!hit);
      if (hit) this.lastHit = hb.move;
    }

    press(input) {
      const s = this.state, tr = this.def.combo.transitions;
      if (s.kind !== 'attack') {
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
        else if (action === 'hitboxes') this.showHits = !this.showHits;
        else if (action === 'hair') this.hair = (this.hair + 1) % HAIRS.length;
        else if (action === 'eyes') this.eyes = (this.eyes + 1) % EYES.length;
        else this.outfit = OUTFIT_KEYS[Number(action.slice(6))];
      }

      const s = this.state;
      if (s.kind === 'attack') {
        s.t += dt;
        const step = 1 / s.clip.fps;
        while (s.t >= step && this.state === s) {
          s.t -= step;
          const win = s.clip.chainWindow, next = this.buffered && win && s.frame >= win[0] && s.frame <= win[1]
            ? (this.def.combo.transitions[s.clipKey] || {})[this.buffered] : null;
          if (next) { this.startClip(next); break; }
          if (this.buffered && win && s.frame >= win[0] && s.frame <= win[1]) this.buffered = null;   // invalid press: dropped
          s.i += 1;
          if (s.i >= s.clip.frames.length) {
            this.state = { kind: 'guard', anim: 'guard', frame: 0, t: 0 };
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
          const rest = this.guardTimer > 0 ? 'guard' : 'idle';
          if (s.anim !== rest) this.state = { kind: rest, anim: rest, frame: 0, t: 0 };
        }
        const st = this.state, sd = this.def.states[st.anim];
        st.t += dt;
        while (st.t >= 1 / sd.fps) { st.t -= 1 / sd.fps; st.frame = (st.frame + 1) % sd.frames; }
        this.drawPost(false);
      }

      this.applyLayers();
      this.hitG.clear();
      if (this.showHits) {
        const hb = this.hitbox();
        for (const b of this.solids) this.hitG.lineStyle(1, 0x40c0ff, 1).strokeRect(b.x + 0.5, b.y + 0.5, b.w - 1, b.h - 1);
        this.hitG.lineStyle(1, 0xff4040, 1).strokeRect(Math.round(this.pos.x) - 32 + 0.5, Math.round(this.pos.y) - 63 + 0.5, 63, 63);
        if (hb) this.hitG.fillStyle(0xffd040, 0.45).fillRect(hb.x, hb.y, hb.w, hb.h);
      }
      this.renderStatus();
    }

    renderStatus() {
      const s = this.state, rows = [
        ['state', s.kind === 'attack' ? `${s.clipKey} (frame ${s.frame})` : s.anim],
        ['facing', this.facing],
        ['outfit', this.outfit],
        ['buffered', this.buffered || '—'],
        ['guard timer', this.guardTimer.toFixed(1) + ' s'],
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
