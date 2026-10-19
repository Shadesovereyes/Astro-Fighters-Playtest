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
  // branch segments (a sickle's blade, a hook): each lies on its own axis that starts at branch.at = [u, v] in the
  // weapon's axis coordinates and turns branch.angle degrees from the weapon axis (positive toward +v, i.e. below the
  // axis in E); from/to run along that branch axis. Main segments have no branch.
  // pose.branchScale foreshortens the branches across the axis (a sickle blade turned toward the viewer shows only its edge)
  // pose.branches overrides branch segments by name ({ <name>: { branch: { at, angle }, to, thickness, pattern } }), so a pose
  // can show a blade turned toward the viewer as its edge folded along the shaft
  const main = item.segments.filter((s) => !s.branch), branches = item.segments.filter((s) => s.branch)
    .map((s) => (pose.branches?.[s.name] ? { ...s, ...pose.branches[s.name], branch: { ...s.branch, ...pose.branches[s.name].branch } } : s));
  const lo = Math.min(...main.map((s) => s.from)), hi = Math.max(...main.map((s) => s.to)), sc = pose.scale ?? 1;
  const paint = (s, u, v) => {
    const h = s.thickness / 2;
    if (v < -h || v >= h) return null;
    const row = s.pattern[Math.floor(u - s.from) % s.pattern.length];
    return row[Math.min(row.length - 1, Math.floor((v + h) * row.length / s.thickness))];
  };
  // chainOnly: the weapon is hidden (its hand is out of sight) but the chain hanging from it shows
  if (!pose.chainOnly) for (let y = -ORIGIN[1]; y < WF - ORIGIN[1]; y++) for (let x = -ORIGIN[0]; x < WF - ORIGIN[0]; x++) {
    // scale foreshortens the weapon's length (a blade pointing toward or away from the viewer), never its thickness
    const cx = x + 0.5 - gx, cy = y + 0.5 - gy, u = (cx * d[0] + cy * d[1]) / sc, v = cx * n[0] + cy * n[1];
    let c = null;
    // a gap between segments (a hilt hidden inside the fist) draws nothing
    if (u >= lo && u < hi) { const s = main.find((g) => u >= g.from && u < g.to); if (s) c = paint(s, u, v); }
    for (const s of branches) {
      if (c) break;
      const b = s.branch, ba = b.angle * Math.PI / 180, du = u - b.at[0], dv = v / (pose.branchScale ?? 1) - b.at[1];
      const bu = du * Math.cos(ba) + dv * Math.sin(ba), bv = -du * Math.sin(ba) + dv * Math.cos(ba);
      if (bu >= s.from && bu < s.to) c = paint(s, bu, bv);
    }
    if (c) out.set(key(x, y), c);
  }
  // chain (a kusarigama's chain and weight): hangs from the point chain.at on the weapon axis in screen space, not along the
  // axis, so it falls with gravity at any blade angle; pose.chain = { to: [dx, dy] weight offset from that point, sag: px
  // the middle bows sideways, z: depth } (default: straight down chain.length px). Links alternate chain.links colours;
  // the weight is the item's weight pattern centred under the chain's end. Both get the same outline as the weapon.
  const chainPx = new Set();
  if (item.chain && !pose.chain?.off) {
    // via (kusarigama held in two hands): the chain droops in a U from the butt (lowest droop px below the lower end),
    // rises into the off hand at via ([x, y] in the frame, the off fist's centre) and hangs from it to the weight; the
    // links inside the off fist (within 1 px of via) are left out so the fist closes over the chain
    const C = item.chain, pc = pose.chain || {};
    const ax = gx + d[0] * C.at * sc, ay = gy + d[1] * C.at * sc;
    const curves = [];
    let sx = ax, sy = ay;
    if (pc.via) {
      const vx = pc.via[0] + 0.5, vy = pc.via[1] + 0.5;
      curves.push([sx, sy, (sx + vx) / 2, Math.max(sy, vy) + 2 * (pc.droop ?? 4), vx, vy]);
      sx = vx; sy = vy;
    }
    const [tx, ty] = pc.to || [0, C.length], bx = sx + tx, by = sy + ty, sag = pc.sag ?? 0;
    curves.push([sx, sy, (sx + bx) / 2 + sag, (sy + by) / 2, bx, by]);
    let n = 0, last = null;
    for (const [x0, y0, x1, y1, x2, y2] of curves) {
      const steps = 4 * Math.ceil(Math.hypot(x2 - x0, y2 - y0) + Math.hypot(x1 - x0, y1 - y0) + 1);
      for (let i = 0; i <= steps; i++) {
        const t = i / steps, x = Math.floor((1 - t) ** 2 * x0 + 2 * (1 - t) * t * x1 + t * t * x2), y = Math.floor((1 - t) ** 2 * y0 + 2 * (1 - t) * t * y1 + t * t * y2);
        const q = key(x, y);
        if (q === last) continue;
        last = q;
        n++;
        if (pc.via && Math.abs(x - pc.via[0]) <= 1 && Math.abs(y - pc.via[1]) <= 1) continue;
        if (!out.has(q)) { out.set(q, C.links[n % C.links.length]); chainPx.add(q); }
      }
    }
    const wx = Math.floor(bx), wy = Math.floor(by), W = C.weight, h = Math.floor(W[0].length / 2);
    W.forEach((row, j) => [...row].forEach((ch, i) => { if (ch === '.') return; const q = key(wx - h + i, wy + 1 + j); out.set(q, ch); chainPx.add(q); }));
  }
  // outline: coloured pixels touching empty space
  for (const [q, c] of [...out]) {
    if (c === '#') continue;
    const [x, y] = unkey(q);
    for (const [dx, dy] of N4) if (!out.has(key(x + dx, y + dy))) { out.set(key(x + dx, y + dy), '#'); if (chainPx.has(q)) chainPx.add(key(x + dx, y + dy)); }
  }
  if (pose.chain?.via) for (const q of [...chainPx]) { const [x, y] = unkey(q); if (Math.abs(x - pose.chain.via[0]) <= 1 && Math.abs(y - pose.chain.via[1]) <= 1) out.delete(q); }
  out.chain = chainPx;
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
// streak: a swing in the plane of the facing seen from the front or back (S, N) projects to a vertical streak at the
// blade's column, from row y0 (start of the swing) to y1 (the blade's end), widest at y1 and tapering to nothing at y0;
// its centre column takes the outermost trail colour and the sides the next ones in
function streakOf(item, pose, weaponPx) {
  const T = pose.trail, cols = item.trail.bands, out = new Map(), x0 = pose.grip[0] + 0.5, W = T.width ?? 4;
  const lo = Math.min(T.y0, T.y1), hi = Math.max(T.y0, T.y1);
  for (let y = Math.floor(lo); y <= Math.ceil(hi); y++) {
    const f = Math.abs(y + 0.5 - T.y0) / Math.max(1, Math.abs(T.y1 - T.y0)), half = Math.max(0.5, (W * Math.min(1, f)) / 2);
    for (let x = Math.floor(x0 - half); x < Math.ceil(x0 + half); x++) {
      if (weaponPx.has(key(x, y))) continue;
      const d = Math.abs(x + 0.5 - x0) * 2;
      out.set(key(x, y), (cols.find((b) => d < b.to) || cols[cols.length - 1]).colour);
    }
  }
  return out;
}
// ellipse: a horizontal swing around the body seen in the cabinet projection. The tip runs on a circle of radius R
// (pixels) in the horizontal plane; depth maps to screen y at k (far side = up). psi is the swing angle in that plane
// (0 = toward the screen +x, +90 = far side); the crescent runs from psi 'from' to 'to', widest at 'to'. Each pixel
// carries its own depth: the near half (sin psi < 0) is drawn over the character, the far half behind it.
function ellipseOf(item, pose, weaponPx) {
  const T = pose.trail, cols = item.trail.bands, out = new Map(), [cx, cy] = T.center, R = T.R, k = T.k ?? 0.5;
  const span = T.to - T.from;
  for (let y = -ORIGIN[1]; y < WF - ORIGIN[1]; y++) for (let x = -ORIGIN[0]; x < WF - ORIGIN[0]; x++) {
    if (weaponPx.has(key(x, y))) continue;
    const u = (x + 0.5 - cx) / R, w = -(y + 0.5 - cy) / (k * R), rho = Math.hypot(u, w);
    if (rho > 1) continue;
    const psi = Math.atan2(w, u) * 180 / Math.PI;
    let rel = ((((psi - T.from) * Math.sign(span)) % 360) + 360) % 360;
    const f = rel / Math.abs(span);
    if (f > 1) continue;
    const depthIn = (1 - rho) * R;
    if (depthIn > (T.width ?? 6) * f) continue;
    const band = cols.find((b) => depthIn < b.to) || cols[cols.length - 1];
    // trail.z overrides the per-pixel depth (e.g. N: the swing runs in front of the body, away from the viewer)
    out.set(key(x, y), [band.colour, T.z || (Math.sin(psi * Math.PI / 180) < 0 ? 'top' : 'behind')]);
  }
  return out;
}
// thrust: a stab's speed lines, drawn parallel to the blade axis (lines: [[v, uFrom, uTo], ...] in the item's axis
// coordinates from the grip, v across the axis, positive below the blade in E). Each line is one pixel wide; its colour
// steps through the item's trail bands from the forward end (uTo) backward, so the line fades toward its tail
function thrustOf(item, pose, weaponPx) {
  const T = pose.trail, cols = item.trail.bands, out = new Map(), ta = pose.angle * Math.PI / 180;
  const ax = [Math.cos(ta), -Math.sin(ta)], nx = [Math.sin(ta), Math.cos(ta)], [gx, gy] = [pose.grip[0] + 0.5, pose.grip[1] + 0.5];
  for (const [v, u0, u1] of T.lines) for (let u = u1; u >= u0; u -= 0.5) {
    const q = key(Math.floor(gx + u * ax[0] + v * nx[0]), Math.floor(gy + u * ax[1] + v * nx[1]));
    if (weaponPx.has(q) || out.has(q)) continue;
    out.set(q, (cols.find((b) => u1 - u < b.to * (T.bandScale ?? 2)) || cols[cols.length - 1]).colour);
  }
  return out;
}
function trailOf(item, pose, weaponPx) {
  if (pose.trail.mode === 'thrust') return thrustOf(item, pose, weaponPx);
  if (pose.trail.mode === 'streak') return streakOf(item, pose, weaponPx);
  if (pose.trail.mode === 'ellipse') return ellipseOf(item, pose, weaponPx);
  // center/radius: a whole swing drawn on one smear frame turns about the swing's pivot (in front of the shoulders),
  // not the end grip, so the crescent follows the blade tip's path; to: the angle the crescent reaches (default the blade)
  // radiusPlus: the radius as the item's own blade length plus a margin, so one key pose serves items of different lengths
  const tipLen = Math.max(...item.segments.map((s) => s.to)) * (pose.scale ?? 1);
  const T = pose.trail, cols = item.trail.bands, R = T.radius ?? (T.radiusPlus != null ? tipLen + T.radiusPlus : tipLen);
  // center 'blade': the pivot sits on the blade's own line, so the crescent ends exactly on the blade at its final angle
  const tipU = Math.max(...item.segments.map((s) => s.to)) * (pose.scale ?? 1), ta = pose.angle * Math.PI / 180;
  const c = T.center === 'blade' ? [pose.grip[0] + (tipU - R) * Math.cos(ta), pose.grip[1] - (tipU - R) * Math.sin(ta)] : T.center || pose.grip;
  const gx = c[0] + 0.5, gy = c[1] + 0.5, a0 = T.from, a1 = T.to ?? pose.angle, span = a1 - a0, out = new Map();
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
  // an itemPoses entry is one override for every frame of that facing, or a per-frame list (null = no override)
  const ip = W.itemPoses?.[W.item]?.[src], ov = Array.isArray(ip) ? ip[k] : ip;
  const p = { ...W[src][k], ...(ov || {}) };
  if (src === dir) return p;
  // mirrored facing: grip mirrored in the body frame, angle measured toward the mirrored forward
  return { ...p, grip: [FRAME - 1 - p.grip[0], p.grip[1]], mirrored: true };
};
const handLayers = { arms: readPng(path.join(animDir, state, 'arms.png')), body: readPng(path.join(animDir, state, 'body.png')) };
// arm-weapon-mask.png (character-posed helper): band-arm pixels in the body layer that a held blade is drawn over
const maskFile = path.join(animDir, state, 'arm-weapon-mask.png'), armMask = fs.existsSync(maskFile) ? readPng(maskFile) : null;
// clothing layers (every animation layer but the body, arms, hair and eyes) cover a masked arm where they overlap it
const clothing = armMask ? Object.entries(JSON.parse(fs.readFileSync(path.join(animDir, state, 'animation.json'), 'utf8')).layers)
  .filter(([n]) => !['body', 'arms'].includes(n) && !/-(hair|eyes)$/.test(n)).map(([, f]) => readPng(path.join(animDir, state, f))) : [];
