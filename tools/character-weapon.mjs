// Deterministic weapon-layer renderer: draws rigid weapon items (production/source/characters/items/<item>.json) as
// authored bands along their axes, placed per frame at the grip points authored in the state spec (spec.weapons, one
// entry per hand: slot main = near hand on the arms layer, slot off = far hand on the body layer; spec.weapon is the
// single main-hand form), and checks each grip registers with its fist in the rendered hand layer.
// Usage: node tools/character-weapon.mjs <body> <state> [--check]
//   reads  production/source/characters/anim/<body>/<state>.json (weapon/weapons) and <state>/arms.png, body.png
//   writes production/source/characters/anim/<body>/<state>/<slot>-<item>-<depth>.png per hand, item and depth slot (rows = spec directions, 128x128)
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

// one frame of the weapon in body-frame coordinates: grip [x, y] (pixel centre of the fist), angle in degrees above the
// screen's +x axis (in E that is forward), so 0 points right/ahead and 90 straight up; scale foreshortens the length
function draw(item, pose) {
  const t = pose.angle * Math.PI / 180, d = [Math.cos(t), -Math.sin(t)], n = [Math.sin(t), Math.cos(t)];
  const gx = pose.grip[0] + 0.5, gy = pose.grip[1] + 0.5, out = new Map();
  const lo = Math.min(...item.segments.map((s) => s.from)), hi = Math.max(...item.segments.map((s) => s.to));
  for (let y = -ORIGIN[1]; y < WF - ORIGIN[1]; y++) for (let x = -ORIGIN[0]; x < WF - ORIGIN[0]; x++) {
    // scale foreshortens the weapon's length (a blade pointing toward or away from the viewer), never its thickness
    const cx = x + 0.5 - gx, cy = y + 0.5 - gy, u = (cx * d[0] + cy * d[1]) / (pose.scale ?? 1), v = cx * n[0] + cy * n[1];
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
  // u of every pixel (outline included), so a pose can split the weapon at the grip into two depths
  out.u = (q) => { const [x, y] = unkey(q), cx = x + 0.5 - gx, cy = y + 0.5 - gy; return (cx * d[0] + cy * d[1]) / (pose.scale ?? 1); };
  return out;
}
// depth slots, back to front: behind (under the body), front (over body and clothing, under the arms), top (over every
// character layer: a blade pointing at the viewer, or a hand held in front of the head). A pose's z is one slot, or
// { hilt, blade } to split the weapon at the grip (hilt = the pommel side, u < 0)
const DEPTHS = ['behind', 'front', 'top'];

// swing smear (pose.trail = { from: <blade angle the swing started at>, width }): a hard-edged pixel-art crescent swept
// around the grip from the start angle to the current blade angle, out to the blade tip; it is widest at the current
// blade and tapers to nothing at the start, banded from the tip inward with the item's trail colours. Pixels under the
// weapon itself are left to the weapon. It is FX, drawn over every character layer as its own sheet.
function trailOf(item, pose, weaponPx) {
  // center/radius: a whole swing drawn on one smear frame turns about the swing's pivot (in front of the shoulders),
  // not the end grip, so the crescent follows the blade tip's path; to: the angle the crescent reaches (default the blade)
  const T = pose.trail, cols = item.trail.bands, R = T.radius ?? Math.max(...item.segments.map((s) => s.to)) * (pose.scale ?? 1);
  const c = T.center || pose.grip, gx = c[0] + 0.5, gy = c[1] + 0.5, a0 = T.from, a1 = T.to ?? pose.angle, span = a1 - a0, out = new Map();
  for (let y = -ORIGIN[1]; y < WF - ORIGIN[1]; y++) for (let x = -ORIGIN[0]; x < WF - ORIGIN[0]; x++) {
    if (weaponPx.has(key(x, y))) continue;
    const dx = x + 0.5 - gx, dy = y + 0.5 - gy, r = Math.hypot(dx, dy);
    if (r > R) continue;
    let phi = Math.atan2(-dy, dx) * 180 / Math.PI;
    // angle measured from the start of the swing in the swing's direction
    let rel = (phi - a0) * Math.sign(span);
    rel = ((rel % 360) + 360) % 360;
    const f = rel / Math.abs(span);
    if (f > 1) continue;
    const inner = R - (T.width ?? 6) * f;
    if (r < inner) continue;
    const depthIn = R - r;
    const band = cols.find((b) => depthIn < b.to) || cols[cols.length - 1];
    out.set(key(x, y), band.colour);
  }
  // the tapered start can leave single detached pixels: drop trail pixels with no 4-neighbour in the trail
  for (const q of [...out.keys()]) { const [x, y] = unkey(q); if (!N4.some(([dx, dy]) => out.has(key(x + dx, y + dy)))) out.delete(q); }
  return out;
}
const depthOf = (z, u) => (typeof z === 'string' ? z : u < 0 ? z.hilt : z.blade);

// itemPoses: per-item overrides of a slot's poses ({ <item>: { <dir>: { field: value } } }), so alternative items in one
// hand (wakizashi or tanto) can hold their blades at different angles on the same grip
const poseOf = (W, dir, k) => {
  const src = W[dir] ? dir : W.mirror?.[dir];
  const p = { ...W[src][k], ...(W.itemPoses?.[W.item]?.[src] || {}) };
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
  const sheets = Object.fromEntries(DEPTHS.map((dd) => [dd, Buffer.alloc(WF * F * WF * dirs.length * 4)])), used = new Set();
  const trailSheet = Buffer.alloc(WF * F * WF * dirs.length * 4);
  let trailUsed = false;
  const z = {};
  dirs.forEach((dir, r) => {
    z[dir] = [];
    for (let k = 0; k < F; k++) {
      const p = poseOf(W, dir, k);
      const raw = draw(item, p.mirrored ? { ...p, grip: [FRAME - 1 - p.grip[0], p.grip[1]] } : p);
      let m = new Map([...raw].map(([q, c]) => [q, [c, depthOf(p.z, raw.u(q))]]));
      let tr = p.trail ? trailOf(item, p.mirrored ? { ...p, grip: [FRAME - 1 - p.grip[0], p.grip[1]], trail: { ...p.trail, ...(p.trail.center ? { center: [FRAME - 1 - p.trail.center[0], p.trail.center[1]] } : {}) } } : p, raw) : new Map();
      if (p.mirrored) {
        m = new Map([...m].map(([q, c]) => { const [x, y] = unkey(q); return [key(FRAME - 1 - x, y), c]; }));
        tr = new Map([...tr].map(([q, c]) => { const [x, y] = unkey(q); return [key(FRAME - 1 - x, y), c]; }));
      }
      for (const [q, c] of tr) {
        const [x, y] = unkey(q), X = x + ORIGIN[0], Y = y + ORIGIN[1];
        if (X < 0 || Y < 0 || X >= WF || Y >= WF) { qc.inFrame = false; continue; }
        Buffer.from(c.slice(1).toLowerCase() + 'ff', 'hex').copy(trailSheet, ((r * WF + Y) * WF * F + k * WF + X) * 4);
        trailUsed = true;
      }
      z[dir].push(p.z);
      // registration: the grip pixel is covered by the hand's layer (the fist closes over the hilt)
      // a pose may name its own hand layer (in S both hands are on the arms layer) or mark the hand hidden (N: the hands
      // are in front of the body, so only the weapon parts that clear the body show and there is no fist to register to)
      const hl = handLayers[p.layer || W.layer || 'arms'], [gx, gy] = p.grip, ai = ((r * FRAME + gy) * hl.w + k * FRAME + gx) * 4;
      qc.gripOnFist[`${W.slot}/${W.item} ${dir}:${k}`] = p.hidden ? 'hidden' : hl.px[ai + 3] === 255;
      for (const [q, [c, dd]] of m) {
        const [x, y] = unkey(q), X = x + ORIGIN[0], Y = y + ORIGIN[1];
        if (!DEPTHS.includes(dd)) throw new Error(`${W.slot}/${W.item} ${dir}:${k}: unknown depth ${dd}`);
        if (X < 0 || Y < 0 || X >= WF || Y >= WF) { qc.inFrame = false; continue; }
        Buffer.from(pal[c] + 'ff', 'hex').copy(sheets[dd], ((r * WF + Y) * WF * F + k * WF + X) * 4);
        used.add(dd);
      }
    }
  });
  // one sheet per depth slot the weapon uses: <slot>-<item>-<depth>.png
  const layers = {};
  for (const dd of DEPTHS.filter((x) => used.has(x))) { layers[dd] = `${W.slot}-${W.item}-${dd}.png`; files[layers[dd]] = encodePng(WF * F, WF * dirs.length, sheets[dd]); }
  // the swing smear is its own FX sheet (drawn over every character layer): <slot>-<item>-trail.png
  if (trailUsed) { layers.trail = `${W.slot}-${W.item}-trail.png`; files[layers.trail] = encodePng(WF * F, WF * dirs.length, trailSheet); }
  out.push({ slot: W.slot, item: W.item, default: W.isDefault, grip: W.gripKind, hand: W.layer || 'arms', layers, status: W.status || spec.status, z,
    grips: Object.fromEntries(dirs.map((d) => [d, Array.from({ length: F }, (_, k) => poseOf(W, d, k).grip)])) });
}
qc.pass = qc.inFrame && Object.values(qc.gripOnFist).every((v) => v === true || v === 'hidden');

files['weapon.json'] = JSON.stringify({
  schema: 'astro-fighters-character-weapon-output/v2',
  body: bodyName, state, frameSize: [WF, WF], origin: ORIGIN, pivot: [ORIGIN[0] + 32, ORIGIN[1] + 63],
  rows: dirs, frames: F,
  depthRule: 'each weapon is split into depth slots, one sheet each: behind = under the body; front = over body and clothing, under the arms (the fists close over the hilt); top = over every character layer (a blade pointing at the viewer, a hand in front of the head). z per frame is one slot or { hilt, blade } split at the grip',
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
