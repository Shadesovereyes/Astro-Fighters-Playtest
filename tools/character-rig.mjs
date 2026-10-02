// Deterministic part split + anchors for a locked 512×64 base body sheet.
// Reads the locked Body1 and Arms1 sheets; never writes to them.
// Usage: node tools/character-rig.mjs <male|female> [--check]
//   writes production/source/characters/rig/<body>/part-map.png and rig.json
//   --check regenerates in memory and fails if the committed outputs differ.
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const FRAME = 64;
const ORDER = ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW'];

// Anatomical side on screen-left (null = profile), and which side is nearer the camera.
const VIEW = {
  S: { screenLeft: 'R', near: null }, SE: { screenLeft: 'R', near: 'R' }, E: { screenLeft: null, near: 'R' },
  NE: { screenLeft: 'L', near: 'R' }, N: { screenLeft: 'L', near: null }, NW: { screenLeft: 'L', near: 'L' },
  W: { screenLeft: null, near: 'L' }, SW: { screenLeft: 'R', near: 'L' }
};

// Body-specific split parameters (local frame coordinates).
const CONFIG = {
  male: {
    body: 'Paperdolls/Male/Layer 1 - Base Body/Male Base Body1.png',
    arms: 'Paperdolls/Male/Layer 3 - Arms/Male Arms1.png',
    headEnd: 20,
    pelvis: [33, 38],
    pelvisColourRows: [39, 40],
    elbow: { S: 28, SE: 28, E: 30, NE: 28, N: 28, NW: 28, W: 30, SW: 28 },
    // Profile views: the far leg is the thin strip behind the near leg. Per-row boundary read from the
    // sheet (E: far leg at x <= value; W: far leg at x >= value). Interior separator lines go to the near leg.
    profileFarLeg: {
      E: { farOn: 'left', rows: { 47: 30, 48: 29, 49: 28, 50: 28, 51: 28, 52: 29, 53: 29, 54: 29, 55: 29, 56: 29, 57: 30, 58: 30, 59: 31, 60: 30 } },
      W: { farOn: 'right', rows: { 47: 33, 48: 34, 49: 35, 50: 35, 51: 35, 52: 34, 53: 34, 54: 34, 55: 34, 56: 34, 57: 33, 58: 33, 59: 32, 60: 33 } }
    },
    kneeOverride: { E: 46, W: 46 },
    kneeSearch: [42, 50]
  }
};

const PART_COLOURS = {
  head: [230, 25, 75], torso: [60, 180, 75], pelvis: [255, 225, 25],
  'R-upper-arm': [0, 130, 200], 'R-forearm-hand': [70, 240, 240],
  'L-upper-arm': [145, 30, 180], 'L-forearm-hand': [240, 50, 230],
  'R-thigh': [245, 130, 48], 'R-shin-foot': [170, 110, 40],
  'L-thigh': [128, 128, 0], 'L-shin-foot': [0, 0, 128]
};
const PARTS = Object.keys(PART_COLOURS);

function paeth(a, b, c) {
  const p = a + b - c, pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c);
  return pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
}

function readPng(file) {
  const d = fs.readFileSync(file);
  let o = 8, w, h, idat = [];
  while (o < d.length) {
    const len = d.readUInt32BE(o), type = d.toString('ascii', o + 4, o + 8), c = d.subarray(o + 8, o + 8 + len);
    if (type === 'IHDR') {
      w = c.readUInt32BE(0); h = c.readUInt32BE(4);
      if (c[8] !== 8 || c[9] !== 6 || c[12] !== 0) throw new Error(`${file}: need 8-bit RGBA, non-interlaced`);
    } else if (type === 'IDAT') idat.push(c);
    o += 12 + len;
  }
  const raw = zlib.inflateSync(Buffer.concat(idat)), stride = w * 4, px = Buffer.alloc(stride * h);
  for (let y = 0, s = 0; y < h; y++) {
    const f = raw[s++];
    for (let x = 0; x < stride; x++) {
      const a = x >= 4 ? px[y * stride + x - 4] : 0, b = y ? px[(y - 1) * stride + x] : 0, c = x >= 4 && y ? px[(y - 1) * stride + x - 4] : 0;
      const v = raw[s++];
      px[y * stride + x] = (f === 0 ? v : f === 1 ? v + a : f === 2 ? v + b : f === 3 ? v + ((a + b) >> 1) : v + paeth(a, b, c)) & 255;
    }
  }
  return { w, h, px };
}

