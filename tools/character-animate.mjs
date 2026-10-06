// Deterministic animation renderer: moves the approved rig parts by whole-pixel offsets per frame.
// Reads the locked sheets and the rig outputs (read-only); never redraws or resamples pixels.
// Usage: node tools/character-animate.mjs <body> <state> [--check]
//   reads  production/source/characters/anim/<body>/<state>.json
//   writes production/source/characters/anim/<body>/<state>/<layer>.png  (rows = directions, columns = frames)
//          production/source/characters/anim/<body>/<state>/animation.json (runtime definition + QC report)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { readPng, encodePng } from './lib/png.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const FRAME = 64;
const BODY_SHEETS = {
  male: { body: 'Paperdolls/Male/Layer 1 - Base Body/Male Base Body1.png', arms: 'Paperdolls/Male/Layer 3 - Arms/Male Arms1.png' }
};
// Draw order inside one layer: lower entries are drawn first, so later parts cover them where they overlap.
const Z = ['R-thigh', 'R-shin-foot', 'L-thigh', 'L-shin-foot', 'pelvis', 'torso', 'sash',
  'R-upper-arm', 'R-forearm-hand', 'L-upper-arm', 'L-forearm-hand', 'hair-fall-lower', 'hair-fall-upper', 'head'];
const LEG_PARTS = ['R-thigh', 'R-shin-foot', 'L-thigh', 'L-shin-foot'];

const [bodyName, state, flag] = process.argv.slice(2);
if (!bodyName || !state) { console.error('Usage: node tools/character-animate.mjs <body> <state> [--check]'); process.exit(2); }
const rigDir = path.join(root, 'production/source/characters/rig', bodyName);
const animDir = path.join(root, 'production/source/characters/anim', bodyName);
const spec = JSON.parse(fs.readFileSync(path.join(animDir, `${state}.json`), 'utf8'));
const rig = JSON.parse(fs.readFileSync(path.join(rigDir, 'rig.json'), 'utf8'));
const overlays = JSON.parse(fs.readFileSync(path.join(rigDir, 'overlays.json'), 'utf8'));
const order = rig.frameOrder;

const colourToPart = new Map();
for (const [p, hex] of Object.entries(rig.partColours)) colourToPart.set(hex.slice(1), p);
for (const [p, info] of Object.entries(overlays.overlayParts || {})) colourToPart.set(info.colour.slice(1), p);
const hexAt = (img, x, y) => img.px.toString('hex', (y * img.w + x) * 4, (y * img.w + x) * 4 + 3);
const opaque = (img, x, y) => img.px[(y * img.w + x) * 4 + 3] === 255;

// Resolve the offset of a part at a frame: its own track, else its group's track, else 0.
const groupOf = {};
for (const [g, parts] of Object.entries(spec.groups || {})) for (const p of parts) groupOf[p] = g;
let currentDir = null;
function offset(part, k) {
  const dirTracks = (spec.directionTracks || {})[currentDir] || {};
  const track = dirTracks[part] ?? dirTracks[groupOf[part]] ?? spec.tracks[part] ?? spec.tracks[groupOf[part]];
  if (!track) return [0, 0];
  const v = track[k];
  return Array.isArray(v) ? v : [0, v];
}
for (const [name, track] of [...Object.entries(spec.tracks), ...Object.values(spec.directionTracks || {}).flatMap((t) => Object.entries(t))]) {
  if (track.length !== spec.frames) throw new Error(`Track ${name} has ${track.length} values; spec has ${spec.frames} frames`);
}
if (spec.frames > 16) throw new Error('Animations are capped at 16 frames');

// Layers: body and arms use the body part map; each overlay uses its own part map.
const partMap = readPng(path.join(rigDir, 'part-map.png'));
const layers = [
  { name: 'body', img: readPng(path.join(root, BODY_SHEETS[bodyName].body)), map: partMap, role: 'body' },
  { name: 'arms', img: readPng(path.join(root, BODY_SHEETS[bodyName].arms)), map: partMap, role: 'arms' },
  ...overlays.layers.map((l) => ({
    name: path.basename(l.partMap, '.png'), img: readPng(path.join(root, l.source)), map: readPng(path.join(rigDir, l.partMap)),
    role: l.source.includes('Layer 2') ? 'clothing' : 'overlay'
  }))
];

