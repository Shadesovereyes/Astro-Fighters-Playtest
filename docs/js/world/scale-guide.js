/* Astro Fighters — player-relative world scale authority.
   The 64×64 player frame sets visual scale. Every proportion below is a ratio of the
   player's measured stature S (opaque height of the south-facing base frame), which the
   runtime measures from whichever base sheet is loaded. The hidden 32×32 grid never sets size.

   `player` mirrors production/asset-manifest.json canonical.playerScale (validated in CI).
   `guide` ratios are PROVISIONAL until approved beside the approved 512×64 player in the
   Phaser scale reference scene (index.html?scale). Objects drawn here are scaffold, not art. */
(() => {
  'use strict';

  const player = {
    sheetCanvas: [512, 64],
    frame: [64, 64],
    framesPerSheet: 8,
    frameOrder: ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW'],
    pivotX: 32,
    collision: {w: 20, h: 8},
    interactionRange: 40
  };

  // Ratios of stature S. `tol` is the accepted relative deviation for placed modules.
  const guide = {
    doorOpeningH:   {r: 1.22, tol: .15, label: 'Door clear opening height'},
    doorOpeningW:   {r: 0.62, tol: .20, label: 'Door clear opening width'},
    eaveH:          {r: 1.90, tol: .20, label: 'Single-storey eave underside'},
    windowSill:     {r: 0.62, tol: .20, label: 'Window sill height'},
    windowH:        {r: 0.40, tol: .25, label: 'Window height'},
    windowW:        {r: 0.55, tol: .25, label: 'Window width'},
    plinthH:        {r: 0.30, tol: .35, label: 'Stone plinth / foundation face'},
    stairRise:      {r: 0.12, tol: .25, label: 'Stair riser'},
    stairTread:     {r: 0.11, tol: .35, label: 'Stair tread (projected depth)'},
    stairW:         {r: 1.30, tol: .25, label: 'Stair flight width'},
    counterH:       {r: 0.52, tol: .15, label: 'Counter top height'},
    counterDepth:   {r: 0.22, tol: .30, label: 'Counter top (projected depth)'},
    crateSmall:     {r: 0.30, tol: .25, label: 'Small crate'},
    crateLarge:     {r: 0.48, tol: .20, label: 'Large crate'},
    barrelH:        {r: 0.50, tol: .20, label: 'Barrel height'},
    benchSeat:      {r: 0.27, tol: .20, label: 'Bench seat height'},
    benchLen:       {r: 1.30, tol: .30, label: 'Bench length'},
    postH:          {r: 2.10, tol: .20, label: 'Structural post height'},
    postW:          {r: 0.22, tol: .30, label: 'Structural post width'},
    railH:          {r: 0.55, tol: .20, label: 'Railing height'},
    lanternH:       {r: 1.85, tol: .20, label: 'Lantern post height'},
    beamClearance:  {r: 1.90, tol: .25, label: 'Gate beam clearance'},
    bridgeSingle:   {r: 1.00, tol: .20, label: 'Bridge walkway, single file'},
    bridgePair:     {r: 1.60, tol: .20, label: 'Bridge walkway, two abreast'}
  };

  const px = (key, S) => Math.max(1, Math.round(guide[key].r * S));
  const within = (key, measured, S) => Math.abs(measured / S - guide[key].r) / guide[key].r <= guide[key].tol;

  /* ---- procedural guide objects (scaffold) ---- */
  const C = {
    stone: ['#5c564d', '#777064', '#8f877a', '#a69d8d', '#bdb4a2'], timber: ['#2b2017', '#433124', '#5c4331', '#76563d', '#8f6b4b', '#a8825d'],
    plaster: ['#aca28c', '#c4b99f', '#d7cdb3'], slate: ['#23272b', '#31363b', '#41484e', '#566067'], dark: '#17130f',
    iron: ['#303436', '#474c4e'], water: ['#1b262b', '#26363d', '#33474f'], amber: ['#b9853f', '#dcae62', '#f0cf8f']
  };
  function surface(w, h) {
    const c = document.createElement('canvas'); c.width = Math.max(1, w); c.height = Math.max(1, h);
    const g = c.getContext('2d'); g.imageSmoothingEnabled = false;
    const rect = (x, y, rw, rh, col) => { g.fillStyle = col; g.fillRect(Math.round(x), Math.round(y), Math.round(rw), Math.round(rh)); };
    return {c, g, rect, w: c.width, h: c.height};
  }
  // Front-face box with a projected top face (flat-faced 3/4 cabinet).
  function box(s, x, y, w, faceH, topH, ramp) {
    s.rect(x, y, w, topH, ramp[4] || ramp[3]);
    s.rect(x, y + topH, w, faceH, ramp[2]);
    s.rect(x, y + topH, w, 1, ramp[3]);
    s.rect(x, y + topH + faceH - 1, w, 1, ramp[0]);
    s.rect(x + w - 1, y, 1, topH + faceH, ramp[1]);
  }

  /* Each builder returns {canvas, anchor:[x,y] ground-contact point in canvas px,
     colliders:[{x,y,w,h}] relative to the anchor, occluder, measures:{key:px}}. */
  const items = {
    'wall-door'(S) {
      const L = Math.round(5.5 * S), eave = px('eaveH', S), band = Math.round(.28 * S), plinth = Math.round(.15 * S);
      const dw = px('doorOpeningW', S), dh = px('doorOpeningH', S), ww = px('windowW', S), wh = px('windowH', S), sill = px('windowSill', S);
      const H = eave + band, s = surface(L, H);
      for (let y = 0; y < band; y += 4) { s.rect(0, y, L, 4, C.slate[y < band / 2 ? 1 : 2]); s.rect(0, y, L, 1, C.slate[3]); }
      s.rect(0, band, L, eave - plinth, C.plaster[1]);
      s.rect(0, band, L, 5, C.timber[2]);
      for (const x of [0, Math.round(L / 2 - dw / 2 - 6), Math.round(L / 2 + dw / 2 + 1), L - 5]) s.rect(x, band, 5, eave - plinth, C.timber[3]);
      s.rect(0, H - plinth, L, plinth, C.stone[1]); s.rect(0, H - plinth, L, 1, C.stone[3]);
      const dx = Math.round(L / 2 - dw / 2);
      s.rect(dx - 3, H - dh - 3, dw + 6, dh + 3, C.timber[1]);
      s.rect(dx, H - dh, dw, dh, C.dark);
      const wx = Math.round(L * .2);
      s.rect(wx - 2, H - sill - wh - 2, ww + 4, wh + 4, C.timber[1]);
      s.rect(wx, H - sill - wh, ww, wh, C.plaster[2]);
      for (let x = wx; x < wx + ww; x += 5) s.rect(x, H - sill - wh, 1, wh, C.timber[2]);
      const half = L / 2;
      return {canvas: s.c, anchor: [half, H], occluder: true, sortOffset: 0,
        colliders: [{x: -half, y: -10, w: half - dw / 2, h: 10}, {x: dw / 2, y: -10, w: half - dw / 2, h: 10}],
        measures: {doorOpeningH: dh, doorOpeningW: dw, eaveH: eave, windowSill: sill, windowH: wh, windowW: ww}};
    },
    stairs(S) {
      const n = 6, rise = px('stairRise', S), tread = px('stairTread', S), w = px('stairW', S);
      const s = surface(w + 8, n * (rise + tread) + 4);
      for (let i = 0; i < n; i++) {
        const y = s.h - (i + 1) * (rise + tread);
        s.rect(4, y, w, tread, C.stone[3]);
        s.rect(4, y + tread, w, rise, C.stone[1]);
        s.rect(4, y + tread, w, 1, C.stone[4]);
      }
      s.rect(0, 0, 4, s.h, C.timber[2]); s.rect(w + 4, 0, 4, s.h, C.timber[1]);
      return {canvas: s.c, anchor: [s.w / 2, s.h], occluder: false, sortOffset: -s.h, colliders: [{x: -s.w / 2, y: -s.h, w: 4, h: s.h}, {x: s.w / 2 - 4, y: -s.h, w: 4, h: s.h}], measures: {stairRise: rise, stairTread: tread, stairW: w}};
    },
    counter(S) {
      const h = px('counterH', S), d = px('counterDepth', S), L = Math.round(1.6 * S), s = surface(L, h + d);
      box(s, 0, 0, L, h, d, C.timber);
      s.rect(3, d + 4, L - 6, 1, C.timber[1]);
      return {canvas: s.c, anchor: [L / 2, h + d], occluder: false, colliders: [{x: -L / 2, y: -d - 2, w: L, h: d + 2}], measures: {counterH: h, counterDepth: d}};
    },
    'crate-small'(S) { const e = px('crateSmall', S), t = Math.round(e * .4), s = surface(e, e + t); box(s, 0, 0, e, e, t, C.timber); return {canvas: s.c, anchor: [e / 2, e + t], colliders: [{x: -e / 2, y: -t - 2, w: e, h: t + 2}], measures: {crateSmall: e}}; },
    'crate-large'(S) { const e = px('crateLarge', S), t = Math.round(e * .4), s = surface(e, e + t); box(s, 0, 0, e, e, t, C.timber); s.rect(2, t + Math.round(e / 2), e - 4, 1, C.timber[1]); return {canvas: s.c, anchor: [e / 2, e + t], colliders: [{x: -e / 2, y: -t - 2, w: e, h: t + 2}], measures: {crateLarge: e}}; },
    barrel(S) {
      const h = px('barrelH', S), w = Math.round(.36 * S), s = surface(w, h);
      s.rect(1, 0, w - 2, h, C.timber[3]); s.rect(0, 2, w, h - 4, C.timber[3]); s.rect(0, 0, w, 3, C.timber[4]);
      for (const y of [Math.round(h * .25), Math.round(h * .7)]) s.rect(0, y, w, 2, C.iron[0]);
      s.rect(w - 2, 2, 2, h - 4, C.timber[1]);
      return {canvas: s.c, anchor: [w / 2, h], colliders: [{x: -w / 2, y: -6, w, h: 6}], measures: {barrelH: h}};
    },
    bench(S) {
      const seat = px('benchSeat', S), L = px('benchLen', S), s = surface(L, seat + 5);
      s.rect(0, 0, L, 5, C.timber[4]); s.rect(0, 4, L, 2, C.timber[2]);
      for (const x of [3, L - 7]) s.rect(x, 5, 4, seat, C.timber[1]);
      return {canvas: s.c, anchor: [L / 2, seat + 5], colliders: [{x: -L / 2, y: -6, w: L, h: 6}], measures: {benchSeat: seat, benchLen: L}};
    },
    post(S) {
      const h = px('postH', S), w = px('postW', S), s = surface(w + 8, h);
      s.rect(0, h - 8, w + 8, 8, C.stone[2]); s.rect(4, 0, w, h - 8, C.timber[3]); s.rect(4, 0, 2, h - 8, C.timber[5]); s.rect(w + 2, 0, 2, h - 8, C.timber[1]);
      return {canvas: s.c, anchor: [(w + 8) / 2, h], occluder: true, colliders: [{x: -(w + 8) / 2, y: -6, w: w + 8, h: 6}], measures: {postH: h, postW: w}};
    },
    railing(S) {
      const h = px('railH', S), L = Math.round(3 * S), s = surface(L, h);
      s.rect(0, 0, L, 4, C.timber[4]); s.rect(0, 3, L, 1, C.timber[1]); s.rect(0, Math.round(h * .55), L, 3, C.timber[2]);
      for (let x = 0; x <= L - 4; x += Math.round(.9 * S)) s.rect(x, 0, 4, h, C.timber[3]);
      s.rect(L - 4, 0, 4, h, C.timber[3]);
      return {canvas: s.c, anchor: [L / 2, h], occluder: false, colliders: [{x: -L / 2, y: -4, w: L, h: 4}], measures: {railH: h}};
    },
    lantern(S) {
      const h = px('lanternH', S), s = surface(20, h);
      s.rect(4, h - 8, 12, 8, C.stone[2]); s.rect(8, 22, 4, h - 30, C.timber[2]); s.rect(0, 2, 20, 3, C.slate[1]); s.rect(3, 5, 14, 16, C.amber[1]); s.rect(3, 5, 14, 1, C.amber[2]); s.rect(9, 5, 2, 16, C.timber[1]);
      return {canvas: s.c, anchor: [10, h], occluder: true, colliders: [{x: -6, y: -6, w: 12, h: 6}], measures: {lanternH: h}};
    },
    'bridge-single'(S) { return bridge(S, 'bridgeSingle'); },
    'bridge-pair'(S) { return bridge(S, 'bridgePair'); },
    ruler(S) {
      const s = surface(12, S + 1);
      s.rect(5, 0, 2, S + 1, C.amber[2]);
      for (let k = 0; k <= S; k += 8) s.rect(k % 16 ? 3 : 1, S - k, k % 16 ? 6 : 10, 1, C.amber[2]);
      s.rect(0, 0, 12, 1, C.amber[2]); s.rect(0, S, 12, 1, C.amber[2]);
      return {canvas: s.c, anchor: [6, S + 1], colliders: [], measures: {}};
    }
  };
  const SPAN = 132; // canal crossing length in px (north–south)
  function bridge(S, key) {
    const w = px(key, S), rail = px('railH', S), s = surface(w + 8, SPAN + rail);
    s.rect(4, rail, w, SPAN, C.timber[3]);
    for (let y = rail; y < rail + SPAN; y += 7) s.rect(4, y, w, 1, C.timber[1]);
    for (const x of [0, w + 4]) { s.rect(x, 0, 4, SPAN + rail, C.timber[2]); for (let y = 0; y < SPAN; y += 22) s.rect(x, y, 4, rail, C.timber[4]); }
    return {canvas: s.c, anchor: [(w + 8) / 2, rail + SPAN], occluder: false, sortOffset: -SPAN, walkway: w, span: SPAN,
      colliders: [{x: -(w + 8) / 2, y: -SPAN, w: 4, h: SPAN}, {x: (w + 8) / 2 - 4, y: -SPAN, w: 4, h: SPAN}], measures: {[key]: w}};
  }

  window.AF_SCALE = {player, guide, px, within, items, status: 'provisional — pending the approved 512×64 player sheet and visual review in Phaser'};
})();
