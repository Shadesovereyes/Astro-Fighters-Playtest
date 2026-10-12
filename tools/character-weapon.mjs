// Deterministic weapon-layer renderer: draws rigid weapon items (production/source/characters/items/<item>.json) as
// authored bands along their axes, placed per frame at the grip points authored in the state spec (spec.weapons, one
// entry per hand: slot main = near hand on the arms layer, slot off = far hand on the body layer; spec.weapon is the
// single main-hand form), and checks each grip registers with its fist in the rendered hand layer.
// Usage: node tools/character-weapon.mjs <body> <state> [--check]
//   reads  production/source/characters/anim/<body>/<state>.json (weapon/weapons) and <state>/arms.png, body.png
//   writes production/source/characters/anim/<body>/<state>/<slot>-<item>.png per hand and item (rows = spec directions, 128x128)
//          production/source/characters/anim/<body>/<state>/weapon.json (frame size, origin, depth per frame, QC)
// The weapon frame is 128x128 so swings can leave the 64x64 body frame; the body frame's (0, 0) sits at ORIGIN, so the
// character pivot [32, 63] is [64, 95] in the weapon frame.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { readPng, encodePng } from './lib/png.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const FRAME = 64, WF = 128, ORIGIN = [32, 32];
const N4 = [[1, 0], [-1, 0], [0, 1], [0, -1]];
const key = (x, y) => `${x},${y}`;
const unkey = (k) => k.split(',').map(Number);

const [bodyName, state, flag] = process.argv.slice(2);
if (!bodyName || !state) { console.error('Usage: node tools/character-weapon.mjs <body> <state> [--check]'); process.exit(2); }
const animDir = path.join(root, 'production/source/characters/anim', bodyName);
const spec = JSON.parse(fs.readFileSync(path.join(animDir, `${state}.json`), 'utf8'));
const weapons = spec.weapons || (spec.weapon ? [{ slot: 'main', layer: 'arms', ...spec.weapon }] : null);
if (!weapons) { console.error(`${state}.json has no weapon section`); process.exit(2); }
const F = spec.frames, dirs = spec.directions;

// one frame of the weapon in body-frame coordinates: grip [x, y] (pixel centre of the near fist), angle in degrees
// above the facing's horizontal (E: +x is forward), so 0 points straight ahead and 90 straight up
function draw(item, pose) {
  const t = pose.angle * Math.PI / 180, d = [Math.cos(t), -Math.sin(t)], n = [Math.sin(t), Math.cos(t)];
  const gx = pose.grip[0] + 0.5, gy = pose.grip[1] + 0.5, out = new Map();
  const lo = Math.min(...item.segments.map((s) => s.from)), hi = Math.max(...item.segments.map((s) => s.to));
  for (let y = -ORIGIN[1]; y < WF - ORIGIN[1]; y++) for (let x = -ORIGIN[0]; x < WF - ORIGIN[0]; x++) {
    const cx = x + 0.5 - gx, cy = y + 0.5 - gy, u = cx * d[0] + cy * d[1], v = cx * n[0] + cy * n[1];
    if (u < lo || u >= hi) continue;
    // a gap between segments (a hilt hidden inside the fist) draws nothing
    const s = item.segments.find((g) => u >= g.from && u < g.to);
    if (!s) continue;
    const h = s.thickness / 2;
    if (v < -h || v >= h) continue;
    const row = s.pattern[Math.floor(u - s.from) % s.pattern.length];
    out.set(key(x, y), row[Math.min(row.length - 1, Math.floor((v + h) * row.length / s.thickness))]);
  }
  // outline: coloured pixels touching empty space
  for (const [q, c] of [...out]) {
    if (c === '#') continue;
    const [x, y] = unkey(q);
    for (const [dx, dy] of N4) if (!out.has(key(x + dx, y + dy))) out.set(key(x + dx, y + dy), '#');
  }
  return out;
}