function render(layer, f, k) {
  const out = Buffer.alloc(FRAME * FRAME * 4), ox = f * FRAME;
  const byPart = new Map();
  for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
    if (!opaque(layer.img, ox + x, y)) continue;
    let part = colourToPart.get(hexAt(layer.map, ox + x, y));
    // A few Arms1 pixels sit just outside the body silhouette: they take the nearest labelled part.
    for (let r = 1; !part && r <= 3; r++) for (let dy = -r; dy <= r && !part; dy++) for (let dx = -r; dx <= r && !part; dx++) {
      const nx = x + dx, ny = y + dy;
      if (nx >= 0 && ny >= 0 && nx < FRAME && ny < FRAME && opaque(layer.map, ox + nx, ny)) part = colourToPart.get(hexAt(layer.map, ox + nx, ny));
    }
    if (!part) throw new Error(`${layer.name} ${order[f]}: pixel ${x},${y} has no rig part`);
    if (!byPart.has(part)) byPart.set(part, []);
    byPart.get(part).push([x, y]);
  }
  for (const part of [...byPart.keys()].sort((a, b) => Z.indexOf(a) - Z.indexOf(b))) {
    const [dx, dy] = offset(part, k);
    for (const [x, y] of byPart.get(part)) {
      const nx = x + dx, ny = y + dy;
      if (nx < 0 || ny < 0 || nx >= FRAME || ny >= FRAME) throw new Error(`${layer.name} ${order[f]} frame ${k}: ${part} leaves the 64×64 frame`);
      layer.img.px.copy(out, (ny * FRAME + nx) * 4, ((y) * layer.img.w + ox + x) * 4, ((y) * layer.img.w + ox + x) * 4 + 4);
    }
  }
  return out;
}

// Render every layer: one sheet per layer, rows = directions, columns = frames.
const sheets = {}, frames = {};
for (const layer of layers) {
  const W = spec.frames * FRAME, H = order.length * FRAME, sheet = Buffer.alloc(W * H * 4);
  frames[layer.name] = [];
  order.forEach((dir, f) => {
    currentDir = dir;
    frames[layer.name][f] = [];
    for (let k = 0; k < spec.frames; k++) {
      const fr = render(layer, f, k);
      frames[layer.name][f][k] = fr;
      for (let y = 0; y < FRAME; y++) fr.copy(sheet, ((f * FRAME + y) * W + k * FRAME) * 4, y * FRAME * 4, (y + 1) * FRAME * 4);
    }
  });
  sheets[layer.name] = encodePng(W, H, sheet);
}

