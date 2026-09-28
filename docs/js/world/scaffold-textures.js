/* Astro Fighters — Slice 0 scaffold textures.
   Procedural stand-ins for the AF-IC-SHARED-FOUNDATION world modules, drawn at the
   manifest runtime canvas sizes so authored PNGs can replace them file-for-file.
   These are temporary non-reviewable engine scaffolding, NOT production source or runtime art. */
(() => {
  'use strict';

  const P = {
    stone: ['#3f3b35', '#5c564d', '#777064', '#8f877a', '#a69d8d', '#bdb4a2', '#d1c8b5'],
    mortar: '#35312c',
    soot: '#2a2723',
    moss: ['#3c4629', '#515d36', '#687244'],
    timber: ['#2b2017', '#433124', '#5c4331', '#76563d', '#8f6b4b', '#a8825d'],
    plaster: ['#8e8472', '#aca28c', '#c4b99f', '#d7cdb3'],
    slate: ['#23272b', '#31363b', '#41484e', '#566067'],
    iron: ['#1d2022', '#303436', '#474c4e', '#5f6567'],
    patina: ['#3b675a', '#548673'],
    indigo: ['#1c2536', '#27354e', '#354968', '#4a6285'],
    water: ['#1b262b', '#26363d', '#33474f'],
    amber: ['#7a5230', '#b9853f', '#dcae62', '#f0cf8f']
  };

  function rng(seed) {
    let a = seed >>> 0;
    return () => {
      a = (a + 0x6D2B79F5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const pick = (r, arr) => arr[Math.floor(r() * arr.length)];

  function surface(w, h) {
    const c = document.createElement('canvas');
    c.width = w; c.height = h;
    const g = c.getContext('2d');
    g.imageSmoothingEnabled = false;
    const px = (x, y, col, a = 1) => {
      if (x < 0 || y < 0 || x >= w || y >= h) return;
      g.globalAlpha = a; g.fillStyle = col; g.fillRect(x | 0, y | 0, 1, 1); g.globalAlpha = 1;
    };
    const rect = (x, y, rw, rh, col, a = 1) => { g.globalAlpha = a; g.fillStyle = col; g.fillRect(x | 0, y | 0, rw | 0, rh | 0); g.globalAlpha = 1; };
    return { c, g, px, rect, w, h };
  }

  // Shared pavement courses (heights sum to 128) so every stone variant tiles against every other.
  const COURSES = [17, 21, 15, 19, 18, 22, 16];

  function pavement(s, seed) {
    const r = rng(seed);
    let y = 0;
    for (const ch of COURSES) {
      let x = Math.floor(r() * 40);
      const start = x;
      while (x < start + s.w) {
        const remaining = start + s.w - x;
        let sw = 18 + Math.floor(r() * 26);
        if (remaining - sw < 14) sw = remaining;
        const base = 2 + Math.floor(r() * 3);
        for (let i = 0; i < sw; i++) {
          const cx = (x + i) % s.w;
          for (let j = 0; j < ch; j++) {
            let col = P.stone[base];
            if (i === sw - 1 || j === ch - 1) col = P.mortar;
            else if (j === 0 || i === 0) col = P.stone[Math.min(6, base + 1)];
            else if (j === ch - 2 || i === sw - 2) col = P.stone[base - 1];
            s.px(cx, y + j, col);
          }
        }
        // speckle wear inside the stone
        const n = Math.floor(sw * ch * 0.06);
        for (let k = 0; k < n; k++) {
          const cx = (x + 1 + Math.floor(r() * (sw - 3))) % s.w;
          const cy = y + 1 + Math.floor(r() * (ch - 3));
          s.px(cx, cy, r() < 0.5 ? P.stone[base - 1] : P.stone[Math.min(6, base + 1)]);
        }
        x += sw;
      }
      y += ch;
    }
  }

  function crackLine(s, r, x, y, len, color = P.mortar) {
    let dx = r() < 0.5 ? 1 : -1;
    for (let i = 0; i < len; i++) {
      s.px(x, y, color);
      s.px(x + 1, y, P.stone[5], 0.5);
      if (r() < 0.55) y += 1; else x += dx;
      if (r() < 0.12) dx = -dx;
      if (r() < 0.07) crackLine(s, r, x, y, Math.floor(len / 3), color);
    }
  }

  const draw = {
    'stone-clean'(s) { pavement(s, 11); },
    'stone-cracked'(s) {
      pavement(s, 11);
      const r = rng(23);
      for (let i = 0; i < 5; i++) crackLine(s, r, 10 + Math.floor(r() * 170), 6 + Math.floor(r() * 100), 14 + Math.floor(r() * 18));
      for (let i = 0; i < 90; i++) s.px(Math.floor(r() * s.w), Math.floor(r() * s.h), pick(r, P.moss), 0.8);
    },
    'stone-patched'(s) {
      pavement(s, 11);
      const r = rng(37);
      // small reset cobbles
      const ox = 58, oy = 38;
      for (let y = 0; y < 44; y += 7) for (let x = 0; x < 64; x += 8) {
        const base = 1 + Math.floor(r() * 3);
        s.rect(ox + x, oy + y, 8, 7, P.mortar);
        s.rect(ox + x, oy + y, 7, 6, P.stone[base]);
        s.rect(ox + x, oy + y, 7, 1, P.stone[base + 1]);
      }
      // timber repair plank
      s.rect(132, 84, 40, 9, P.timber[1]);
      s.rect(132, 84, 40, 1, P.timber[4]);
      s.rect(132, 92, 40, 1, P.timber[0]);
      s.px(135, 88, P.iron[3]); s.px(168, 88, P.iron[3]);
    },
    'stone-timber-transition'(s) {
      const tmp = surface(s.w, 128); pavement(tmp, 11);
      s.g.drawImage(tmp.c, 0, 0, s.w, 28, 0, 0, s.w, 28);
      s.rect(0, 28, s.w, 4, P.stone[5]);
      s.rect(0, 31, s.w, 1, P.stone[1]);
      const r = rng(41);
      for (let y = 32; y < s.h; y += 8) {
        let x = -Math.floor(r() * 30);
        while (x < s.w) {
          const len = 30 + Math.floor(r() * 40);
          const t = 2 + Math.floor(r() * 3);
          s.rect(x, y, len, 7, P.timber[t]);
          s.rect(x, y, len, 1, P.timber[t + 1]);
          s.rect(x + len - 1, y, 1, 7, P.timber[0]);
          for (let k = 0; k < len; k += 5 + Math.floor(r() * 7)) s.px(x + k, y + 3 + Math.floor(r() * 3), P.timber[t - 1]);
          x += len;
        }
        s.rect(0, y + 7, s.w, 1, P.timber[0]);
      }
    },
    'building-threshold'(s) {
      s.rect(0, 0, s.w, 9, P.timber[2]);
      s.rect(0, 0, s.w, 2, P.timber[4]);
      s.rect(0, 8, s.w, 1, P.timber[0]);
      s.rect(0, 9, s.w, 40, P.stone[4]);
      const r = rng(53);
      for (let i = 0; i < 260; i++) s.px(Math.floor(r() * s.w), 10 + Math.floor(r() * 38), r() < 0.5 ? P.stone[3] : P.stone[5]);
      s.rect(0, 9, s.w, 1, P.stone[6]);
      s.rect(42, 9, 1, 40, P.stone[2]);
      s.rect(86, 9, 1, 40, P.stone[2]);
      s.rect(0, 49, s.w, 10, P.stone[2]);
      s.rect(0, 49, s.w, 1, P.stone[5]);
      s.rect(0, 59, s.w, 5, P.soot, 0.55);
      // worn centre where feet cross
      for (let i = 0; i < 120; i++) s.px(44 + Math.floor(r() * 40), 14 + Math.floor(r() * 30), P.stone[5], 0.8);
    },
    'drainage-channel'(s) {
      const r = rng(61);
      const curb = (y0, hgt) => {
        let x = -Math.floor(r() * 20);
        while (x < s.w) {
          const len = 22 + Math.floor(r() * 18);
          s.rect(x, y0, len, hgt, P.stone[4]);
          s.rect(x, y0, len, 1, P.stone[6]);
          s.rect(x + len - 1, y0, 1, hgt, P.mortar);
          s.rect(x, y0 + hgt - 1, len, 1, P.stone[2]);
          x += len;
        }
      };
      s.rect(0, 8, s.w, 32, P.slate[1]);
      s.rect(0, 8, s.w, 5, P.slate[0]);
      s.rect(0, 25, s.w, 5, P.water[1]);
      s.rect(0, 25, s.w, 1, P.water[2]);
      for (let i = 0; i < 70; i++) s.px(Math.floor(r() * s.w), 14 + Math.floor(r() * 24), pick(r, [P.slate[2], P.moss[0], P.soot]));
      curb(0, 8);
      curb(40, 8);
    },
    'drainage-grate'(s) {
      s.rect(0, 0, s.w, s.h, P.iron[1]);
      s.rect(0, 0, s.w, 1, P.iron[3]);
      s.rect(0, s.h - 1, s.w, 1, P.iron[0]);
      s.rect(3, 4, s.w - 6, s.h - 8, P.slate[0]);
      for (let x = 5; x < s.w - 4; x += 4) { s.rect(x, 4, 2, s.h - 8, P.iron[2]); s.rect(x, 4, 1, s.h - 8, P.iron[3]); }
      const r = rng(67);
      for (let i = 0; i < 18; i++) s.px(Math.floor(r() * s.w), Math.floor(r() * s.h), pick(r, P.patina));
    },
    cracks(s) {
      const r = rng(71);
      crackLine(s, r, 30, 4, 40, P.soot);
      crackLine(s, r, 18, 30, 22, P.soot);
    },
    stains(s) {
      const r = rng(79);
      for (let i = 0; i < 900; i++) {
        const a = r() * Math.PI * 2, d = Math.sqrt(r()) * 28;
        const x = 32 + Math.cos(a) * d * 1.1, y = 32 + Math.sin(a) * d * 0.7;
        if (r() < 0.55) s.px(x, y, P.soot, 0.22 + (1 - d / 28) * 0.25);
      }
    },
    'cart-wear'(s) {
      const r = rng(83);
      for (const ty of [16, 40]) {
        for (let x = 0; x < s.w; x++) {
          const fade = Math.min(1, x / 18, (s.w - x) / 18);
          for (let j = 0; j < 6; j++) {
            if (r() < 0.6 * fade) s.px(x, ty + j, j < 2 ? P.stone[6] : P.soot, j < 2 ? 0.35 : 0.3);
          }
        }
      }
    },
    'timber-post'(s) {
      s.rect(12, 112, 24, 16, P.stone[3]);
      s.rect(12, 112, 24, 2, P.stone[5]);
      s.rect(34, 112, 2, 16, P.stone[1]);
      s.rect(17, 0, 14, 113, P.timber[3]);
      s.rect(17, 0, 2, 113, P.timber[5]);
      s.rect(29, 0, 2, 113, P.timber[1]);
      const r = rng(89);
      for (let i = 0; i < 40; i++) s.rect(19 + Math.floor(r() * 10), Math.floor(r() * 108), 1, 3 + Math.floor(r() * 5), P.timber[2]);
      for (const by of [18, 92]) { s.rect(16, by, 16, 4, P.iron[1]); s.rect(16, by, 16, 1, P.iron[3]); s.px(20, by + 2, P.iron[3]); s.px(27, by + 2, P.iron[3]); }
    },
    'horizontal-beam'(s) {
      s.rect(0, 14, s.w, 5, P.timber[4]);
      s.rect(0, 14, s.w, 1, P.timber[5]);
      s.rect(0, 19, s.w, 12, P.timber[2]);
      s.rect(0, 30, s.w, 2, P.timber[0]);
      const r = rng(97);
      for (let i = 0; i < 50; i++) s.rect(Math.floor(r() * s.w), 20 + Math.floor(r() * 9), 3 + Math.floor(r() * 7), 1, P.timber[1]);
      s.rect(0, 14, 3, 18, P.timber[1]);
      s.rect(s.w - 3, 14, 3, 18, P.timber[1]);
      for (const bx of [6, s.w - 18]) { s.rect(bx, 18, 12, 12, P.iron[1]); s.rect(bx, 18, 12, 1, P.iron[3]); s.px(bx + 3, 23, P.iron[3]); s.px(bx + 8, 23, P.iron[3]); }
      s.rect(4, 32, s.w - 8, 3, P.soot, 0.35);
    },
    'timber-plaster-wall'(s) {
      // slate eave
      for (let y = 0; y < 22; y += 4) {
        const off = (y / 4) % 2 ? 3 : 0;
        s.rect(0, y, s.w, 4, P.slate[y < 8 ? 1 : 2]);
        for (let x = off; x < s.w; x += 6) s.rect(x, y + 3, 1, 1, P.slate[0]);
        s.rect(0, y, s.w, 1, P.slate[3]);
      }
      s.rect(0, 22, s.w, 3, P.slate[0]);
      // top rail
      s.rect(0, 25, s.w, 7, P.timber[2]);
      s.rect(0, 25, s.w, 1, P.timber[4]);
      // plaster field
      s.rect(0, 32, s.w, 116, P.plaster[2]);
      const r = rng(101);
      for (let i = 0; i < 700; i++) s.px(Math.floor(r() * s.w), 32 + Math.floor(r() * 116), r() < 0.6 ? P.plaster[1] : P.plaster[3]);
      for (let i = 0; i < 400; i++) { const y = 110 + Math.floor(Math.pow(r(), 0.6) * 38); s.px(Math.floor(r() * s.w), y, P.plaster[0], 0.6); }
      // mid rail
      s.rect(0, 88, s.w, 6, P.timber[2]);
      s.rect(0, 88, s.w, 1, P.timber[4]);
      // posts (half posts at edges tile into full posts)
      for (const [x, wdt] of [[0, 5], [93, 10], [s.w - 5, 5]]) {
        s.rect(x, 25, wdt, 123, P.timber[3]);
        s.rect(x, 25, 1, 123, P.timber[5]);
        s.rect(x + wdt - 1, 25, 1, 123, P.timber[1]);
      }
      // lattice window in the left bay
      s.rect(22, 42, 50, 36, P.timber[1]);
      s.rect(24, 44, 46, 32, P.plaster[3]);
      for (let x = 24; x < 70; x += 6) s.rect(x, 44, 1, 32, P.timber[2]);
      for (let y = 44; y < 76; y += 8) s.rect(24, y, 46, 1, P.timber[2]);
      // sill
      s.rect(0, 148, s.w, 12, P.timber[1]);
      s.rect(0, 148, s.w, 1, P.timber[4]);
    },
    'aged-stone-foundation'(s) {
      const r = rng(107);
      s.rect(0, 0, s.w, 7, P.stone[5]);
      s.rect(0, 0, s.w, 1, P.stone[6]);
      s.rect(0, 6, s.w, 1, P.stone[1]);
      let y = 7;
      for (const ch of [28, 29]) {
        let x = -Math.floor(r() * 30);
        while (x < s.w) {
          const len = 34 + Math.floor(r() * 30);
          const base = 2 + Math.floor(r() * 2);
          s.rect(x, y, len, ch, P.stone[base]);
          s.rect(x, y, len, 1, P.stone[base + 2]);
          s.rect(x, y, 1, ch, P.stone[base + 1]);
          s.rect(x + len - 1, y, 1, ch, P.mortar);
          s.rect(x, y + ch - 1, len, 1, P.mortar);
          for (let i = 0; i < len * ch * 0.05; i++) s.px(x + Math.floor(r() * len), y + Math.floor(r() * ch), P.stone[base - 1]);
          x += len;
        }
        y += ch;
      }
      for (let i = 0; i < 240; i++) { const yy = s.h - 1 - Math.floor(Math.pow(r(), 2) * 16); s.px(Math.floor(r() * s.w), yy, pick(r, P.moss)); }
    },
    // Dressing / occluder scaffolds (not manifest dependencies; required Slice 0 roles).
    noren(s) {
      s.rect(0, 0, s.w, 4, P.timber[2]);
      s.rect(0, 0, s.w, 1, P.timber[4]);
      for (let i = 0; i < 3; i++) {
        const x = 2 + i * 20;
        s.rect(x, 4, 19, s.h - 4, P.indigo[2]);
        s.rect(x, 4, 1, s.h - 4, P.indigo[3]);
        s.rect(x + 18, 4, 1, s.h - 4, P.indigo[0]);
        s.rect(x, s.h - 2, 19, 2, P.indigo[1]);
      }
      // pale crest ring across the centre panel
      for (let a = 0; a < 40; a++) { const t = a / 40 * Math.PI * 2; s.px(32 + Math.cos(t) * 7, 20 + Math.sin(t) * 7, P.plaster[3]); }
    },
    'lantern-post'(s) {
      s.rect(10, 100, 12, 12, P.stone[3]);
      s.rect(10, 100, 12, 1, P.stone[5]);
      s.rect(14, 30, 4, 72, P.timber[2]);
      s.rect(14, 30, 1, 72, P.timber[4]);
      s.rect(6, 8, 20, 4, P.slate[1]);
      s.rect(8, 12, 16, 18, P.amber[2]);
      s.rect(8, 12, 16, 1, P.amber[3]);
      s.rect(8, 12, 1, 18, P.timber[1]); s.rect(23, 12, 1, 18, P.timber[1]); s.rect(15, 12, 2, 18, P.timber[1]);
      s.rect(8, 20, 16, 1, P.timber[1]);
      s.rect(6, 30, 20, 3, P.slate[1]);
    },
    'crate-stack'(s) {
      const crate = (x, y, w, h, t) => {
        s.rect(x, y, w, h, P.timber[t]);
        s.rect(x, y, w, 2, P.timber[t + 2]);
        s.rect(x, y, 2, h, P.timber[t + 1]);
        s.rect(x + w - 2, y, 2, h, P.timber[0]);
        s.rect(x, y + h - 2, w, 2, P.timber[0]);
        for (let yy = y + 6; yy < y + h - 2; yy += 6) s.rect(x + 2, yy, w - 4, 1, P.timber[t - 1]);
      };
      crate(2, 26, 26, 28, 2);
      crate(26, 30, 20, 24, 3);
      crate(10, 4, 22, 22, 3);
      s.rect(2, 54, 44, 2, P.soot, 0.5);
    }
  };

  const SPECS = {
    'stone-clean': [192, 128], 'stone-cracked': [192, 128], 'stone-patched': [192, 128],
    'stone-timber-transition': [128, 64], 'building-threshold': [128, 64],
    'drainage-channel': [160, 48], 'drainage-grate': [48, 32],
    cracks: [64, 64], stains: [64, 64], 'cart-wear': [96, 64],
    'timber-post': [48, 128], 'horizontal-beam': [128, 48],
    'timber-plaster-wall': [192, 160], 'aged-stone-foundation': [192, 64],
    noren: [64, 44], 'lantern-post': [32, 112], 'crate-stack': [48, 56]
  };

  function build(id) {
    const size = SPECS[id];
    if (!size || !draw[id]) throw new Error(`Unknown scaffold module ${id}`);
    const s = surface(size[0], size[1]);
    draw[id](s);
    return s.c;
  }

  window.AF_SCAFFOLD = { SPECS, build, palette: P };
})();