function encodePng(w, h, px) {
  const crcTable = Array.from({ length: 256 }, (_, n) => { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; return c >>> 0; });
  const crc = (buf) => { let c = 0xffffffff; for (const b of buf) c = crcTable[(c ^ b) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; };
  const chunk = (type, data) => { const t = Buffer.from(type), len = Buffer.alloc(4), cr = Buffer.alloc(4); len.writeUInt32BE(data.length); cr.writeUInt32BE(crc(Buffer.concat([t, data]))); return Buffer.concat([len, t, data, cr]); };
  const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4); ihdr[8] = 8; ihdr[9] = 6;
  const raw = Buffer.alloc((w * 4 + 1) * h);
  for (let y = 0; y < h; y++) px.copy(raw, y * (w * 4 + 1) + 1, y * w * 4, (y + 1) * w * 4);
  return Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), chunk('IHDR', ihdr), chunk('IDAT', zlib.deflateSync(raw, { level: 9 })), chunk('IEND', Buffer.alloc(0))]);
}

const hex = (img, x, y) => { const i = (y * img.w + x) * 4; return img.px.toString('hex', i, i + 3); };
const opaque = (img, x, y) => x >= 0 && y >= 0 && x < img.w && y < img.h && img.px[(y * img.w + x) * 4 + 3] === 255;
const isWrap = (c) => c === 'ffffff' || c === 'e3e3e3';
const centre = (xs) => Math.round((Math.min(...xs) + Math.max(...xs)) / 2);

function components(points) {
  const key = (x, y) => `${x},${y}`, set = new Set(points.map(([x, y]) => key(x, y))), seen = new Set(), out = [];
  for (const [x, y] of points) {
    if (seen.has(key(x, y))) continue;
    const comp = [], stack = [[x, y]]; seen.add(key(x, y));
    while (stack.length) {
      const [cx, cy] = stack.pop(); comp.push([cx, cy]);
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
        const k = key(cx + dx, cy + dy);
        if (set.has(k) && !seen.has(k)) { seen.add(k); stack.push([cx + dx, cy + dy]); }
      }
    }
    out.push(comp);
  }
  return out;
}