// QC.
const a = (buf, x, y) => x >= 0 && y >= 0 && x < FRAME && y < FRAME && buf[(y * FRAME + x) * 4 + 3] === 255;
const stack = (bufs) => { const o = Buffer.alloc(FRAME * FRAME * 4); for (const b of bufs) for (let i = 0; i < b.length; i += 4) if (b[i + 3]) b.copy(o, i, i, i + 4); return o; };
// Seam gaps: two touching pixels of different parts (in the reference pose) that the frame's offsets pull apart.
// A part above another must not rise relative to it; side-by-side parts must not slide apart horizontally.
function seamGaps(layer, f, k) {
  const ox = f * FRAME, partAt = new Map();
  for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
    if (!opaque(layer.img, ox + x, y)) continue;
    const p = colourToPart.get(hexAt(layer.map, ox + x, y));
    if (p) partAt.set(y * FRAME + x, p);
  }
  let n = 0;
  for (const [i, p] of partAt) {
    const x = i % FRAME, y = (i - x) / FRAME, [dxA, dyA] = offset(p, k);
    const below = partAt.get(i + FRAME), right = x + 1 < FRAME ? partAt.get(i + 1) : undefined;
    if (below && below !== p) { const [, dyB] = offset(below, k); if (dyA < dyB) n++; }
    if (right && right !== p) { const [dxB] = offset(right, k); if (dxB > dxA) n++; }
  }
  return n;
}
const skin = (bodyBuf, dressed) => { let n = 0; for (let i = 0; i < dressed.length; i += 4) if (bodyBuf[i + 3] && dressed.compare(bodyBuf, i, i + 4, i, i + 4) === 0 && bodyBuf.toString('hex', i, i + 3) !== '000000') n++; return n; };
const clothing = layers.filter((l) => l.role === 'clothing').map((l) => l.name);
const qc = { frame0MatchesReference: true, feetPlanted: true, newGaps: {}, newExposedSkin: {} };
order.forEach((dir, f) => {
  currentDir = dir;
  for (const layer of layers) {
    const ref = Buffer.alloc(FRAME * FRAME * 4);
    for (let y = 0; y < FRAME; y++) layer.img.px.copy(ref, y * FRAME * 4, (y * layer.img.w + f * FRAME) * 4, (y * layer.img.w + f * FRAME + FRAME) * 4);
    if (!frames[layer.name][f][0].equals(ref)) qc.frame0MatchesReference = false;
  }
  const bodyArms = (k) => stack([frames.body[f][k], frames.arms[f][k]]);
  for (let k = 0; k < spec.frames; k++) {
    for (const layer of layers) {
      const g = seamGaps(layer, f, k);
      if (g > 0) qc.newGaps[`${layer.name} ${dir}:${k}`] = g;
    }
    for (const c of clothing) {
      const dressed = (kk) => stack([frames.body[f][kk], frames[c][f][kk], frames.arms[f][kk]]);
      const extra = skin(frames.body[f][k], dressed(k)) - skin(frames.body[f][0], dressed(0));
      if (extra > 0) qc.newExposedSkin[`${c} ${dir}:${k}`] = extra;
    }
    for (const leg of LEG_PARTS) { const [dx, dy] = offset(leg, k); if (dx || dy) qc.feetPlanted = false; }
  }
});
qc.pass = qc.frame0MatchesReference && qc.feetPlanted && !Object.keys(qc.newGaps).length && !Object.keys(qc.newExposedSkin).length;

const definition = JSON.stringify({
  schema: 'astro-fighters-character-animation-output/v1',
  body: bodyName, state, status: spec.status, frames: spec.frames, fps: spec.fps,
  frameSize: [FRAME, FRAME], pivot: [32, 63],
  sheetLayout: { rows: order, columns: `frames 0–${spec.frames - 1}` },
  layers: Object.fromEntries(layers.map((l) => [l.name, `${l.name}.png`])),
  drawOrder: overlays.drawOrder,
  rootMotion: spec.rootMotion,
  qc
}, null, 2) + '\n';

const outDir = path.join(animDir, state);
const files = { ...Object.fromEntries(Object.entries(sheets).map(([n, b]) => [`${n}.png`, b])), 'animation.json': definition };
if (flag === '--check') {
  const tmp = path.join(outDir, '.check.png');
  const stale = Object.entries(files).filter(([rel, data]) => {
    const file = path.join(outDir, rel);
    if (!fs.existsSync(file)) return true;
    if (!rel.endsWith('.png')) return fs.readFileSync(file, 'utf8') !== data;
    fs.writeFileSync(tmp, data);
    try { return !readPng(file).px.equals(readPng(tmp).px); } finally { fs.rmSync(tmp, { force: true }); }
  });
  if (stale.length) { console.error(`Animation ${bodyName}/${state} outputs are stale (${stale.map(([r]) => r).join(', ')}); rerun node tools/character-animate.mjs ${bodyName} ${state}`); process.exit(1); }
  if (!qc.pass) { console.error(`Animation ${bodyName}/${state} fails QC: ${JSON.stringify(qc)}`); process.exit(1); }
  console.log(`Animation ${bodyName}/${state} outputs are current and pass QC.`);
} else {
  fs.mkdirSync(outDir, { recursive: true });
  for (const [rel, data] of Object.entries(files)) fs.writeFileSync(path.join(outDir, rel), data);
  console.log(`Wrote ${Object.keys(files).length} files to ${path.relative(root, outDir)}/`);
  console.log(`QC: ${JSON.stringify(qc)}`);
}
