// Character lab: the male paper doll assembled and driven by Phaser from the exported runtime sheets
// (docs/data/characters/male.json, written by tools/export-character-runtime.mjs).
// Movement is continuous (pixels per second, delta time, normalised diagonals); facing follows the four-direction rule;
// attacks follow combo.json (unarmed transitions, and the weapon combos keyed by the combo path); every layer, the
// weapon depth slots included, is its own sprite in the locked draw order. The player and the sparring partner are the
// same fighter: the player reads the keyboard, the partner reads scripted input (window.characterLab partner API).
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
  const DIRV = { S: [0, 1], E: [1, 0], N: [0, -1], W: [-1, 0] };
  const NO_KEYS = { isDown: false };

  // ---- fighter: one character (paper doll, state machine, combos, hits taken and dealt) ------------------------
  class Fighter {
    constructor(scene, opts) {
      const def = this.def = scene.def;
      this.scene = scene; this.name = opts.name;
      this.outfit = opts.outfit; this.hair = opts.hair; this.eyes = opts.eyes; this.mode = 0;
      this.facing = opts.facing; this.pos = { x: opts.x, y: opts.y };
      this.r = def.combo.bodyCollision.hurtRadius; this.h = 54;   // hurt footprint for the hit arc
      this.state = { kind: opts.guard ? 'guard' : 'idle', anim: opts.guard ? 'guard' : 'idle', frame: 0, t: 0 };
      this.guardTimer = opts.guard ? GUARD_TIMEOUT : 0; this.alwaysGuard = !!opts.guard;
      this.buffered = null; this.target = null; this.lastHit = null; this.flash = 0; this.autoFace = !!opts.autoFace;
      this.pressQueue = []; this.move = { x: 0, y: 0, sprint: false };   // scripted input (the keyboard player reads keys)
      // stamina (combo.json stamina): weaves spend it; at 0 the fighter is exhausted until it is full again
      this.stamina = def.combo.stamina.values.max; this.exhausted = false; this.sinceSpend = Infinity;
      // health and poise (combo.json health, poise): hits deal both; a blocked hit less health and more poise
      this.health = def.combo.health.values.max; this.poise = def.combo.poise.values.max; this.sincePoise = Infinity;
      // paper doll: one sprite per slot, in draw order, inside a container placed at the pivot
      this.doll = scene.add.container(this.pos.x, this.pos.y);
      this.layers = {};
      const shadow = scene.add.sprite(0, 0, 'shadow', 0).setOrigin(0.5, 63 / 64);
      this.doll.add(shadow); this.layers.shadow = shadow;
      // weapon sprites: 128x128 frames whose pivot [64, 95] is the body frame's pivot [32, 63]
      this.wsprites = {};
      const wsprite = (hand, depth) => {
        const spr = scene.add.sprite(0, 0, `idle|body`, 0).setOrigin(64 / 128, 95 / 128).setVisible(false);
        this.doll.add(spr); (this.wsprites[hand] ??= {})[depth] = spr;
      };
      for (const depth of ['behind', 'trailBehind']) for (const h of HANDS) wsprite(h, depth);
      for (const { slot } of def.slots) {
        if (slot === 'arms') for (const h of HANDS) wsprite(h, 'front');
        const spr = scene.add.sprite(0, 0, `idle|body`, 0).setOrigin(0.5, 63 / 64);
        this.doll.add(spr); this.layers[slot] = spr;
      }
      for (const depth of ['top', 'trail']) for (const h of HANDS) wsprite(h, depth);
      // the impact burst (impact-fx, in states that carry it) over every character layer
      this.layers.fx = scene.add.sprite(0, 0, `idle|body`, 0).setOrigin(0.5, 63 / 64).setVisible(false);
      this.doll.add(this.layers.fx);
      this.applyLayers();
    }

    destroy() { this.doll.destroy(); }
    others() { return this.scene.fighters.filter((f) => f !== this); }
    // hit targets: the training posts and the other fighters
    targets() { return [...this.scene.posts, ...this.others()]; }

    // frame index in a state's sheet for the current facing row
    frameIndex(anim, col) {
      const s = this.def.states[anim], row = s.rows.indexOf(this.facing);
      return row * s.frames + col;
    }

    applyLayers() {
      const { anim, frame } = this.state, def = this.def, outfit = def.outfits[this.outfit], st = def.states[anim];
      const pick = { body: 'body', arms: 'arms', clothing: outfit.clothing, armAccessories: outfit.armAccessories, hair: HAIRS[this.hair], eyes: EYES[this.eyes] };
      const idx = this.frameIndex(anim, frame);
      for (const { slot } of def.slots) {
        const spr = this.layers[slot], layer = pick[slot];
        if (!layer) { spr.setVisible(false); continue; }
        spr.setVisible(true).setTexture(`${anim}|${layer}`, idx);
        if (this.flash > 0) spr.setTintFill(0xffffff); else spr.clearTint();
      }
      if (st.layers['impact-fx']) this.layers.fx.setVisible(true).setTexture(`${anim}|impact-fx`, idx); else this.layers.fx.setVisible(false);
      this.layers.shadow.setFrame(def.referenceFrameOrder.indexOf(this.facing));
      // weapons: the mode's item per hand, from the state's weapon sheets (none in unarmed states)
      const mode = MODES[this.mode], W = st.weapons;
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

    // face a point along the dominant axis
    facePoint(t) {
      const dx = t.x - this.pos.x, dy = t.y - this.pos.y;
      if (dx === 0 && dy === 0) return;
      this.facing = Math.abs(dx) >= Math.abs(dy) ? (dx > 0 ? 'E' : 'W') : (dy > 0 ? 'S' : 'N');
    }

    clipDef(key) { const [state, clip] = key.split('/'); return { state, clip, ...this.def.states[state].clips[clip] }; }

    // an attack press with a selected target turns the character to face it (dominant axis)
    faceTarget() { const t = this.target?.pos || this.target; if (t) this.facePoint(t); }

    // startAt: a clip entered from another clip's hold may start later (its entry rule, e.g. at the smear frame)
    startClip(key, path = '', startAt = null, input = null) {
      const c = this.clipDef(key), i = startAt !== null && c.frames.includes(startAt) ? c.frames.indexOf(startAt) : 0;
      if (c.state !== 'weave') this.faceTarget();
      this.state = { kind: c.state === 'weave' ? 'evade' : 'attack', anim: c.state, clipKey: key, clip: c, i, frame: c.frames[i], t: 0, path, input };
      // attacks spend the attacker's stamina (combo.json stamina.values light/heavyAttackCost)
      if (c.state !== 'weave') { const V = this.def.combo.stamina.values; this.spend(input === 'light' ? V.lightAttackCost : V.heavyAttackCost); }
      this.buffered = null;
      this.applyRootMotion();
      this.checkHit();
    }

    events(anim) { return (this.def.states[anim].events || {}).E || []; }

    activeFrame(c) {
      const a = this.events(c.state).find((e) => e.clip === c.clip && e.type === 'active');
      return a ? a.frame : c.frames[0];
    }

    applyRootMotion() {
      const s = this.state, rm = this.def.states[s.anim].rootMotion[this.facing];
      if (!rm) return [0, 0];
      const [dx, dy] = rm[s.frame] || [0, 0], x0 = this.pos.x, y0 = this.pos.y;
      this.moveBy(dx, dy);
      return [this.pos.x - x0, this.pos.y - y0];
    }

    // body collision (combo.json bodyCollision): a foot point moving to (x, y) is refused when it would lie inside the
    // doubled ellipse around another fighter and closer to it than before (two overlapping bodies may only separate)
    actorBlocked(x, y, b) {
      const C = this.def.combo.bodyCollision, q = (px, py) => ((px - b.x) / (2 * C.rx)) ** 2 + ((py - b.y) / (2 * C.ry)) ** 2;
      const n = q(x, y);
      return n < 1 && n < q(this.pos.x, this.pos.y);
    }

    blocked(x, y) {
      return this.scene.solids.some((b) => x > b.x && x < b.x + b.w && y > b.y && y < b.y + b.h)
        || this.others().some((f) => this.actorBlocked(x, y, f.pos));
    }

    // move the foot point, sliding along solids and other bodies axis by axis
    moveBy(dx, dy) {
      const x = Phaser.Math.Clamp(this.pos.x + dx, 16, VIEW_W - 16), y = Phaser.Math.Clamp(this.pos.y + dy, 40, VIEW_H - 4);
      if (!this.blocked(x, this.pos.y)) this.pos.x = x;
      if (!this.blocked(this.pos.x, y)) this.pos.y = y;
    }

    activeEvent() {
      const s = this.state;
      if (s.kind !== 'attack') return null;
      return this.events(s.anim).find((x) => x.frame === s.frame && x.hitbox) || null;
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
      const a = this.def.combo.hitArea, [fx, fy] = DIRV[this.facing], P = p.pos || p;
      const dx = P.x - this.pos.x, dy = P.y - this.pos.y, d = Math.hypot(dx, dy);
      if (d - p.r > a.radius) return null;
      if (d > p.r) {
        const ang = Math.acos(Phaser.Math.Clamp((dx * fx + dy * fy) / d, -1, 1)), tol = Math.asin(Math.min(1, p.r / d));
        if (ang - tol > a.halfAngleDeg * Math.PI / 180) return null;
      }
      return Math.max(0, d - p.r);
    }

    label(p) { return p instanceof Fighter ? p.name : `post ${p.id}`; }

    checkHit() {
      const e = this.activeEvent();
      if (!e) return;
      const [, y, , h] = e.hitbox, band = [63 - (y + h), 63 - y];
      const inside = this.targets().map((p) => ({ p, d: this.inArc(p) }))
        .filter(({ p, d }) => d !== null && band[0] < p.h && band[1] > 0);
      if (!inside.length) { this.lastHit = `${e.move} → miss`; return; }
      const pick = inside.find(({ p }) => p === this.target) || inside.sort((a, b) => a.d - b.d)[0];
      const tgt = this.label(pick.p) + (pick.p === this.target ? ' (target)' : '');
      if (pick.p instanceof Fighter) {
        const res = pick.p.takeHit(this, this.state.input === 'light' ? 'light' : 'heavy');
        this.lastHit = `${e.move} → ${tgt}${res === 'evaded' ? ' evaded (weave)' : res === 'blocked' ? ' blocked' : res === 'guardBreak' ? ' guard broken' : ''}`;
      } else { pick.p.flash = 0.25; this.lastHit = `${e.move} → ${tgt}`; }
    }

    // a hit lands on this fighter: during the weave's evade frames it misses; otherwise the hit recoil (hitReact, when
    // exported for this facing) starts from its first frame, interrupting whatever was playing, and the attacker
    // follows the knockback (combo.json hitFollow); without hitReact a one-frame flash
    takeHit(attacker, weight = 'light') {
      const s = this.state, C = this.def.combo, Bk = C.block.values;
      if (s.kind === 'evade' && this.events(s.anim).some((e) => e.frame === s.frame && e.type === 'evade')) return 'evaded';
      const hp = weight === 'light' ? C.health.values.lightDamage : C.health.values.heavyDamage;
      const pd = weight === 'light' ? C.poise.values.lightDamage : C.poise.values.heavyDamage;
      // block (combo.json block): a hit from the front half lands on the block: stamina is spent, less health and
      // more poise damage, a small push back; at 0 poise the guard breaks (the hit recoil stands in for the stagger)
      if (s.kind === 'block') {
        const [fx, fy] = DIRV[this.facing], dx = attacker.pos.x - this.pos.x, dy = attacker.pos.y - this.pos.y, d = Math.hypot(dx, dy) || 1;
        if ((dx * fx + dy * fy) / d >= Math.cos(Bk.frontHalfAngleDeg * Math.PI / 180) - 1e-9) {
          this.spend(Bk.staminaPerBlockedHit);
          this.damage(hp * Bk.healthDamageScale, pd * Bk.poiseDamageScale);
          if (this.poise > 0 && !this.exhausted) { this.moveBy(-fx * Bk.blockedKnockback, -fy * Bk.blockedKnockback); return 'blocked'; }
          this.poise = this.def.combo.poise.values.max;
          this.recoil(attacker);
          return 'guardBreak';
        }
      }
      this.damage(hp, pd);
      if (this.poise <= 0) this.poise = this.def.combo.poise.values.max;
      return this.recoil(attacker);
    }

    damage(hp, pd) {
      this.health = Math.max(0, this.health - hp);
      this.poise = Math.max(0, this.poise - pd); this.sincePoise = 0;
    }

    recoil(attacker) {
      this.facePoint(attacker.pos);
      const hr = this.def.states.hitReact;
      if (!hr || !hr.rows.includes(this.facing)) { this.flash = 0.08; return 'hit'; }
      const c = this.clipDef('hitReact/hitReact');
      this.state = { kind: 'hit', anim: 'hitReact', clipKey: 'hitReact/hitReact', clip: c, i: 0, frame: c.frames[0], t: 0, path: '', by: attacker };
      this.buffered = null; this.guardTimer = GUARD_TIMEOUT;
      this.knock();
      return 'hit';
    }

    // hit recoil root motion; the attacker follows it so a chain keeps its distance
    knock() {
      const [dx, dy] = this.applyRootMotion(), a = this.state.by;
      if (a && (dx || dy) && this.def.combo.hitFollow && (a.state.kind === 'attack' || a.state.kind === 'guard')) a.moveBy(dx, dy);
    }

    // in the hit recoil only its recover frames take input (they cancel it); hitstun frames take none
    canAct() {
      const s = this.state;
      if (s.kind !== 'hit') return true;
      return this.events(s.anim).some((e) => e.frame === s.frame && e.type === 'recover');
    }
    // the rest pose: the exhausted stance while exhausted (unarmed only: a weapon mode keeps its stance so the weapon
    // never disappears), otherwise the guard or weapon stance
    restAnim() { return this.exhausted && !MODES[this.mode].items && this.def.states.exhausted ? 'exhausted' : (MODES[this.mode].stance || 'guard'); }
    toRest() { this.state = { kind: 'guard', anim: this.restAnim(), frame: 0, t: 0 }; }

    spend(cost) {
      const S = this.def.combo.stamina.values;
      this.stamina = Math.max(0, this.stamina - cost); this.sinceSpend = 0;
      if (this.stamina === 0) this.exhausted = true;
    }

    tickStamina(dt) {
      const S = this.def.combo.stamina.values;
      this.sinceSpend += dt;
      if (this.sinceSpend >= S.regenDelaySeconds) this.stamina = Math.min(S.max, this.stamina + S.regenPerSecond * dt);
      if (this.exhausted && this.stamina >= S.recoverAt) this.exhausted = false;
      const P = this.def.combo.poise.values;
      this.sincePoise += dt;
      if (this.sincePoise >= P.regenDelaySeconds) this.poise = Math.min(P.max, this.poise + P.regenPerSecond * dt);
    }

    // the block is held from rest (not while moving, attacking or in hit recoil); unarmed only (no weapon block sheets
    // yet), and not while exhausted or without stamina
    canBlock() {
      return !this.exhausted && this.stamina > 0 && !MODES[this.mode].items && !!this.def.states.block;
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
      // exhausted fighters cannot dodge; a weave needs stamina above 0 and spends its cost
      if (MODES[this.mode].items || !this.canAct() || this.exhausted || this.stamina <= 0) return;
      if (this.state.kind === 'hit' || this.state.kind === 'block') this.toRest();
      const s = this.state;
      if (s.kind === 'attack' || s.kind === 'evade') {
        if (this.press('weave')) this.spend(this.def.combo.stamina.values.weaveCost);
        return;
      }
      this.spend(this.def.combo.stamina.values.weaveCost);
      const c = this.clipDef('weave/weave');
      this.state = { kind: 'evade', solo: true, anim: c.state, clipKey: 'weave/weave', clip: c, i: 0, frame: c.frames[0], t: 0, path: '' };
      this.buffered = null;
      this.applyRootMotion();
    }

    press(input) {
      if (!this.canAct() || this.state.kind === 'block') return;
      if (this.state.kind === 'hit') this.toRest();
      const s = this.state, tr = this.def.combo.transitions, wc = this.weaponCombo();
      if (s.kind === 'evade' && s.solo) return;
      if (s.kind !== 'attack' && s.kind !== 'evade' && wc) {
        const key = (wc.paths[''] || {})[input];
        if (key) this.startClip(key, input === 'light' ? 'L' : 'H', null, input);
        return;
      }
      if (s.kind !== 'attack' && s.kind !== 'evade') {
        const from = s.kind === 'guard' ? (tr.guard || tr.neutral) : tr.neutral;
        if (from[input]) this.startClip(from[input], '', null, input);
        return;
      }
      // presses from the clip's active frame on are buffered and taken at its chain window
      if (s.frame >= this.activeFrame(s.clip)) { this.buffered = input; return !!this.nextClip(s, input).key; }
      return false;
    }

    // one update: input (actions queued since the last frame, and the movement vector), then the state machine
    step(dt, input) {
      for (const action of this.pressQueue.splice(0)) {
        if (action === 'light' || action === 'heavy') this.press(action);
        else if (action === 'weave') this.weave();
        else if (action === 'hair') this.hair = (this.hair + 1) % HAIRS.length;
        else if (action === 'eyes') this.eyes = (this.eyes + 1) % EYES.length;
        else if (action === 'weapon') {
          // a mode change waits for rest (an attack in progress finishes with its own weapon)
          const k = this.state.kind;
          if (k === 'attack' || k === 'evade' || k === 'hit') continue;
          this.mode = (this.mode + 1) % MODES.length;
          if (k === 'guard') this.toRest();
        }
        else if (action.startsWith('outfit')) this.outfit = OUTFIT_KEYS[Number(action.slice(6))];
      }
      this.flash = Math.max(0, this.flash - dt);
      this.tickStamina(dt);

      const s = this.state;
      if (s.kind === 'attack' || s.kind === 'evade' || s.kind === 'hit') {
        s.t += dt;
        // exhausted attacks play slowed (combo.json stamina.values.exhaustedAttackSpeed)
        const slow = s.kind === 'attack' && this.exhausted ? this.def.combo.stamina.values.exhaustedAttackSpeed : 1;
        const step = 1 / (s.clip.fps * slow);
        while (s.t >= step && this.state === s) {
          s.t -= step;
          const win = s.clip.chainWindow, next = this.buffered && win && s.frame >= win[0] && s.frame <= win[1]
            ? this.nextClip(s, this.buffered) : null;
          if (next && next.key) { this.startClip(next.key, next.path, next.startAt, this.buffered); break; }
          if (this.buffered && win && s.frame >= win[0] && s.frame <= win[1]) this.buffered = null;   // invalid press: dropped
          s.i += 1;
          if (s.i >= s.clip.frames.length) { this.toRest(); this.guardTimer = GUARD_TIMEOUT; break; }
          s.frame = s.clip.frames[s.i];
          if (s.kind === 'hit') this.knock();
          else { this.applyRootMotion(); this.checkHit(); }
        }
      } else if (s.kind === 'block' || input.block && this.canBlock()) {
        // holding the block: the block stance loops in place; releasing it (or losing the stamina) returns to rest
        if (s.kind !== 'block') this.state = { kind: 'block', anim: 'block', frame: 0, t: 0 };
        else if (!input.block || !this.canBlock()) { this.toRest(); this.guardTimer = GUARD_TIMEOUT; }
        const st = this.state, sd = this.def.states[st.anim];
        st.t += dt;
        while (st.t >= 1 / sd.fps) { st.t -= 1 / sd.fps; st.frame = (st.frame + 1) % sd.frames; }
      } else {
        const { vx, vy, sprint } = input;
        const moving = vx !== 0 || vy !== 0;
        if (moving) {
          const len = Math.hypot(vx, vy), anim = sprint && !this.exhausted ? 'sprint' : 'walk', sp = this.scene.speed[anim];
          this.faceFrom(vx, vy);
          this.moveBy(vx / len * sp * dt, vy / len * sp * dt);
          if (s.anim !== anim) { this.state = { kind: anim, anim, frame: 0, t: 0 }; }
        } else {
          if (!this.alwaysGuard) this.guardTimer = Math.max(0, this.guardTimer - dt);
          const tired = this.restAnim() === 'exhausted';
          const rest = tired || this.guardTimer > 0 ? this.restAnim() : 'idle';
          if (s.anim !== rest) this.state = { kind: rest === 'idle' ? 'idle' : 'guard', anim: rest, frame: 0, t: 0 };
          // the sparring partner keeps facing the player while it stands
          if (this.autoFace) { const o = this.others()[0]; if (o) this.facePoint(o.pos); }
        }
        const st = this.state, sd = this.def.states[st.anim];
        st.t += dt;
        while (st.t >= 1 / sd.fps) { st.t -= 1 / sd.fps; st.frame = (st.frame + 1) % sd.frames; }
      }
      this.applyLayers();
    }
  }

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
      // authored collision (independent of the posts' drawing): ground-plane boxes a foot point cannot enter
      this.solids = this.posts.map((p) => ({ x: p.x - 11, y: p.y - 4, w: 22, h: 7 }));

      // walk and sprint speeds come from the sheets' root motion so the planted foot stays planted
      this.speed = {};
      for (const anim of ['walk', 'sprint']) {
        const s = def.states[anim], rm = s.rootMotion.E;
        this.speed[anim] = rm.reduce((a, [dx]) => a + Math.abs(dx), 0) / s.frames * s.fps;
      }
      this.fighters = [];
      this.player = new Fighter(this, { name: 'player', outfit: 'gi', hair: 0, eyes: 0, facing: 'S', x: 120, y: 110 });
      this.fighters.push(this.player);
      this.partner = null;
      this.hitG = this.add.graphics().setDepth(10000);
      this.showHits = false;
      this.posts.forEach((p) => this.drawPost(p));

      const kb = this.input.keyboard;
      this.keys = kb.addKeys('W,A,S,D,UP,DOWN,LEFT,RIGHT,SHIFT,I');
      // discrete actions are queued from key events so a tap shorter than one frame is never lost
      this.pressQueue = [];
      const onKey = { J: 'light', K: 'heavy', L: 'weave', P: 'partner', H: 'hitboxes', T: 'target', Q: 'weapon', ONE: 'outfit0', TWO: 'outfit1', THREE: 'outfit2', FOUR: 'outfit3', FIVE: 'hair', SIX: 'eyes' };
      for (const [key, action] of Object.entries(onKey)) kb.on(`keydown-${key}`, (e) => { if (!e.repeat) this.pressQueue.push(action); });
      this.statusEl = document.getElementById('state');
    }

    // the player's state, kept on the scene for tools and tests that read it
    get pos() { return this.player?.pos; }
    get state() { return this.player.state; } set state(v) { this.player.state = v; }
    get facing() { return this.player.facing; } set facing(v) { this.player.facing = v; }
    get mode() { return this.player.mode; } set mode(v) { this.player.mode = v; }
    get guardTimer() { return this.player.guardTimer; } set guardTimer(v) { this.player.guardTimer = v; }
    get lastHit() { return this.player?.lastHit; }
    get target() { return this.player.target; }
    clipDef(key) { return this.player.clipDef(key); }
    applyLayers() { this.player.applyLayers(); }

    drawPost(p) {
      const g = p.g, hit = p.flash > 0;
      g.clear();
      if (this.player.target === p) g.lineStyle(1, 0xf0d080, 1).strokeEllipse(p.x, p.y, 22, 7);
      g.fillStyle(0x1c1b18, 0.55).fillEllipse(p.x, p.y, 16, 4);
      g.fillStyle(hit ? 0xd9a441 : 0x7a5a3a, 1).fillRect(p.x - p.w / 2, p.y - p.h, p.w, p.h);
      g.fillStyle(hit ? 0xf0d080 : 0x8f6c47, 1).fillRect(p.x - p.w / 2, p.y - p.h, 3, p.h);
      g.lineStyle(1, 0x000000, 1).strokeRect(p.x - p.w / 2 + 0.5, p.y - p.h + 0.5, p.w - 1, p.h - 1);
      g.setDepth(p.y);
    }

    // T cycles the player's selected target through the targets and back to none
    cycleTarget() {
      const pl = this.player, t = pl.targets(), i = pl.target ? t.indexOf(pl.target) + 1 : 0;
      pl.target = i < t.length ? t[i] : null;
    }

    // P: the sparring partner (red armour, purple eyes), the same fighter as the player on scripted input; it spawns
    // in front of the player at the body-collision distance, stays in its guard and faces the player while it stands
    togglePartner() {
      if (this.partner) {
        if (this.player.target === this.partner) this.player.target = null;
        this.partner.destroy(); this.fighters = this.fighters.filter((f) => f !== this.partner); this.partner = null; return;
      }
      const C = this.def.combo.bodyCollision, pl = this.player, [fx, fy] = DIRV[pl.facing];
      const x = Phaser.Math.Clamp(pl.pos.x + fx * 2 * C.rx, 16, VIEW_W - 16), y = Phaser.Math.Clamp(pl.pos.y + fy * 2 * C.ry, 40, VIEW_H - 4);
      this.partner = new Fighter(this, { name: 'partner', outfit: 'redArmor', hair: 0, eyes: 1, facing: pl.facing, x, y, guard: true, autoFace: true });
      this.partner.facePoint(pl.pos); this.partner.applyLayers();
      this.fighters.push(this.partner);
    }

    update(time, deltaMs) {
      const dt = Math.min(deltaMs / 1000, 0.05), k = this.keys, pl = this.player;
      for (const action of this.pressQueue.splice(0)) {
        if (action === 'partner') this.togglePartner();
        else if (action === 'hitboxes') this.showHits = !this.showHits;
        else if (action === 'target') this.cycleTarget();
        else pl.pressQueue.push(action);
      }
      const vx = (k.D.isDown || k.RIGHT.isDown ? 1 : 0) - (k.A.isDown || k.LEFT.isDown ? 1 : 0);
      const vy = (k.S.isDown || k.DOWN.isDown ? 1 : 0) - (k.W.isDown || k.UP.isDown ? 1 : 0);
      pl.step(dt, { vx, vy, sprint: k.SHIFT.isDown, block: k.I.isDown });
      if (this.partner) { const m = this.partner.move; this.partner.step(dt, { vx: m.x, vy: m.y, sprint: m.sprint, block: !!m.block }); }
      for (const p of this.posts) { p.flash = Math.max(0, p.flash - dt); this.drawPost(p); }

      this.hitG.clear();
      // lab HUD (not world art): health, poise and stamina bars above each fighter (stamina red while exhausted)
      for (const f of this.fighters) {
        const C = this.def.combo, x = Math.round(f.pos.x) - 10, y = Math.round(f.pos.y) - 66;
        this.hitG.fillStyle(0x1c1b18, 0.8).fillRect(x - 1, y - 1, 22, 10);
        const bars = [[f.health / C.health.values.max, 0xd05a4a], [f.poise / C.poise.values.max, 0xe0c048], [f.stamina / C.stamina.values.max, f.exhausted ? 0xc04030 : 0x8fd06a]];
        bars.forEach(([v, col], i) => this.hitG.fillStyle(col, 1).fillRect(x, y + i * 3, Math.round(20 * v), 2));
      }
      if (this.showHits) {
        const a = this.def.combo.hitArea, R = Phaser.Math.DegToRad;
        for (const b of this.solids) this.hitG.lineStyle(1, 0x40c0ff, 1).strokeRect(b.x + 0.5, b.y + 0.5, b.w - 1, b.h - 1);
        for (const f of this.fighters) {
          const hb = f.hitbox(), face = { S: 90, E: 0, N: 270, W: 180 }[f.facing], C = this.def.combo.bodyCollision;
          const live = !!f.activeEvent(), px = Math.round(f.pos.x), py = Math.round(f.pos.y);
          this.hitG.fillStyle(0xffd040, live ? 0.45 : 0.12).slice(px, py, a.radius, R(face - a.halfAngleDeg), R(face + a.halfAngleDeg)).fillPath();
          this.hitG.lineStyle(1, 0x40c0ff, 0.8).strokeEllipse(px, py, 2 * C.rx, 2 * C.ry);
          this.hitG.lineStyle(1, 0xff4040, 1).strokeRect(px - 32 + 0.5, py - 63 + 0.5, 63, 63);
          if (hb) this.hitG.lineStyle(1, 0xffd040, 0.8).strokeRect(hb.x + 0.5, hb.y + 0.5, hb.w - 1, hb.h - 1);
        }
      }
      this.renderStatus();
    }

    renderStatus() {
      const pl = this.player, s = pl.state, pt = this.partner, rows = [
        ['state', s.kind === 'attack' ? `${s.clipKey} (frame ${s.frame})` : s.anim],
        ['facing', pl.facing],
        ['weapon', MODES[pl.mode].label],
        ['combo path', s.kind === 'attack' && s.path ? s.path.split('').join(' ') : '—'],
        ['outfit', pl.outfit],
        ['buffered', pl.buffered || '—'],
        ['guard timer', pl.guardTimer.toFixed(1) + ' s'],
        ['health / poise', `${Math.round(pl.health)} / ${Math.round(pl.poise)}`],
        ['stamina', `${Math.round(pl.stamina)}${pl.exhausted ? ' (exhausted)' : ''}`],
        ['target', pl.target ? pl.label(pl.target) : 'none'],
        ['last hit', pl.lastHit || '—'],
        ['partner', pt ? `${pt.state.anim} (frame ${pt.state.frame}), health ${Math.round(pt.health)}, poise ${Math.round(pt.poise)}, stamina ${Math.round(pt.stamina)}${pt.lastHit ? ', last hit ' + pt.lastHit : ''}` : '—']
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