function splitFrame(cfg, body, arms, f) {
  const dir = ORDER[f], view = VIEW[dir], ox = f * FRAME;
  const label = new Map(), notes = [];
  const key = (x, y) => `${x},${y}`;
  const bodyPts = [];
  for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) if (opaque(body, ox + x, y)) bodyPts.push([x, y]);
  const colour = (x, y) => hex(body, ox + x, y);
  const isArm = (x, y) => opaque(arms, ox + x, y);

  // Arms: Arms1 ∩ Body1, one component per visible arm.
  const armComps = components(bodyPts.filter(([x, y]) => isArm(x, y))).filter((c) => c.length > 4)
    .sort((a, b) => a.reduce((s, p) => s + p[0], 0) / a.length - b.reduce((s, p) => s + p[0], 0) / b.length);
  const armSides = view.screenLeft ? (armComps.length === 2 ? [view.screenLeft, view.screenLeft === 'R' ? 'L' : 'R'] : null) : [view.near];
  if (!armSides || armSides.length !== armComps.length) throw new Error(`${dir}: expected ${view.screenLeft ? 2 : 1} arm components, found ${armComps.length}`);
  armComps.forEach((comp, i) => {
    for (const [x, y] of comp) label.set(key(x, y), `${armSides[i]}-${y <= cfg.elbow[dir] ? 'upper-arm' : 'forearm-hand'}`);
  });
  // Stray Arms1 fragments (≤4 px) follow the nearest labelled arm pixel.
  if (!view.screenLeft) notes.push(`far (${view.near === 'R' ? 'L' : 'R'}) arm fully hidden by the body; no pixels`);

  // Head, torso, pelvis.
  const neckRow = bodyPts.filter(([x, y]) => y === cfg.headEnd - 1 && !isArm(x, y)).map(([x]) => x);
  const [neckMin, neckMax] = [Math.min(...neckRow), Math.max(...neckRow)];
  const legPts = [];
  for (const [x, y] of bodyPts) {
    const k = key(x, y);
    if (label.has(k) || isArm(x, y)) continue;
    if (y < cfg.headEnd || (y === cfg.headEnd && x >= neckMin && x <= neckMax)) label.set(k, 'head');
    else if (y < cfg.pelvis[0]) label.set(k, 'torso');
    else if (y <= cfg.pelvis[1]) label.set(k, 'pelvis');
    else if (y <= cfg.pelvisColourRows[1] && isWrap(colour(x, y))) label.set(k, 'pelvis');
    else legPts.push([x, y]);
  }

  // Legs: per-row split along the interior separator between the two legs.
  const legSet = new Set(legPts.map(([x, y]) => key(x, y)));
  const crotch = bodyPts.filter(([x, y]) => y === cfg.pelvis[1] && colour(x, y) === '000000' && !isArm(x, y)).map(([x]) => x);
  const crotchX = crotch.length ? crotch.reduce((a, b) => (Math.abs(b - 31.5) < Math.abs(a - 31.5) ? b : a)) : 32;
  const profile = cfg.profileFarLeg[dir];
  let prev = crotchX;
  const split = {};
  for (let y = cfg.pelvis[1] + 1; y < FRAME && !profile; y++) {
    const xs = legPts.filter((p) => p[1] === y).map((p) => p[0]);
    if (!xs.length) continue;
    const cells = [];
    for (let x = Math.min(...xs); x <= Math.max(...xs); x++) cells.push({ x, c: legSet.has(key(x, y)) ? (colour(x, y) === '000000' ? 'k' : 'c') : 'e' });
    const seps = [];
    for (let i = 0; i < cells.length; i++) {
      if (cells[i].c === 'c') continue;
      let j = i; while (j + 1 < cells.length && cells[j + 1].c !== 'c') j++;
      if (cells.slice(0, i).some((q) => q.c === 'c') && cells.slice(j + 1).some((q) => q.c === 'c')) seps.push([cells[i].x, cells[j].x]);
      i = j;
    }
    const tol = 4;
    const best = seps.map(([a, b]) => ({ a, b, m: (a + b) / 2 })).filter((s) => Math.abs(s.m - prev) <= tol).sort((p, q) => Math.abs(p.m - prev) - Math.abs(q.m - prev))[0];
    // Rows with no separator (e.g. an all-outline sole row) inherit the split above in two-leg views.
    split[y] = best ? Math.floor(best.m) : Math.floor(prev);
    if (best) prev = best.m;
  }
  const sideOf = (x, y) => {
    const s = split[y];
    if (view.screenLeft) {
      if (s === null || s === undefined) throw new Error(`${dir}: no leg separator on row ${y}`);
      return x <= s ? view.screenLeft : view.screenLeft === 'R' ? 'L' : 'R';
    }
    const far = view.near === 'R' ? 'L' : 'R', b = profile.rows[y];
    if (b === undefined) return view.near;
    return (profile.farOn === 'left' ? x <= b : x >= b) ? far : view.near;
  };
  const legs = { R: [], L: [] };
  for (const [x, y] of legPts) legs[sideOf(x, y)].push([x, y]);
  const knee = {};
  for (const side of ['R', 'L']) {
    const pts = legs[side];
    if (!pts.length) { knee[side] = null; continue; }
    const rows = [];
    for (let y = cfg.kneeSearch[0]; y <= cfg.kneeSearch[1]; y++) { const n = pts.filter((p) => p[1] === y).length; if (n) rows.push([y, n]); }
    const top = Math.min(...pts.map((p) => p[1]));
    if (!view.screenLeft && side !== view.near && top > cfg.kneeSearch[0]) {
      knee[side] = null; notes.push(`far (${side}) thigh hidden behind the near thigh; far leg visible from y=${top} as shin-foot only`);
    } else knee[side] = cfg.kneeOverride?.[dir] && side === view.near ? cfg.kneeOverride[dir] : rows.sort((a, b) => a[1] - b[1] || a[0] - b[0])[0][0];
    for (const [x, y] of pts) label.set(key(x, y), `${side}-${knee[side] !== null && y <= knee[side] ? 'thigh' : 'shin-foot'}`);
  }

  // Any remaining pixel (stray Arms1 fragment) takes the label of its nearest labelled neighbour.
  for (const [x, y] of bodyPts) {
    if (label.has(key(x, y))) continue;
    let best = null;
    for (let r = 1; r < 4 && !best; r++) for (let dy = -r; dy <= r && !best; dy++) for (let dx = -r; dx <= r && !best; dx++) best = label.get(key(x + dx, y + dy)) || null;
    if (!best) throw new Error(`${dir}: unlabelled pixel ${x},${y}`);
    label.set(key(x, y), best);
  }

  // Anchors (local frame coordinates).
  const of = (part) => bodyPts.filter(([x, y]) => label.get(key(x, y)) === part);
  const at = (pts, y) => pts.filter((p) => p[1] === y).map((p) => p[0]);
  const anchors = {};
  const head = of('head'), skull = head.filter((p) => p[1] < cfg.headEnd - 1);
  anchors.head = [centre(skull.map((p) => p[0])), Math.min(...skull.map((p) => p[1]))];
  anchors.neck = [centre(at(head, cfg.headEnd).length ? at(head, cfg.headEnd) : at(head, cfg.headEnd - 1)), cfg.headEnd];
  for (const side of ['R', 'L']) {
    const upper = of(`${side}-upper-arm`), fore = of(`${side}-forearm-hand`);
    if (upper.length) {
      const top = Math.min(...upper.map((p) => p[1]));
      anchors[`${side}-shoulder`] = [centre(upper.filter((p) => p[1] <= top + 2).map((p) => p[0])), top];
      anchors[`${side}-elbow`] = [centre(at(upper, cfg.elbow[dir])), cfg.elbow[dir]];
    } else { anchors[`${side}-shoulder`] = null; anchors[`${side}-elbow`] = null; }
    if (fore.length) {
      const wrapRows = fore.filter(([x, y]) => isWrap(colour(x, y))).map((p) => p[1]);
      const below = wrapRows.length ? fore.filter((p) => p[1] > Math.max(...wrapRows)) : fore.filter((p) => p[1] >= Math.max(...fore.map((q) => q[1])) - 3);
      anchors[`${side}-hand-grip`] = [centre(below.map((p) => p[0])), Math.round(below.reduce((s, p) => s + p[1], 0) / below.length)];
    } else anchors[`${side}-hand-grip`] = null;
    const leg = legs[side];
    if (leg.length) {
      anchors[`${side}-knee`] = knee[side] !== null ? [centre(at(leg, knee[side])), knee[side]] : null;
      const sole = Math.max(...leg.map((p) => p[1]));
      anchors[`${side}-foot`] = [centre(at(leg, sole)), sole];
    } else { anchors[`${side}-knee`] = null; anchors[`${side}-foot`] = null; }
  }
  const pelvis = of('pelvis');
  anchors.hip = [centre(pelvis.map((p) => p[0])), cfg.pelvis[1]];

  const counts = Object.fromEntries(PARTS.map((p) => [p, of(p).length]));
  const near = view.near, far = near ? (near === 'R' ? 'L' : 'R') : null;
  return { dir, label, frame: {
    direction: dir, frame: f, anatomicalScreenLeft: view.screenLeft, nearSide: near, farSide: far,
    elbowRow: cfg.elbow[dir], kneeRow: knee, pixelCounts: counts, anchors, notes
  } };
}