const poseOf = (W, dir, k) => {
  const src = W[dir] ? dir : W.mirror?.[dir];
  const p = W[src][k];
  if (src === dir) return p;
  // mirrored facing: grip mirrored in the body frame, angle measured toward the mirrored forward
  return { ...p, grip: [FRAME - 1 - p.grip[0], p.grip[1]], mirrored: true };
};
const handLayers = { arms: readPng(path.join(animDir, state, 'arms.png')), body: readPng(path.join(animDir, state, 'body.png')) };
const qc = { gripOnFist: {}, inFrame: true };
const files = {}, out = [];
// a hand slot may list alternative items (items: [...], the first is the default); each is rendered on the same grips as
// its own sheet <slot>-<item>.png, so the runtime can swap the item without changing the pose
for (const W of weapons.flatMap((w) => (w.items || [w.item]).map((it, i) => ({ ...w, item: it, isDefault: i === 0 })))) {
  const item = JSON.parse(fs.readFileSync(path.join(root, 'production/source/characters/items', `${W.item}.json`), 'utf8'));
  const pal = Object.fromEntries(Object.entries(item.palette).map(([s, h]) => [s, h.slice(1).toLowerCase()]));
  const hand = handLayers[W.layer || 'arms'];
  const sheet = Buffer.alloc(WF * F * WF * dirs.length * 4);
  const z = {};
  dirs.forEach((dir, r) => {
    z[dir] = [];
    for (let k = 0; k < F; k++) {
      const p = poseOf(W, dir, k);
      let m = draw(item, p.mirrored ? { ...p, grip: [FRAME - 1 - p.grip[0], p.grip[1]] } : p);
      if (p.mirrored) m = new Map([...m].map(([q, c]) => { const [x, y] = unkey(q); return [key(FRAME - 1 - x, y), c]; }));
      z[dir].push(p.z);
      // registration: the grip pixel is covered by the hand's layer (the fist closes over the hilt)
      const [gx, gy] = p.grip, ai = ((r * FRAME + gy) * hand.w + k * FRAME + gx) * 4;
      qc.gripOnFist[`${W.slot}/${W.item} ${dir}:${k}`] = hand.px[ai + 3] === 255;
      for (const [q, c] of m) {
        const [x, y] = unkey(q), X = x + ORIGIN[0], Y = y + ORIGIN[1];
        if (X < 0 || Y < 0 || X >= WF || Y >= WF) { qc.inFrame = false; continue; }
        Buffer.from(pal[c] + 'ff', 'hex').copy(sheet, ((r * WF + Y) * WF * F + k * WF + X) * 4);
      }
    }
  });
  const file = `${W.slot}-${W.item}.png`;
  files[file] = encodePng(WF * F, WF * dirs.length, sheet);
  out.push({ slot: W.slot, item: W.item, default: W.isDefault, grip: W.gripKind, hand: W.layer || 'arms', file, status: W.status || spec.status, z,
    grips: Object.fromEntries(dirs.map((d) => [d, Array.from({ length: F }, (_, k) => poseOf(W, d, k).grip)])) });
}
qc.pass = qc.inFrame && Object.values(qc.gripOnFist).every(Boolean);

files['weapon.json'] = JSON.stringify({
  schema: 'astro-fighters-character-weapon-output/v2',
  body: bodyName, state, frameSize: [WF, WF], origin: ORIGIN, pivot: [ORIGIN[0] + 32, ORIGIN[1] + 63],
  rows: dirs, frames: F,
  depthRule: weapons[0].depthRule,
  weapons: out,
  qc
}, null, 2) + '\n';
const outDir = path.join(animDir, state);
if (flag === '--check') {
  const tmp = path.join(outDir, '.check.png');
  const stale = Object.entries(files).filter(([rel, data]) => {
    const file = path.join(outDir, rel);
    if (!fs.existsSync(file)) return true;
    if (!rel.endsWith('.png')) return fs.readFileSync(file, 'utf8') !== data;
    fs.writeFileSync(tmp, data);
    try { return !readPng(file).px.equals(readPng(tmp).px); } finally { fs.rmSync(tmp, { force: true }); }
  });
  if (stale.length) { console.error(`Weapon ${bodyName}/${state} outputs are stale (${stale.map(([r]) => r).join(', ')}); rerun node tools/character-weapon.mjs ${bodyName} ${state}`); process.exit(1); }
  if (!qc.pass) { console.error(`Weapon ${bodyName}/${state} fails QC: ${JSON.stringify(qc)}`); process.exit(1); }
  console.log(`Weapon ${bodyName}/${state} outputs are current and pass QC.`);
} else {
  for (const [rel, data] of Object.entries(files)) fs.writeFileSync(path.join(outDir, rel), data);
  console.log(`Wrote ${Object.keys(files).length} files to ${path.relative(root, outDir)}/`);
  console.log(`QC: ${JSON.stringify(qc)}`);
}