const qc = { gripOnFist: {}, inFrame: true };
const files = {}, out = [];
// a hand slot may list alternative items (items: [...], the first is the default); each is rendered on the same grips as
// its own sheet <slot>-<item>.png, so the runtime can swap the item without changing the pose
for (const W of weapons.flatMap((w) => (w.items || [w.item]).map((it, i) => ({ ...w, item: it, isDefault: i === 0 })))) {
  const item = JSON.parse(fs.readFileSync(path.join(root, 'production/source/characters/items', `${W.item}.json`), 'utf8'));
  const pal = Object.fromEntries(Object.entries(item.palette).map(([s, h]) => [s, h.slice(1).toLowerCase()]));
  const sheets = Object.fromEntries(DEPTHS.map((dd) => [dd, Buffer.alloc(WF * F * WF * dirs.length * 4)])), used = new Set();
  // trail sheets per depth: top (over every character layer) or behind (a swing in front of a back-facing body)
  const trailSheets = { top: Buffer.alloc(WF * F * WF * dirs.length * 4), behind: Buffer.alloc(WF * F * WF * dirs.length * 4) }, trailUsed = new Set();
  const z = {};
  dirs.forEach((dir, r) => {
    z[dir] = [];
    for (let k = 0; k < F; k++) {
      const p = poseOf(W, dir, k);
      // omit: the weapon is not drawn (N: a hand hidden in front of the body on the far side of the torso, so the blade
      // would show detached from the visible arm); its smear, if any, is still drawn
      const raw = p.omit ? Object.assign(new Map(), { u: () => 0 }) : draw(item, p.mirrored ? { ...p, grip: [FRAME - 1 - p.grip[0], p.grip[1]] } : p);
      let m = new Map([...raw].map(([q, c]) => [q, [c, raw.chain?.has(q) ? (p.chain?.z ?? depthOf(p.z, -1)) : depthOf(p.z, raw.u(q))]]));
      // a mirrored facing draws the source facing's trail and mirrors its pixels, like the weapon
      let tr = p.trail ? trailOf(item, p.mirrored ? { ...p, grip: [FRAME - 1 - p.grip[0], p.grip[1]] } : p, raw) : new Map();
      if (p.mirrored) {
        m = new Map([...m].map(([q, c]) => { const [x, y] = unkey(q); return [key(FRAME - 1 - x, y), c]; }));
        tr = new Map([...tr].map(([q, c]) => { const [x, y] = unkey(q); return [key(FRAME - 1 - x, y), c]; }));
      }
      for (const [q, c] of tr) {
        const [x, y] = unkey(q), X = x + ORIGIN[0], Y = y + ORIGIN[1];
        // clipBody: the smear is drawn only outside the character's silhouette (a streak seen head-on would otherwise
        // stripe the face and torso)
        if (p.trail.clipBody && x >= 0 && y >= 0 && x < FRAME && y < FRAME
          && ['body', 'arms'].some((n) => handLayers[n].px[((r * FRAME + y) * handLayers[n].w + k * FRAME + x) * 4 + 3] === 255)) continue;
        if (X < 0 || Y < 0 || X >= WF || Y >= WF) { qc.inFrame = false; continue; }
        const [col, td] = Array.isArray(c) ? c : [c, p.trail.z || 'top'];
        Buffer.from(col.slice(1).toLowerCase() + 'ff', 'hex').copy(trailSheets[td], ((r * WF + Y) * WF * F + k * WF + X) * 4);
        trailUsed.add(td);
      }
      z[dir].push(p.z);
      // registration: the grip pixel is covered by the hand's layer (the fist closes over the hilt)
      // a pose may name its own hand layer (in S both hands are on the arms layer) or mark the hand hidden (N: the hands
      // are in front of the body, so only the weapon parts that clear the body show and there is no fist to register to)
      const hl = handLayers[p.layer || W.layer || 'arms'], [gx, gy] = p.grip, ai = ((r * FRAME + gy) * hl.w + k * FRAME + gx) * 4;
      qc.gripOnFist[`${W.slot}/${W.item} ${dir}:${k}`] = p.hidden ? 'hidden' : hl.px[ai + 3] === 255;
      for (const [q, [c, dd]] of m) {
        const [x, y] = unkey(q), X = x + ORIGIN[0], Y = y + ORIGIN[1];
        // aboveArm: over the arm holding it (a blade never goes under that arm) but still covered by the torso: drawn in
        // the top sheet except where the body layer shows and neither the arms layer nor the posed arm mask does
        let ds = dd;
        if (dd === 'aboveArm') {
          ds = 'top';
          const op = (n) => x >= 0 && y >= 0 && x < FRAME && y < FRAME && handLayers[n].px[((r * FRAME + y) * handLayers[n].w + k * FRAME + x) * 4 + 3] === 255;
          const at = (img) => x >= 0 && y >= 0 && x < FRAME && y < FRAME && img.px[((r * FRAME + y) * img.w + k * FRAME + x) * 4 + 3] === 255;
          const armHere = armMask && at(armMask) && !clothing.some(at);
          if (op('body') && !op('arms') && !armHere) continue;
        } else if (!DEPTHS.includes(dd)) throw new Error(`${W.slot}/${W.item} ${dir}:${k}: unknown depth ${dd}`);
        if (X < 0 || Y < 0 || X >= WF || Y >= WF) { qc.inFrame = false; continue; }
        Buffer.from(pal[c] + 'ff', 'hex').copy(sheets[ds], ((r * WF + Y) * WF * F + k * WF + X) * 4);
        used.add(ds);
      }
    }
  });
  // one sheet per depth slot the weapon uses: <slot>-<item>-<depth>.png
  const layers = {};
  for (const dd of DEPTHS.filter((x) => used.has(x))) { layers[dd] = `${W.slot}-${W.item}-${dd}.png`; files[layers[dd]] = encodePng(WF * F, WF * dirs.length, sheets[dd]); }
  // the swing smear is its own FX sheet (drawn over every character layer): <slot>-<item>-trail.png
  if (trailUsed.has('top')) { layers.trail = `${W.slot}-${W.item}-trail.png`; files[layers.trail] = encodePng(WF * F, WF * dirs.length, trailSheets.top); }
  if (trailUsed.has('behind')) { layers.trailBehind = `${W.slot}-${W.item}-trail-behind.png`; files[layers.trailBehind] = encodePng(WF * F, WF * dirs.length, trailSheets.behind); }
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