function build(name) {
  const cfg = CONFIG[name];
  if (!cfg) throw new Error(`No rig config for ${name}`);
  const body = readPng(path.join(root, cfg.body)), arms = readPng(path.join(root, cfg.arms));
  if (body.w !== 512 || body.h !== 64) throw new Error('Body sheet must be 512×64');
  const map = Buffer.alloc(512 * 64 * 4), frames = [];
  let total = 0, labelled = 0;
  for (let f = 0; f < 8; f++) {
    const { label, frame } = splitFrame(cfg, body, arms, f);
    for (const [k, part] of label) {
      const [x, y] = k.split(',').map(Number), i = (y * 512 + f * FRAME + x) * 4;
      map.set([...PART_COLOURS[part], 255], i); labelled++;
    }
    frames.push(frame);
  }
  for (let i = 3; i < body.px.length; i += 4) if (body.px[i]) total++;
  if (total !== labelled) throw new Error(`Coverage mismatch: ${labelled} labelled of ${total} body pixels`);
  for (let i = 3; i < body.px.length; i += 4) if ((body.px[i] === 255) !== (map[i] === 255)) throw new Error('Part map does not match body silhouette');
  const rig = {
    schema: 'astro-fighters-character-rig/v1',
    body: name,
    source: { body: cfg.body, arms: cfg.arms },
    frameSize: [FRAME, FRAME],
    frameOrder: ORDER,
    status: 'candidate — pending user approval',
    method: {
      head: `rows ≤ ${cfg.headEnd} (row ${cfg.headEnd} only within the neck columns of row ${cfg.headEnd - 1})`,
      torso: `rows ${cfg.headEnd}–${cfg.pelvis[0] - 1} excluding arms`,
      pelvis: `rows ${cfg.pelvis[0]}–${cfg.pelvis[1]} plus shorts-coloured pixels on rows ${cfg.pelvisColourRows.join('–')}`,
      arms: 'Arms1 ∩ Body1 components; upper arm at or above the elbow row',
      legs: 'per-row split at the interior separator nearest the crotch; profiles use the per-row far-leg boundary in the tool config; thigh at or above the narrowest row in the knee search band (profile near knee fixed at row 46)',
      anatomicalSides: 'R/L are the character\'s own sides; nearSide/farSide per direction (null for S and N)'
    },
    partColours: Object.fromEntries(PARTS.map((p) => [p, '#' + PART_COLOURS[p].map((v) => v.toString(16).padStart(2, '0')).join('')])),
    totalPixels: total,
    frames
  };
  return { png: encodePng(512, 64, map), json: JSON.stringify(rig, null, 2) + '\n' };
}

const [name, flag] = process.argv.slice(2);
if (!name) { console.error('Usage: node tools/character-rig.mjs <male> [--check]'); process.exit(2); }
const outDir = path.join(root, 'production/source/characters/rig', name);
const { png, json } = build(name);
if (flag === '--check') {
  const okPng = fs.existsSync(path.join(outDir, 'part-map.png')) && readPng(path.join(outDir, 'part-map.png')).px.equals(readPng.call(null, (() => { const t = path.join(outDir, '.check.png'); fs.writeFileSync(t, png); return t; })()).px);
  fs.rmSync(path.join(outDir, '.check.png'), { force: true });
  const okJson = fs.existsSync(path.join(outDir, 'rig.json')) && fs.readFileSync(path.join(outDir, 'rig.json'), 'utf8') === json;
  if (!okPng || !okJson) { console.error(`Rig outputs for ${name} are stale or missing; rerun node tools/character-rig.mjs ${name}`); process.exit(1); }
  console.log(`Rig outputs for ${name} are current.`);
} else {
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'part-map.png'), png);
  fs.writeFileSync(path.join(outDir, 'rig.json'), json);
  console.log(`Wrote ${path.relative(root, outDir)}/part-map.png and rig.json`);
}
