// Deterministic posed-animation renderer: builds authored leg and arm poses (data specs) on top of the
// locked reference sheets. Reference pixels are reused unchanged (body, arm rows, wrap+foot block, hair,
// eyes); new pixels come only from the spec (row patterns, foot variants, fills) and the outline rules.
// Usage: node tools/character-posed.mjs <body> <state> [--check]
//   reads  production/source/characters/anim/<body>/<state>.json
//   writes production/source/characters/anim/<body>/<state>/<layer>.png  (rows = spec directions, columns = frames)
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
// The near side of each profile: E shows the character's right side, W its left.
const NEAR = { E: { leg: ['R-thigh', 'R-shin-foot'], arm: ['R-upper-arm', 'R-forearm-hand'] } };
const LEG_PARTS = ['R-thigh', 'R-shin-foot', 'L-thigh', 'L-shin-foot'];
const N4 = [[1, 0], [-1, 0], [0, 1], [0, -1]];
const LIMB = { 'R-thigh': ['leg', 'R'], 'R-shin-foot': ['leg', 'R'], 'L-thigh': ['leg', 'L'], 'L-shin-foot': ['leg', 'L'],
  'R-upper-arm': ['arm', 'R'], 'R-forearm-hand': ['arm', 'R'], 'L-upper-arm': ['arm', 'L'], 'L-forearm-hand': ['arm', 'L'] };

const [bodyName, state, flag] = process.argv.slice(2);
if (!bodyName || !state) { console.error('Usage: node tools/character-posed.mjs <body> <state> [--check]'); process.exit(2); }
const rigDir = path.join(root, 'production/source/characters/rig', bodyName);
const animDir = path.join(root, 'production/source/characters/anim', bodyName);
const spec = JSON.parse(fs.readFileSync(path.join(animDir, `${state}.json`), 'utf8'));
const rig = JSON.parse(fs.readFileSync(path.join(rigDir, 'rig.json'), 'utf8'));
const overlays = JSON.parse(fs.readFileSync(path.join(rigDir, 'overlays.json'), 'utf8'));
const order = rig.frameOrder;
const F = spec.frames;
if (F > 16) throw new Error('Animations are capped at 16 frames');
for (const [name, list] of [['bob', spec.bob.dy], ['legs.near', spec.legs.near], ['legs.far', spec.legs.far], ['arms.near', spec.arms.near], ['arms.far', spec.arms.far],
  ...Object.entries(spec.rootMotion).filter(([k]) => k !== 'rule')]) {
  if (list.length !== F) throw new Error(`${name} has ${list.length} entries; spec has ${F} frames`);
}

// Pixel maps are Map<"x,y", value>. Colour values are 6-digit hex; generated outline is tagged so cleanup only
// ever touches pixels this tool added.
const BLACK = '000000', GEN = 'gen';
const key = (x, y) => `${x},${y}`;
const unkey = (k) => k.split(',').map(Number);
const pal = Object.fromEntries(Object.entries(spec.palette).map(([s, h]) => [s, h.slice(1).toLowerCase()]));
const symOf = Object.fromEntries(Object.entries(pal).map(([s, h]) => [h, s]));
const colourOf = (s) => (s === 'o' ? GEN : pal[s]);
const farShade = { ...spec.farShade.map, o: 'o' };
const coloured = (v) => v !== undefined && v !== GEN && v !== BLACK;
// Python-compatible rounding (half to even), so the spec renders exactly as approved.
const roundHalfEven = (v) => { const f = Math.floor(v), d = v - f; return d > 0.5 ? f + 1 : d < 0.5 ? f : (f % 2 === 0 ? f : f + 1); };

const colourToPart = new Map();
for (const [p, hex] of Object.entries(rig.partColours)) colourToPart.set(hex.slice(1), p);
for (const [p, info] of Object.entries(overlays.overlayParts || {})) colourToPart.set(info.colour.slice(1), p);
const hexAt = (img, x, y) => img.px.toString('hex', (y * img.w + x) * 4, (y * img.w + x) * 4 + 3);
const opaque = (img, x, y) => img.px[(y * img.w + x) * 4 + 3] === 255;

const src = order.indexOf(spec.sourceDirection);
const body = readPng(path.join(root, BODY_SHEETS[bodyName].body));
const arms = readPng(path.join(root, BODY_SHEETS[bodyName].arms));
const partMap = readPng(path.join(rigDir, 'part-map.png'));
const ox = src * FRAME;
const bodyPart = (x, y) => (opaque(body, ox + x, y) ? colourToPart.get(hexAt(partMap, ox + x, y)) : undefined);
const sym = (img, x, y) => { const h = hexAt(img, ox + x, y), s = symOf[h]; if (!s) throw new Error(`colour #${h} at ${x},${y} is not in the spec palette`); return s; };
const nearSide = NEAR[spec.sourceDirection];

// ---- legs -------------------------------------------------------------------------------------------
const L = spec.legs;
const ankleBlock = [];
for (let y = 56; y < FRAME; y++) for (let x = 0; x < FRAME; x++) if (bodyPart(x, y) === nearSide.leg[1]) ankleBlock.push([x, y, sym(body, x, y)]);
const ankleX = Math.min(...ankleBlock.filter(([, y, c]) => y === 56 && c !== '#').map(([x]) => x));

function thigh(out, p) {
  for (let y = p.hipRow; y <= p.kneeRow; y++) {
    const t = (y - p.hipRow) / Math.max(1, p.kneeRow - p.hipRow);
    const x0 = roundHalfEven(p.hipX + (p.kneeX - p.hipX) * t);
    const pat = L.thighRows[Math.min(3, Math.floor((y - p.hipRow) * 4 / (p.kneeRow - p.hipRow + 1)))];
    [...pat].forEach((c, j) => out.set(key(x0 + j, y), c));
  }
}
const shinPattern = (i) => (i < 3 ? L.shinRows4[Math.min(2, i)] : L.shinRow3);
function closeLeg(out, skipRefOutline) {
  for (const [k, c] of [...out]) {
    if (skipRefOutline && c === '#') continue;
    const [x, y] = unkey(k);
    for (const [dx, dy] of N4) if (!out.has(key(x + dx, y + dy))) out.set(key(x + dx, y + dy), 'o');
  }
}
function pinchFill(out) {
  const pts = [...out.keys()].map(unkey), xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
  const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
  for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
    if (out.has(key(x, y))) continue;
    if ((out.has(key(x - 1, y)) && out.has(key(x + 1, y))) || (out.has(key(x, y - 1)) && out.has(key(x, y + 1)))) out.set(key(x, y), 'o');
  }
}
function buildLeg(p) {
  const out = new Map();
  thigh(out, p);
  if (p.construction === 'reference-ankle') {
    const spans = [];
    for (let y = p.kneeRow + 1; y < p.wrapRow; y++) spans.push(y);
    spans.forEach((y, i) => {
      const t = (i + 1) / spans.length, x0 = roundHalfEven(p.kneeX + (p.ankleX - p.kneeX) * t);
      [...shinPattern(i)].forEach((c, j) => out.set(key(x0 + j, y), c));
      if (i === 0) out.set(key(x0, y), 'D');
    });
    const dx = p.ankleX - ankleX, dy = p.wrapRow - 56;
    for (const [x, y, c] of ankleBlock) if (c !== '#') out.set(key(x + dx, y + dy), c);
    out.set(key(p.ankleX, 59 + dy), 'd'); out.set(key(p.ankleX + 1, 59 + dy), 'm');
    closeLeg(out, false);
    for (const [x, y, c] of ankleBlock) if (c === '#' && !out.has(key(x + dx, y + dy))) out.set(key(x + dx, y + dy), '#');
  } else if (p.construction === 'line') {
    const bot = p.wrapRow + 2;
    for (let y = p.kneeRow + 1, i = 0; y <= bot; y++, i++) {
      const x0 = roundHalfEven(p.kneeX + (p.footX - p.kneeX) * (y - p.kneeRow) / (bot - p.kneeRow));
      [...(y >= p.wrapRow ? L.wrap : shinPattern(i))].forEach((c, j) => out.set(key(x0 + j, y), c));
      if (i === 0) out.set(key(x0, y), 'D');
    }
    const ft = L.feet[p.foot];   // ft.dx moves the foot's column 0 sideways (a foot pointing back starts left of the ankle)
    ft.rows.forEach((row, r) => [...row].forEach((c, j) => { if (c !== '.') out.set(key(p.footX - 1 + (ft.dx || 0) + j, bot + 1 + r), c); }));
    closeLeg(out, true);
  } else if (p.construction === 'band') {
    // Like 'line', but thigh and shin are bands of constant thickness measured across the limb, not row spans of
    // fixed width, so a leg keeps its thickness at any angle. Each band runs along the limb's centre line (hip joint
    // to knee to ankle; the 'line' poses' back-edge coordinates plus half the limb width) and a pixel takes the colour
    // of its row pattern read back to front across the band. The knee is a round joint the width of the shin, so the
    // bend closes without a bump.
    out.clear();
    if (p.ankle) return kickLeg(p, out);
    const bot = p.wrapRow + 2;
    const band = (ax, ay, bx, by) => {
      const len = Math.hypot(bx - ax, by - ay), d = [(bx - ax) / len, (by - ay) / len], n = [d[1], -d[0]];
      return { len, uv: (x, y) => { const cx = x + 0.5 - ax, cy = y + 0.5 - ay; return [cx * d[0] + cy * d[1], cx * n[0] + cy * n[1]]; } };
    };
    const kx = p.kneeX + 2.5, ky = p.kneeRow + 0.5;
    const th = band(p.hipX + 2.5, p.hipRow + 0.5, kx, ky), sh = band(p.kneeX + 2, ky, p.footX + 1.5, bot + 0.5);
    // the wrap is cut by rows (wrapRow to the last shin row), as in 'line', so it reads as a level band at the ankle
    const shinPat = (u, y) => (y >= p.wrapRow ? L.wrap : u < 3 ? L.shinRows4[Math.max(0, Math.min(2, Math.floor(u)))] : L.shinRow3);
    const pick = (pat, v) => pat[Math.max(0, Math.min(pat.length - 1, Math.floor(v + pat.length / 2)))];
    for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
      const [su, sv] = sh.uv(x, y), [tu, tv] = th.uv(x, y);
      const sp = shinPat(su, y), inShin = y <= bot && su >= 0 && su <= sh.len + 1.5 && Math.abs(sv + 0.5 - 0.5) <= sp.length / 2 && sv >= -sp.length / 2 && sv < sp.length / 2;
      const inThigh = tu >= -2 && tu <= th.len && tv >= -2.5 && tv < 2.5;
      const inKnee = Math.hypot(x + 0.5 - kx + 0.25, y + 0.5 - ky) <= 2.3;
      if (inThigh) out.set(key(x, y), pick(L.thighRows[Math.max(0, Math.min(3, Math.floor(tu * 4 / th.len)))], tv));
      else if (inShin) out.set(key(x, y), pick(sp, sv));
      else if (inKnee) out.set(key(x, y), pick(L.shinRows4[0], sv));
    }
    // the foot hangs under the wrap; where the slanted wrap end overlaps it, the wrap stays on top
    const ft = L.feet[p.foot];
    ft.rows.forEach((row, r) => [...row].forEach((c, j) => { const q = key(p.footX - 1 + (ft.dx || 0) + j, bot + 1 + r); if (c !== '.' && !out.has(q)) out.set(q, c); }));
    closeLeg(out, true);
  } else throw new Error(`unknown leg construction ${p.construction}`);
  pinchFill(out);
  return out;
}
// kick leg: a band leg whose shin ends at an explicit ankle point (any angle, e.g. horizontal in a kick), not on a
// wrap row. The wrap is the last wrapLen px along the shin (cut across the limb, not by rows) and the authored foot
// is placed with its anchor cell on the ankle point. out.limb keeps the geometry so garments can be drawn along it.
function kickLeg(p, out) {
  const band = (ax, ay, bx, by) => {
    const len = Math.hypot(bx - ax, by - ay), d = [(bx - ax) / len, (by - ay) / len], n = [d[1], -d[0]];
    return { len, uv: (x, y) => { const cx = x + 0.5 - ax, cy = y + 0.5 - ay; return [cx * d[0] + cy * d[1], cx * n[0] + cy * n[1]]; } };
  };
  // the shin's front (L) side faces the band's normal; a leg pointing right has its front up, pointing left down
  const kx = p.kneeX + 0.5, ky = p.kneeRow + 0.5, ax = p.ankle[0] + 0.5, ay = p.ankle[1] + 0.5;
  const th = band(p.hipX + 0.5, p.hipRow + 0.5, kx, ky), sh = band(kx, ky, ax, ay);
  // section: a front/back view's own cross-sections (read from its reference legs, lit in the centre) instead of the
  // profile rows; shin patterns apply from their 'from' distance along the shin
  const SC = p.section ? L.sections[p.section] : null, wrapLen = p.wrapLen ?? (SC ? SC.wrapLen : 3);
  const thighPat = (tu) => (SC ? SC.thigh : L.thighRows[Math.max(0, Math.min(3, Math.floor(tu * 4 / th.len)))]);
  const shinPatOf = (su, wrap) => {
    if (SC) return wrap ? SC.wrap : (SC.shin.filter((e) => su >= e.from).pop() || SC.shin[0]).rows;
    return wrap ? L.wrap : su < 3 ? L.shinRows4[Math.max(0, Math.min(2, Math.floor(su)))] : L.shinRow3;
  };
  const pick = (pat, v) => pat[Math.max(0, Math.min(pat.length - 1, Math.floor(v + pat.length / 2)))];
  const seg = new Map();
  for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
    const [su, sv] = sh.uv(x, y), [tu, tv] = th.uv(x, y);
    const wrap = su >= sh.len - wrapLen, sp = shinPatOf(su, wrap);
    const inShin = su >= 0 && su <= sh.len && sv >= -sp.length / 2 && sv < sp.length / 2;
    const tp = thighPat(tu), inThigh = tu >= -2 && tu <= th.len && tv >= -tp.length / 2 && tv < tp.length / 2;
    const inKnee = Math.hypot(x + 0.5 - kx, y + 0.5 - ky) <= 2.3;
    if (inThigh) { out.set(key(x, y), pick(tp, tv)); seg.set(key(x, y), 'thigh'); }
    else if (inShin) { out.set(key(x, y), pick(sp, sv)); seg.set(key(x, y), wrap ? 'wrap' : 'shin'); }
    else if (inKnee) { out.set(key(x, y), pick(SC ? SC.shin[0].rows : L.shinRows4[0], sv)); seg.set(key(x, y), 'knee'); }
  }
  const ft = L.feet[p.foot];
  if (!ft.anchor) throw new Error(`kick foot ${p.foot} needs an anchor`);
  ft.rows.forEach((row, r) => [...row].forEach((c, j) => {
    const q = key(p.ankle[0] + 1 + j - ft.anchor[0], p.ankle[1] + r - ft.anchor[1]);
    if (c !== '.' && !out.has(q)) { out.set(q, c); seg.set(q, 'foot'); }
  }));
  closeLeg(out, true);
  pinchFill(out);
  out.limb = { th, sh, kx, ky, wrapLen, seg, section: p.section, crease: !!p.crease, hip: [p.hipX + 0.5, p.hipRow + 0.5], ankle: [ax, ay] };
  return out;
}
const legPoses = L.poses.map(buildLeg);

// ---- arms -------------------------------------------------------------------------------------------
const A = spec.arms, AR = A.rows;
const refArm = new Map();
for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) if (opaque(arms, ox + x, y)) refArm.set(key(x, y), sym(arms, x, y));
const armRows = [...new Set([...refArm.keys()].map((k) => unkey(k)[1]))];
const refBack = {};
for (const y of armRows) refBack[y] = Math.min(...[...refArm.keys()].map(unkey).filter((p) => p[1] === y).map((p) => p[0]));
function armShift(p) {
  if (p.construction === 'reference' || p.construction === 'band') return () => 0;
  if (p.construction === 'pendulum') return (y) => roundHalfEven(p.total * (Math.min(y, AR.pendulumRigidFrom) - AR.shoulder) / (AR.pendulumRigidFrom - AR.shoulder));
  // straight: the whole arm, hand included, on one line from the shoulder (no rigid forearm or wrist); a raised arm
  // drops rows between the shoulder and the wrist wrap so it keeps its length while it angles away
  if (p.construction === 'straight') {
    const row = armRow(p), bottom = row(Math.max(...armRows));
    return (y) => { const ny = row(y); return ny === null || ny <= AR.shoulder ? 0 : roundHalfEven(p.total * (ny - AR.shoulder) / (bottom - AR.shoulder)); };
  }
  if (p.construction === 'line') {
    const e = (y) => (y <= AR.elbow ? refBack[AR.shoulder] + p.upper * (y - AR.shoulder) / (AR.elbow - AR.shoulder)
      : refBack[AR.shoulder] + p.upper + p.lean * (y - AR.elbow) / (AR.lineHand - AR.elbow));
    return (y) => { const yy = Math.max(AR.shoulder, Math.min(y, AR.lineHand)); return Math.floor(e(yy) + 0.5) - refBack[yy]; };
  }
  throw new Error(`unknown arm construction ${p.construction}`);
}
// Rows of a raised arm: 'drop' rows, evenly spaced between the shoulder row and the wrist wrap (pendulumRigidFrom),
// are removed and every row below moves up; other constructions keep every row.
function armRow(p) {
  const n = p.drop || 0;
  if (!n) return (y) => y;
  const lo = AR.shoulder + 1, span = AR.pendulumRigidFrom - lo;
  if (n >= span) throw new Error(`arm drop ${n} leaves no upper arm`);
  const dropped = Array.from({ length: n }, (_, i) => lo + Math.floor((i + 0.5) * span / n));
  return (y) => (dropped.includes(y) ? null : y - dropped.filter((r) => r < y).length);
}
// band: an authored raised arm. The arm is a straight band of constant thickness from the shoulder pivot at `angle`
// degrees behind vertical; each pixel takes its colour from the authored cross-section pattern of its segment (upper
// arm and forearm, wrist wrap, hand, hand end), read back-to-front across the band, so the arm keeps its thickness at
// any angle. bandRef maps a band pixel to the reference arm pixel at the same distance along and across the arm
// (used only to place arm accessories).
function bandGeom(p) {
  const B = { ...A.band, ...(p.band || {}) }, t = p.angle * Math.PI / 180, d = [-Math.sin(t), Math.cos(t)], n = [Math.cos(t), Math.sin(t)];
  const uv = (x, y) => { const cx = x + 0.5 - B.pivot[0], cy = y + 0.5 - B.pivot[1]; return [cx * d[0] + cy * d[1], cx * n[0] + cy * n[1]]; };
  return { B, uv };
}
function bandArm(p) {
  const { B, uv } = bandGeom(p), out = new Map(), ref = new Map(), half = B.thickness / 2, end = B.start + B.length;
  // elbow: a bent arm is two bands, the upper arm (p.angle, to elbow.at along the arm) and the forearm (elbow.angle)
  // from the elbow point, joined by a round elbow; the forearm carries the wrap and the fist
  const E = p.elbow, eu = E ? E.at : Infinity;
  const fore = E && (() => {
    const t1 = p.angle * Math.PI / 180, ex = B.pivot[0] - Math.sin(t1) * eu, ey = B.pivot[1] + Math.cos(t1) * eu;
    const g = bandGeom({ angle: E.angle, band: { ...(p.band || {}), pivot: [ex, ey] } });
    return { uv: (x, y) => { const [u, v] = g.uv(x, y); return [u + eu, v]; }, ex, ey };
  })();
  const pick = (u, v, h) => {
    const pat = u >= end - 1 && B.pattern.handEnd ? B.pattern.handEnd : u >= B.handFrom ? B.pattern.hand : u >= B.wrapFrom ? B.pattern.wrap : B.pattern.skin;
    return pat[Math.min(pat.length - 1, Math.floor(v + h))];
  };
  const seg = new Map();
  for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
    let [u, v] = uv(x, y);
    if (E) {
      // each band is tested on its own (a tightly bent arm folds the forearm back alongside the upper arm); the
      // forearm is drawn over the upper arm, and the elbow is a round joint the width of the arm
      const [u2, v2] = fore.uv(x, y), h2 = (u2 >= B.handFrom ? (B.handThickness ?? B.thickness) : B.thickness) / 2;
      const inFore = u2 >= eu && u2 < end && v2 >= -h2 && v2 < h2;
      const inUpper = u >= B.start && u <= eu && v >= -half && v < half;
      const inElbow = Math.hypot(x + 0.5 - fore.ex, y + 0.5 - fore.ey) <= half;
      if (inFore) { out.set(key(x, y), pick(u2, v2, h2)); ref.set(key(x, y), [Math.floor(B.pivot[0] + v2), Math.floor(B.pivot[1] + u2)]); seg.set(key(x, y), 'fore'); }
      else if (inUpper || inElbow) { const uu = Math.min(u, eu), vv = Math.max(-half, Math.min(half - 0.01, v)); out.set(key(x, y), pick(uu, vv, half)); ref.set(key(x, y), [Math.floor(B.pivot[0] + vv), Math.floor(B.pivot[1] + uu)]); seg.set(key(x, y), 'upper'); }
      continue;
    }
    const hand = u >= B.handFrom, h = hand ? (B.handThickness ?? B.thickness) / 2 : half;
    if (u < B.start || u >= end || v < -h || v >= h) continue;
    out.set(key(x, y), pick(u, v, h));
    ref.set(key(x, y), [Math.floor(B.pivot[0] + v), Math.floor(B.pivot[1] + u)]);
  }
  // where the forearm lies against the upper arm away from the elbow, the upper arm's edge becomes outline, so the
  // two read as separate limb segments
  if (E) for (const [q, sg] of seg) {
    if (sg !== 'upper') continue;
    const [x, y] = unkey(q);
    if (Math.hypot(x + 0.5 - fore.ex, y + 0.5 - fore.ey) <= half + 1) continue;
    if (N4.some(([dx, dy]) => seg.get(key(x + dx, y + dy)) === 'fore')) { out.set(q, 'o'); ref.delete(q); }
  }
  // an authored fist replaces the band's hand segment: its anchor cell sits on the arm line where the hand begins.
  // The fist is chosen by the direction of the hand: back (fist), forward (fist mirrored) or up (fistUp).
  if (B.fist) {
    const along = (x, y) => (E ? fore.uv(x, y) : uv(x, y))[0];
    for (const q of [...out.keys()]) { const [x, y] = unkey(q); if (along(x, y) >= B.handFrom) { out.delete(q); ref.delete(q); } }
    const a = ((E ? E.angle : p.angle) % 360 + 540) % 360 - 180, t = a * Math.PI / 180;
    const ox = E ? fore.ex : B.pivot[0], oy = E ? fore.ey : B.pivot[1], du = E ? B.handFrom - eu : B.handFrom;
    const ax = ox - Math.sin(t) * du, ay = oy + Math.cos(t) * du;
    let F = B.fist;
    const fwdTo = B.fistForwardUpTo ?? -135;   // forward fist from straight ahead up to this angle (toward up)
    const mir = { anchor: [B.fist.rows[0].length - 1 - B.fist.anchor[0], B.fist.anchor[1]], rows: B.fist.rows.map((r) => [...r].reverse().join('')) };
    if (p.fistKind === 'front' && B.fistFront) F = B.fistFront;   // knuckles toward the viewer (a punch at the camera)
    else if (p.fistKind === 'palm' && B.palmUp) F = (a > -60 && a < 60 && B.palmDown) ? B.palmDown : B.palmUp;   // open hand: heel of the palm leads (palm strikes)
    else if (p.fistKind === 'heel' && B.palmHeel) F = B.palmHeel;   // open hand, heel of the palm leading a straight thrust, fingers up (standing Sumo Palm)
    else if (p.fistKind === 'up' && B.fistUp) F = B.fistUp;
    else if (p.fistKind === 'forward') F = mir;
    else if (p.fistKind === 'back') F = B.fist;
    else if (a < -45 && a >= fwdTo) F = { anchor: [B.fist.rows[0].length - 1 - B.fist.anchor[0], B.fist.anchor[1]], rows: B.fist.rows.map((r) => [...r].reverse().join('')) };
    else if ((a > 135 || a < -135) && B.fistUp) F = B.fistUp;
    // fistDy: a bent arm's fist may sit higher or lower on the wrist (whole pixels)
    const x0 = Math.floor(ax) - F.anchor[0], y0 = Math.floor(ay) - F.anchor[1] + (E ? (E.fistDy ?? B.bentFistDy ?? 0) : 0);
    F.rows.forEach((row, r) => [...row].forEach((c, j) => {
      if (c === '.') return;
      const q = key(x0 + j, y0 + r);
      out.set(q, c);
      if (!E) { const [u, v] = uv(x0 + j, y0 + r); ref.set(q, [Math.floor(B.pivot[0] + v), Math.floor(B.pivot[1] + u)]); }
    }));
  }
  out.ref = ref;
  return out;
}
const bandRef = (p) => { const r = bandArm(p).ref; return (x, y) => r.get(key(x, y)) || [-1, -1]; };
function buildArm(p) {
  if (p.construction === 'band') return bandArm(p);
  const shift = armShift(p), row = armRow(p);
  if (Math.min(...armRows) < AR.shoulder) throw new Error('reference arm starts above the shoulder row');
  const out = new Map();
  for (const [k, c] of refArm) { const [x, y] = unkey(k), ny = row(y); if (ny !== null) out.set(key(x + shift(y), ny), c); }
  return out;
}
function closeArm(out, keep) {
  for (const [k, c] of [...out]) {
    if (c === '#' || c === 'o') continue;
    const [x, y] = unkey(k);
    for (const [dx, dy] of N4) { const q = key(x + dx, y + dy); if (!out.has(q) && !keep(x + dx, y + dy, q)) out.set(q, 'o'); }
  }
  return out;
}

// ---- body without the near limbs ----------------------------------------------------------------------
const R = spec.armRemovalFill;
const bodyRest = new Map(), holes = [];
for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
  const p = bodyPart(x, y);
  if (!p || LEG_PARTS.includes(p)) continue;
  if (nearSide.arm.includes(p)) { holes.push([x, y]); bodyRest.set(key(x, y), null); } else bodyRest.set(key(x, y), sym(body, x, y));
}
for (const [x, y] of holes) {
  const k = key(x, y);
  if (y <= R.torsoMaxRow) bodyRest.set(k, 'm');
  else if (y <= R.trunkRows[1]) bodyRest.set(k, x < R.trunkGreyFromX ? 'W' : 'w');
  else if (y === R.trunkWhiteRow) bodyRest.set(k, 'W');
  else if (y === R.hemRow) bodyRest.set(k, 'o');
  else bodyRest.delete(k);
}
for (let y = R.frontEdgeRows[0]; y <= R.frontEdgeRows[1]; y++) {
  const xs = holes.filter(([, hy]) => hy === y).map(([x]) => x).filter((x) => bodyRest.has(key(x, y)));
  if (xs.length) { const m = Math.max(...xs); if (!bodyRest.has(key(m + 1, y))) bodyRest.set(key(m, y), 'o'); }
}
const filled = (v) => v !== undefined && v !== '#';
for (let y = R.separatorRows[0]; y <= R.separatorRows[1]; y++) for (let x = R.separatorCols[0]; x <= R.separatorCols[1]; x++) {
  if (bodyRest.get(key(x, y)) === '#' && filled(bodyRest.get(key(x + 1, y))) && filled(bodyRest.get(key(x - 1, y)))) bodyRest.set(key(x, y), 'W');
}
for (let x = 0; x < FRAME; x++) {
  const r = R.trunkWhiteRow;
  if (bodyRest.get(key(x, r)) === 'd' && bodyRest.get(key(x + 1, r)) === 'W' && ['W', 'w'].includes(bodyRest.get(key(x - 1, r)))) bodyRest.set(key(x, r), 'W');
}

// ---- lean (optional) --------------------------------------------------------------------------------------
// A forward lean is stacked whole-pixel offsets toward the facing: pelvis, torso (with the arms, which hang from the
// shoulders) and head (with hair and eyes) each move sideways as a block. Legs are authored per pose and do not lean.
// The arm-removal fills belong to the torso up to torsoMaxRow and to the pelvis below.
// With lean.torsoShear the torso is not a block: each torso row moves by the straight line from the pelvis offset
// (below torsoMaxRow) to the head offset (above the shoulder row), so the back stays one slanted line.
const LEAN = spec.lean?.dx, TORSO_SHEAR = !!spec.lean?.torsoShear;
for (const [g, v] of Object.entries(LEAN || {})) if (Array.isArray(v) && v.length !== F) throw new Error(`lean ${g} needs ${F} entries`);
const leanGroup = (part, y) => {
  if (!part || LEG_PARTS.includes(part)) return null;
  if (part === 'head' || overlays.overlayParts?.[part]?.lagFrames !== undefined && part !== 'sash') return 'head';
  if (part === 'torso') return 'torso';
  if (part === 'pelvis' || part === 'sash') return 'pelvis';
  if (LIMB[part]?.[0] === 'arm') return y === undefined || y <= R.torsoMaxRow ? 'torso' : 'pelvis';
  return null;
};
const leanVal = (group, k) => { const v = group && LEAN?.[group]; return Array.isArray(v) ? v[k] : (v || 0); };
const leanOf = (group, k, y) => {
  if (group !== 'torso' || !TORSO_SHEAR) return leanVal(group, k);
  const lo = R.torsoMaxRow + 1, hi = AR.shoulder - 1, yy = Math.max(hi, Math.min(lo, y ?? AR.shoulder));
  return roundHalfEven(leanVal('pelvis', k) + (leanVal('head', k) - leanVal('pelvis', k)) * (lo - yy) / (lo - hi));
};
// lean.torsoDrop shortens the leaning torso so it keeps its length: that many torso rows, evenly spaced between the
// shoulder row and torsoMaxRow, are removed and everything above them (upper torso, head, hair, eyes, arms) moves down.
const DROP = spec.lean?.torsoDrop || 0;
const torsoDropped = Array.from({ length: DROP }, (_, i) => AR.shoulder + Math.floor((i + 0.5) * (R.torsoMaxRow - AR.shoulder + 1) / DROP));
// lean.headDy lowers the head (with hair and eyes) on its own, sinking the neck into the shoulders; the head is drawn
// over the torso where they meet.
const HEAD_DY = spec.lean?.headDy || 0;
const leanY = (group, y) => (group === 'head' ? y + DROP + HEAD_DY : group === 'arm' ? y + DROP
  : group === 'torso' ? (torsoDropped.includes(y) ? null : y + torsoDropped.filter((r) => r > y).length) : y);
// a front/back view may shorten the torso on its own (view torsoDrop, in place of lean.torsoDrop): a forward lean seen
// from the front or behind reads as a shorter trunk with the head sunk between the shoulders
const viewDrop = (d) => d?.torsoDrop ?? DROP;
const viewLeanY = (d, group, y) => {
  const n = viewDrop(d);
  if (n === DROP) return leanY(group, y);
  const dropped = Array.from({ length: n }, (_, i) => AR.shoulder + Math.floor((i + 0.5) * (R.torsoMaxRow - AR.shoulder + 1) / n));
  return group === 'head' ? y + n + HEAD_DY : group === 'arm' ? y + n
    : group === 'torso' ? (dropped.includes(y) ? null : y + dropped.filter((r) => r > y).length) : y;
};
const restGroup = new Map();
for (const p of bodyRest.keys()) { const [x, y] = unkey(p); restGroup.set(p, leanGroup(bodyPart(x, y), y)); }

// ---- overlays (hair, eyes) ------------------------------------------------------------------------------
const overlayLayers = spec.overlays.layers.map((name) => {
  const l = overlays.layers.find((o) => path.basename(o.partMap, '.png') === name);
  if (!l) throw new Error(`overlay ${name} not in overlays.json`);
  return { name, img: readPng(path.join(root, l.source)), map: readPng(path.join(rigDir, l.partMap)) };
});
const lagOf = (part) => (part === 'head' ? 0 : overlays.overlayParts?.[part]?.lagFrames);

const OUTLINE_RAISED = !!spec.arms?.outlineRaised || process.env.OUTLINE_RAISED === '1';
const bob = spec.bob.dy;
// ---- frames -------------------------------------------------------------------------------------------
const FAR_ARM_PX = [];   // positions where the posed far arm shows (for far-arm accessories)
const report = { cleanupRemoved: [], cleanupMerged: [], frontalOutlineAdded: {}, frontalHoleFills: {} };
// bob.head / bob.arms: optional per-frame dy for the head (with hair and eyes; it moves at the neck) and the arms (they
// move at the shoulders), in place of the body bob; given as absolute dy like bob.dy
const headDelta = (k) => (spec.bob.head ? spec.bob.head[k] - bob[k] : 0);
const armDelta = (k) => (spec.bob.arms ? spec.bob.arms[k] - bob[k] : 0);
for (const t of ['head', 'arms']) if (spec.bob[t] && spec.bob[t].length !== F) throw new Error(`bob.${t} needs ${F} entries`);
function frame(k) {
  const b = bob[k], HD = headDelta(k), AD = armDelta(k);
  const bodyL = new Map(), armsL = new Map();
  const far = legPoses[L.far[k]], near = legPoses[L.near[k]];
  const T = leanOf('torso', k, AR.shoulder);
  const shifted = (m) => new Map([...m].map(([p, c]) => { const [x, y] = unkey(p); return [key(x + T, y + DROP), c]; }));
  const rest = new Map([...bodyRest].sort(([p], [q]) => (restGroup.get(p) === 'head') - (restGroup.get(q) === 'head')).flatMap(([p, c]) => { const [x, y] = unkey(p), g = restGroup.get(p), ny = leanY(g, y); return ny === null ? [] : [[key(x + leanOf(g, k, y), ny + (g === 'head' ? HD : 0)), c]]; }));
  // where the lean slides one block past the next (torso over pelvis, head over neck), an edge that was covered in the
  // reference is now open and gets outline
  if (LEAN) for (const [p, c] of bodyRest) {
    if (c === '#' || c === 'o') continue;
    const [x, y] = unkey(p), g = restGroup.get(p), lx = x + leanOf(g, k, y), ly0 = leanY(g, y);
    if (ly0 === null) continue;
    const ly = ly0 + (g === 'head' ? HD : 0);
    for (const [dx, dy] of N4) {
      const q = key(lx + dx, ly + dy);
      if (bodyRest.has(key(x + dx, y + dy)) && !rest.has(q)) rest.set(q, 'o');
    }
  }
  // a raised (band) near arm crosses the torso, so it is outlined over the body as well. Above the shoulder row an arm
  // gets no outline (it joins the shoulder there); with arms.outlineRaised a band arm raised above the shoulder row
  // (forearm and fist over the face) is outlined there too, except at the shoulder joint itself (within the arm's
  // thickness of its pivot), so overlapping parts keep reading (outlineRule, user 2026-10-14)
  const joint = (p) => (x, y) => {
    if (y >= AR.shoulder + DROP) return false;
    if (!(OUTLINE_RAISED && p.construction === 'band')) return true;
    const B = { ...A.band, ...(p.band || {}) };
    return Math.hypot(x + 0.5 - T - B.pivot[0], y + 0.5 - DROP - B.pivot[1]) <= B.thickness / 2 + 1.5;
  };
  const nj = joint(A.near[k]), fj = joint(A.far[k]);
  const na = closeArm(shifted(buildArm(A.near[k])), (x, y, q) => nj(x, y) || (A.near[k].construction !== 'band' && rest.has(q)));
  const fa = closeArm(shifted(buildArm(A.far[k])), (x, y) => fj(x, y));
  for (const [p, c] of far) bodyL.set(p, colourOf(farShade[c]));
  for (const [p, c] of fa) { const [x, y] = unkey(p); bodyL.set(key(x, y + b + AD), colourOf(farShade[c])); }
  const farKeys = new Set(bodyL.keys());
  for (const [p, c] of near) bodyL.set(p, colourOf(c));
  for (const [p, c] of rest) { const [x, y] = unkey(p); bodyL.set(key(x, y + b), colourOf(c)); }
  for (const [p, c] of na) { const [x, y] = unkey(p); armsL.set(key(x, y + b + AD), colourOf(c)); }
  const nearPos = new Set([...near.keys(), ...[...rest.keys()].map((p) => { const [x, y] = unkey(p); return key(x, y + b); }), ...[...na.keys()].map((p) => { const [x, y] = unkey(p); return key(x, y + b + AD); })]);
  const farPx = new Set([...farKeys].filter((p) => !nearPos.has(p)));
  FAR_ARM_PX[k] = new Set([...fa.keys()].map((p) => { const [x, y] = unkey(p); return key(x, y + b + AD); }).filter((p) => farPx.has(p)));
  const comp = () => { const m = new Map(bodyL); for (const [p, c] of armsL) m.set(p, c); return m; };
  let img = comp();
  // closeOpenEdges: a body edge the reference left covered (the back of the shorts over a raised rear leg) gets outline
  if (spec.cleanup.closeOpenEdges) for (const [p, c] of [...img]) {
    if (!coloured(c)) continue;
    const [x, y] = unkey(p);
    if (y < spec.cleanup.notchFromRow) continue;
    for (const [dx, dy] of N4) { const q = key(x + dx, y + dy); if (!img.has(q)) { img.set(q, GEN); bodyL.set(q, GEN); } }
  }
  for (let y = spec.cleanup.notchFromRow; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
    if (img.has(key(x, y))) continue;
    if (N4.filter(([dx, dy]) => img.has(key(x + dx, y + dy))).length >= 3) { img.set(key(x, y), GEN); bodyL.set(key(x, y), GEN); }
  }
  // remove generated outline that outlines nothing
  const removed = [];
  for (;;) {
    const drop = [];
    for (const [p, c] of img) {
      if (c !== GEN) continue;
      const [x, y] = unkey(p), nb = N4.map(([dx, dy]) => img.get(key(x + dx, y + dy)));
      if (nb.includes(undefined) && !nb.some(coloured)) drop.push(p);
    }
    if (!drop.length) break;
    for (const p of drop) {
      for (const layer of [bodyL, armsL]) if (layer.has(p) && coloured(layer.get(p))) throw new Error(`cleanup at ${p} would remove a coloured pixel`);
      img.delete(p); bodyL.delete(p); armsL.delete(p); removed.push(p);
    }
  }
  // merge doubled lines on the far side (row-major order)
  const merged = [];
  const pts = [...img.keys()].map(unkey).sort((a, c) => a[1] - c[1] || a[0] - c[0]);
  for (const [x, y] of pts) {
    const p = key(x, y);
    if (img.get(p) !== GEN || N4.some(([dx, dy]) => !img.has(key(x + dx, y + dy)))) continue;
    for (const [a, d] of N4) {
      const n1 = img.get(key(x + a, y + d)), n2 = img.get(key(x - a, y - d)), n3 = img.get(key(x - 2 * a, y - 2 * d));
      if (farPx.has(p) && farPx.has(key(x + a, y + d)) && coloured(n1) && (n2 === GEN || n2 === BLACK) && coloured(n3)
        && !N4.some(([dx, dy]) => coloured(img.get(key(x + dx, y + dy))) && !farPx.has(key(x + dx, y + dy)))) {
        if (armsL.has(p)) throw new Error(`merge at ${p} is covered by the arms layer`);
        img.set(p, n1); bodyL.set(p, n1); merged.push(p); break;
      }
    }
  }
  report.cleanupRemoved.push(removed.length); report.cleanupMerged.push(merged.length);
  for (const layer of [bodyL, armsL]) for (const [p, c] of layer) if (c === GEN) layer.set(p, BLACK);
  // overlays follow the head; lagging falls never sit higher than the part above them
  const hb = (kk) => bob[kk] + headDelta(kk);
  // spec.overlays.noLagFrames: frames whose hair falls (and sash flaps, below) follow with no lag (e.g. the first upright frame after a
  // lying frame, where the earlier bob belongs to a rotated body and would leave the falls detached)
  const noLag = spec.overlays?.noLagFrames?.includes(k);
  const cap = hb(k), up = noLag ? cap : Math.min(hb((k - 1 + F) % F), cap), lo = noLag ? cap : Math.min(hb((k - 2 + F) % F), up), dyOf = [cap, up, lo];
  const ov = {};
  for (const l of overlayLayers) {
    const m = new Map();
    for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
      if (!opaque(l.img, ox + x, y)) continue;
      const part = colourToPart.get(hexAt(l.map, ox + x, y)), lag = lagOf(part);
      if (lag === undefined) throw new Error(`${l.name}: pixel ${x},${y} has part ${part}, which has no walk motion`);
      m.set(key(x + leanOf(leanGroup(part), k, y), leanY(leanGroup(part), y) + dyOf[lag]), hexAt(l.img, ox + x, y));
    }
    ov[l.name] = m;
  }
  return { body: bodyL, arms: armsL, ...ov };
}
const srcFrames = Array.from({ length: F }, (_, k) => frame(k));
const layerNames = Object.keys(srcFrames[0]);

// ---- mirrored directions --------------------------------------------------------------------------------
const mirrorValid = {};
const sourceImgs = { body, arms, ...Object.fromEntries(overlayLayers.map((l) => [l.name, l.img])) };
const mirrors = Object.fromEntries(Object.entries(spec.mirror || {}).filter(([d]) => d !== 'rule'));
for (const [dir, { from }] of Object.entries(mirrors)) {
  const a = order.indexOf(from) * FRAME, w = order.indexOf(dir) * FRAME;
  mirrorValid[dir] = Object.values(sourceImgs).every((img) => {
    for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
      const i = (y * img.w + a + x) * 4, j = (y * img.w + w + FRAME - 1 - x) * 4;
      if (img.px.compare(img.px, j, j + 4, i, i + 4) !== 0) return false;
    }
    return true;
  });
  if (!mirrorValid[dir]) throw new Error(`${dir} reference is not a mirror of ${from}; it cannot be mirrored`);
}
// ---- front and back views (row edits on the reference frame) -------------------------------------------------
// No new pixels: a limb gets shorter by dropping listed reference rows and longer by repeating them; every row of
// that limb below the edit moves with it. Parts above the legs bob as a block.
const FR = spec.frontal;
function partNear(map, fx, x, y) {
  if (opaque(map, fx + x, y)) { const p = colourToPart.get(hexAt(map, fx + x, y)); if (p) return p; }
  for (let r = 1; r <= 3; r++) for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) {
    const nx = x + dx, ny = y + dy;
    if (nx >= 0 && ny >= 0 && nx < FRAME && ny < FRAME && opaque(map, fx + nx, ny)) { const p = colourToPart.get(hexAt(map, fx + nx, ny)); if (p) return p; }
  }
  return undefined;
}
const rowMap = (y, bobDy, removed, repeated) => {
  if (removed.includes(y)) return [];
  const s = y + bobDy - removed.filter((r) => r < y).length + repeated.filter((r) => r < y).length;
  return [s, ...repeated.filter((r) => r === y).map((_, i) => s + i + 1)];
};
// Diagonal views add a sideways swing: every limb row also shifts sideways, from hipDx / 0 at the pivot (hip or
// shoulder) growing linearly to footDx / handDx at the foot or hand, which move rigidly. Where a moved limb newly
// leaves colour against empty space, outline is added; reference edges stay as drawn.
const shear = (y, pivot, rigid, total) => { const yy = Math.min(y, rigid); return yy <= pivot ? 0 : roundHalfEven(total * (yy - pivot) / (rigid - pivot)); };
const refExposed = {};
// body pixels of a head drawn in front of the torso (headZ above 3): clothing does not cover them
const HEAD_FRONT = {}, BAND_SHOWN = {}, LEG_FRONT = {}, WEAPON_ARM = {};
function exposedInReference(fx) {
  if (refExposed[fx]) return refExposed[fx];
  const m = new Map();
  for (const img of [body, arms]) for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) if (opaque(img, fx + x, y)) m.set(key(x, y), hexAt(img, fx + x, y));
  return (refExposed[fx] = new Set([...m].filter(([p, c]) => { const [x, y] = unkey(p); return c !== BLACK && N4.some(([dx, dy]) => !m.has(key(x + dx, y + dy))); }).map(([p]) => p)));
}
// Where one pixel of a front/back/diagonal view goes at frame k: its rows (after row edits), sideways shift and depth.
// legBand: a diagonal view's legs are the E sprint's band legs (same poses and phase), each moved to its own hip in
// this view (offset, plus the pelvis lean) and narrowed sideways by scaleX for the angled stride; the far leg is one
// shade darker and drawn behind the body.
const bandLegCache = new Map();
// legBand.sides: per side and frame, whether that leg is a band leg (otherwise it keeps its reference rows);
// legBand.pose: per side and frame, a named pose authored in this view's own coordinates (used as is, no offset or
// scale), with legBand.z per side and frame for its depth (a kick toward the viewer is drawn in front of the body)
const bandSide = (d, s, k) => !!d.legBand && (!d.legBand.sides || !!d.legBand.sides[s]?.[k]);
function frontalLegs(d, k) {
  const LB = d.legBand, far = d.far, pl = d.leanScale ? roundHalfEven(d.leanScale * leanOf('pelvis', k)) * (d.leanSign || 1) : 0;
  return ['R', 'L'].filter((side) => bandSide(d, side, k)).map((side) => {
    const named = LB.pose?.[side]?.[k];
    if (named) {
      const p0 = L.poses.find((p) => p.name === named);
      if (!p0) throw new Error(`legBand pose ${named} not in legs.poses`);
      // a view bob (bent standing leg) lowers the kicking leg with the body, and a hip hike raises it with its hip
      const bd = bobOf(d, k) - bob[k] + (d.variants?.[k] ? variantShear(d, k, p0.hipX, p0.hipRow, 'pelvis') : 0);
      const pose = bd ? { ...p0, hipRow: p0.hipRow + bd, kneeRow: p0.kneeRow + bd, ankle: [p0.ankle[0], p0.ankle[1] + bd] } : p0;
      const ck = JSON.stringify(pose);
      if (!bandLegCache.has(ck)) bandLegCache.set(ck, buildLeg(pose));
      return { side, isFar: side === far, z: LB.z?.[side]?.[k] ?? 2, pose, legMap: bandLegCache.get(ck) };
    }
    const isFar = side === far, src = L.poses[L[isFar ? 'far' : 'near'][k]], off = LB.offset[side] + pl, sx = LB.scaleX ?? 1;
    const hx = src.hipX + off, tx = (v) => hx + roundHalfEven((v - src.hipX) * sx);
    const pose = { ...src, hipX: hx, kneeX: tx(src.kneeX), footX: tx(src.footX) };
    const ck = JSON.stringify(pose);
    if (!bandLegCache.has(ck)) bandLegCache.set(ck, buildLeg(pose));
    return { side, isFar, z: isFar ? 0 : 2, pose, legMap: bandLegCache.get(ck) };
  });
}
function twistOf(d, k, g, y) {
  const T = d.twist;
  if (!T || !g) return 0;
  if (g === 'pelvis') return T.pelvis[k];
  if (g === 'head') return T.head[k];
  if (g !== 'torso') return 0;
  const lo = R.torsoMaxRow + 1, hi = AR.shoulder, yy = Math.max(hi, Math.min(lo, y));
  return roundHalfEven(T.pelvis[k] + (T.shoulders[k] - T.pelvis[k]) * (lo - yy) / (lo - hi));
}
// Part variants of a frontal view, per frame (frontal.partVariants, named and reused; the view lists them per frame):
//   bob     a per-frame bob for this view (the planted leg bends: it drops that many bob rows, the body sits lower)
//   hike    pelvis raised on one side: a whole-pixel column shear, dy at the left and right ends of span (the torso,
//           head and shoulders above ride on it)
//   tilt    torso tilt: a further column shear growing from 0 at the trunk top to full at the shoulder row (head and
//           shoulders follow at their own column); with rigid (a reference torso row) the torso above that row and the
//           head move as one block and that row is the only seam: raised, it repeats down to its own place; lowered, the
//           torso rows just below it are dropped; the torso below it stays on the pelvis
//   turn    hips turned: the shorts lose one column on that side (the column at 'col' is dropped, the outer ones move in)
//   knee    the bent standing leg's knee moves dx sideways (rows: hip, knee, ankle; full at the knee)
//   plant   the standing leg (side) moves dx as a whole, toward the centre line
//   tiptoe  the heel raised: hem and sock risen 'up' rows over the shortened shin, the shoe drawn as an authored foot (rows, at, sample)
//   rotate  torso and hips turned into the kick: on the far side of 'center' the listed columns are dropped per part
//           (the outer columns close in, so that side narrows); the near side moves nearDx toward the centre; the
//           head moves headDx and each band arm's shoulder armDx[side]
const variantsOf = (d, k) => (d.variants?.[k] || []).map((n) => { const v = FR.partVariants?.[n]; if (!v) throw new Error(`part variant ${n} not defined`); return v; });
const bobOf = (d, k) => { const v = variantsOf(d, k).find((x) => x.bob !== undefined); return v ? v.bob : bob[k]; };
function variantShear(d, k, x, y, group) {
  let dy = 0;
  const lerp = (span, ends, xx) => { const t = Math.max(0, Math.min(1, (xx - span[0]) / (span[1] - span[0]))); return ends[0] + (ends[1] - ends[0]) * t; };
  for (const v of variantsOf(d, k)) {
    if (v.hike && group !== 'leg') dy += lerp(v.span, v.hike, group === 'head' ? v.headX : x);
    if (v.tilt && (group === 'torso' || group === 'head')) {
      const f = group === 'head' ? 1 : v.rigid !== undefined ? (y <= v.rigid ? 1 : 0) : Math.max(0, Math.min(1, (R.torsoMaxRow + 1 - y) / (R.torsoMaxRow + 1 - AR.shoulder)));
      dy += lerp(v.span, v.tilt, group === 'head' ? v.headX : x) * f;
    }
  }
  return roundHalfEven(dy);
}
function variantTurn(d, k, x, part) {
  if (part !== 'pelvis' && part !== 'sash') return 0;
  for (const v of variantsOf(d, k)) if (v.turn) {
    const c = v.turn.col;
    if (x === c) return null;                              // the dropped column
    if (v.turn.side === 'left' && x < c) return 1;         // outer columns move in
    if (v.turn.side === 'right' && x > c) return -1;
  }
  return 0;
}
function variantRotate(d, k, x, part) {
  let dx = 0;
  for (const v of variantsOf(d, k)) {
    const r = v.rotate;
    if (!r) continue;
    if (part === 'head' || overlays.overlayParts?.[part]?.lagFrames !== undefined) { dx += r.headDx || 0; continue; }
    const drop = r.drop?.[part === 'sash' ? 'pelvis' : part];
    if (!drop) continue;
    if (drop.includes(x)) return null;
    const farRight = r.far === 'right', far = farRight ? x > r.center : x < r.center;
    if (far) dx += farRight ? -drop.filter((c) => c < x && c > r.center).length : drop.filter((c) => c > x && c < r.center).length;
    else if (x !== r.center) dx += farRight ? r.nearDx : -r.nearDx;
  }
  return dx;
}
const rotateArmDx = (d, k, sd) => variantsOf(d, k).reduce((a, v) => a + (v.rotate?.armDx?.[sd] || 0), 0);
function frontalMove(d, k, part, y, x) {
  // crouch: a view's whole figure sits lower by d.crouch rows (every leg drops that many more bob rows)
  const b = bobOf(d, k) + (d.crouch || 0), lift = d.legLift || FR.legLift, far = d.far, limb = LIMB[part];
  const c0 = d.crouch || 0, cap = b, up = Math.min(bobOf(d, (k - 1 + F) % F) + c0, cap), lo = Math.min(bobOf(d, (k - 2 + F) % F) + c0, up), dyOf = [cap, up, lo];
  let rows, dx = 0, z = 3, legDrop = [], zOver;
  if (limb?.[0] === 'leg') {
    const s = limb[1], n = lift[s][k] + b;
    if (bandSide(d, s, k)) rows = [];   // drawn as band legs instead (frontalLegs)
    else if (d.legPose) {
      // a named leg pose drops its own rows (thigh rows foreshorten a knee coming toward or away from the viewer,
      // shin rows a lower leg folding back); every leg also drops the frame's bob rows so the planted foot stays down
      // pose rows and bob rows may be given per side ({R, L}) where the two legs are drawn differently (diagonals)
      const side = (v) => (Array.isArray(v) ? v : v[s]);
      const drop = [...new Set([...side(d.legPoseRows[d.legPose[s][k]]), ...side(d.bobRows).slice(0, b)])];
      rows = rowMap(y, b, drop, []); legDrop = drop;
      // a swinging leg comes in under the body: it shears toward the centre line from the hip row to the foot
      const pdx = (d.legPoseDx?.[d.legPose[s][k]] || 0) * (d.inward?.[s] || 0);
      if (pdx) dx = shear(y, d.legPivot ?? 39, d.legPoseDxFrom ?? 56, pdx);
      // diagonal views also swing the leg sideways from the hip to the foot
      if (d.footDx) { const hd = d.hipDx[s][k]; dx += hd + shear(y, d.legPivot, d.footFrom[s], d.footDx[s][k] - hd); }
    } else rows = rowMap(y, b, n > 0 ? d.legRows[s].slice(0, n) : [], n < 0 ? d.legRepeatRows[s].slice(0, -n) : []);
    if (d.footDx) { const hd = d.hipDx[s][k]; dx = hd + shear(y, d.legPivot, d.footFrom[s], d.footDx[s][k] - hd); }
    // knee variant: the bent standing leg's knee comes out sideways, growing from the hip row to the knee row and
    // back to nothing at the ankle (whole pixels)
    // plant variant: the standing leg moves dx toward the centre line as a whole (weight over the support foot)
    for (const v of variantsOf(d, k)) if (v.plant?.side === s) dx += v.plant.dx;
    // tiptoe: the heel raised (Muay Thai lead foot seen from the front/back): the reference shoe rows (from shoe down)
    // are left out and drawn as the authored foot (frontalFrame); the hem and sock (from hem down) rise up rows, and the
    // trouser rows that would land in the up rows just above the risen hem are left out, so the shin shortens there
    // keep: that many trouser rows just above the hem rise with it (a knee chambered toward the viewer shows as the
    // knee block with the shin hanging below it); z: the leg's depth (in front of the torso when it comes at the viewer)
    for (const v of variantsOf(d, k)) if (v.tiptoe?.side === s) {
      const t = v.tiptoe, pH = rowMap(t.hem, b, legDrop, [])[0], top = t.hem - (t.keep || 0);
      if (y >= t.shoe) rows = [];
      else if (y >= top) rows = rows.map((r) => r - t.up);
      else rows = rows.filter((r) => r < pH - t.up - (t.keep || 0));
      if (t.z !== undefined) zOver = t.z;
    }
    for (const v of variantsOf(d, k)) if (v.knee?.side === s) {
      const [h0, kn, a0] = v.knee.rows, t = y <= h0 || y >= a0 ? 0 : y <= kn ? (y - h0) / (kn - h0) : (a0 - y) / (a0 - kn);
      dx += roundHalfEven(v.knee.dx * t);
    }
    z = zOver ?? (s === far ? 0 : 2);
  } else if (limb?.[0] === 'arm') {
    const s = limb[1], h = d.handDy[s][k];
    rows = rowMap(y, b, h < 0 ? d.armRows[s].slice(0, -h) : [], h > 0 ? d.armRepeatRows[s].slice(0, h) : []);
    if (d.handDx) dx = shear(y, d.armPivot, d.handFrom[s], d.handDx[s][k]);
    z = s === far ? -1 : 4;
    rows = rows.map((r) => r + viewDrop(d) + armDelta(k));   // the lean's shortened torso lowers the shoulders
    // armVisibleTo: arms swept behind the body show only down to this reference row (shoulder and upper arm)
    if (d.armBand?.[s]) rows = [];   // drawn as an authored band arm instead (frontalFrame)
    const vis = typeof d.armVisibleTo === 'object' ? d.armVisibleTo?.[s] : d.armVisibleTo;
    if (vis !== undefined && vis !== null && y > vis) rows = [];
  } else if (part === 'head' || overlays.overlayParts?.[part]?.lagFrames !== undefined) {
    // a view may lower the head further (headDy, one value or per frame) and draw it in front of the torso (headZ above
    // 3) or behind it
    const g = leanGroup(part);
    rows = [viewLeanY(d, g, y) + dyOf[lagOf(part)] + (g === 'head' ? (Array.isArray(d.headDy) ? d.headDy[k] : d.headDy || 0) + headDelta(k) : 0)];
    if (g === 'head' && d.headZ !== undefined) z = d.headZ;
  }
  else if (part === 'torso') { const ny = viewLeanY(d, 'torso', y); rows = ny === null ? [] : [ny + b]; }
  else { rows = [y + b]; if (part === 'pelvis') z = 2.5; }
  // twist: a frontal view's body rotation as sideways whole-pixel offsets: pelvis and head as blocks, the torso
  // sheared from the pelvis value (trunk top) to the shoulders value (shoulder row); arms follow the shoulders
  if (d.twist && limb?.[0] !== 'leg') dx += twistOf(d, k, limb?.[0] === 'arm' ? 'torso' : leanGroup(part, y), limb?.[0] === 'arm' ? AR.shoulder : y);
  // leanScale: a diagonal view shows part of the profile lean sideways (toward the facing), scaled from E's offsets
  if (d.leanScale && limb?.[0] !== 'leg') {
    const g = limb?.[0] === 'arm' ? 'torso' : leanGroup(part, y), ly = limb?.[0] === 'arm' ? AR.shoulder : y;
    if (g) dx += roundHalfEven(d.leanScale * leanOf(g, k, ly)) * (d.leanSign || 1);
  }
  if (d.variants?.[k] && x !== undefined && limb?.[0] !== 'leg') {
    const group = part === 'torso' ? 'torso' : part === 'pelvis' || part === 'sash' ? 'pelvis' : (part === 'head' || overlays.overlayParts?.[part]?.lagFrames !== undefined) ? 'head' : null;
    if (group) {
      const sh = variantShear(d, k, x, y, group), tn = variantTurn(d, k, x, part), rt = variantRotate(d, k, x, part);
      rows = tn === null || rt === null ? [] : rows.map((r) => r + sh);
      // a rigid tilt's seam row: raised, it repeats down to its own place; lowered, the torso rows below it are dropped
      const seam = variantsOf(d, k).find((v) => v.tilt && v.rigid !== undefined)?.rigid;
      if (seam !== undefined && group === 'torso' && rows.length) {
        const lift = variantShear(d, k, x, seam, 'torso');
        if (lift < 0 && y === seam) { const r0 = Math.max(...rows); for (let i = 1; i <= -lift; i++) rows.push(r0 + i); }
        if (lift > 0 && y > seam && y <= seam + lift) rows = [];
      }
      if (tn) dx += tn;
      if (rt) dx += rt;
    }
  }
  return { rows, dx, z };
}
// A view's band arm for one side: its pixels (symbols, in frame coordinates after bob, crouch, torso drop and lean)
// and, for each of them, the view's reference arm pixel at the same place along and across the arm (for accessories).
// Reference arm span per row (columns of the view's Arms1 pixels of one side), so a band pixel can find the reference
// pixel at the same fraction across the arm even where the reference forearm is offset from the upper arm.
const armSpanCache = {};
function refArmSpan(dir, sd) {
  const ck = `${dir}:${sd}`;
  if (armSpanCache[ck]) return armSpanCache[ck];
  const fx = order.indexOf(dir) * FRAME, span = {};
  for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
    if (!opaque(arms, fx + x, y) || hexAt(arms, fx + x, y) === BLACK) continue;
    const part = partNear(partMap, fx, x, y);
    if (LIMB[part]?.[0] !== 'arm' || LIMB[part][1] !== sd) continue;
    const e = (span[y] ??= [99, -1]); e[0] = Math.min(e[0], x); e[1] = Math.max(e[1], x);
  }
  return (armSpanCache[ck] = span);
}
function frontalBand(d, k, sd, dir) {
  const ab = d.armBand?.[sd];
  if (!ab) return null;
  // per-frame values: scale may be an array, elbow an array of {at, angle} (null for a straight arm), fist an array of
  // fist kinds ('up', 'forward', 'back') overriding the direction rule
  const at = (v) => (Array.isArray(v) ? v[k] : v);
  const sc = at(ab.scale) ?? 1, r = (v) => Math.round(v * sc), B0 = A.band, el = at(ab.elbow);
  const lx = (d.leanScale ? roundHalfEven(d.leanScale * leanOf('torso', k, AR.shoulder)) * (d.leanSign || 1) : 0)
    + twistOf(d, k, 'torso', AR.shoulder) + (at(ab.pivotDx) || 0) + rotateArmDx(d, k, sd);
  // pivotDy: the shoulder joint sits that many rows lower on this frame (keeps a wide arm's shoulder under the gi)
  const dy = bobOf(d, k) + armDelta(k) + (at(ab.pivotDy) || 0) + (d.crouch || 0) + viewDrop(d) + (d.variants?.[k] ? variantShear(d, k, ab.pivot[0], AR.shoulder, 'torso') : 0);
  const pb = { angle: at(ab.angle), band: { pivot: ab.pivot, start: B0.start, length: r(B0.length + B0.start) - B0.start,
    wrapFrom: r(B0.wrapFrom), handFrom: r(B0.handFrom) }, ...(el ? { elbow: { ...el, at: r(el.at) } } : {}), fistKind: at(ab.fist) };
  const { uv } = bandGeom(pb), pixels = new Map(), ref = new Map(), across = new Map(), zs = new Map(), span = dir ? refArmSpan(dir, sd) : {}, T = B0.thickness;
  // depth per segment: the arm is at z (default: far arm -1, behind the body; near arm 4, in front); with zFore the part
  // from foreAt along the arm (default the elbow) is at zFore instead, so a far arm's forearm and fist can come out in
  // front of the torso while its shoulder end stays behind
  const z0 = at(ab.z) ?? (sd === d.far ? -1 : 4), zF = at(ab.zFore), fAt = at(ab.foreAt) ?? (el ? r(el.at) : Infinity);
  const arm = bandArm(pb);
  for (const [q, c] of arm) {
    const [x, y] = unkey(q), Q = key(x + lx, y + dy);
    // distance along and across the arm (both segments of a bent arm)
    const rr = arm.ref.get(q), [u, v] = el ? (rr ? [rr[1] - ab.pivot[1], rr[0] - ab.pivot[0]] : [Infinity, 0]) : uv(x, y);
    // showTo: only the part of the arm up to this distance from the shoulder shows (the rest is behind the body)
    // (per frame when an array; null shows the whole arm)
    if (at(ab.showTo) != null && !(u <= at(ab.showTo))) continue;
    const ry = Math.floor(ab.pivot[1] + u / sc), e = span[ry];
    pixels.set(Q, c);
    zs.set(Q, zF !== undefined && u >= fAt ? zF : z0);
    // the reference pixel at the same fraction across the reference arm's row (back edge to front edge)
    const f = Math.max(0, Math.min(0.999, (v + T / 2) / T));
    ref.set(Q, key(e ? e[0] + Math.floor(f * (e[1] - e[0] + 1)) : Math.floor(ab.pivot[0] + v), ry));
    across.set(Q, [ry, f]);
  }
  return { pixels, ref, across, zs };
}
// armWiden: a thin reference upper arm is widened by one column on its outer side (the outermost colour column is
// repeated outward and the outline moves with it), so it is as thick as the wrist and fist below it.
// armNarrow: the opposite on the inner side: the innermost colour column of the listed rows is dropped and the inner
// outline moves out with it, leaving a gap between the wrist/fist and the body.
function widenXs(d, dir, part, x, y) {
  const N = d.armNarrow, limb = LIMB[part];
  if (N && limb?.[0] === 'arm' && y >= N.rows[0] && y <= N.rows[1]) {
    const e = refArmSpan(dir, limb[1])[y];
    if (!e) return [x];
    const inward = d.inward?.[limb[1]] || 0, i = inward > 0 ? e[1] : e[0];
    if (x === i) return [];
    return (inward > 0 ? x > i : x < i) ? [x - inward] : [x];
  }
  const W = d.armWiden;
  if (!W || limb?.[0] !== 'arm' || y < W.rows[0] || y > W.rows[1]) return [x];
  const e = refArmSpan(dir, limb[1])[y];
  if (!e) return [x];
  const inward = d.inward?.[limb[1]] || 0, o = inward > 0 ? e[0] : e[1];
  if (x === o) return [x, x - inward];
  return (inward > 0 ? x < o : x > o) ? [x - inward] : [x];
}
// tiptoe feet: rows of '#' (outline) and 's' (shoe or bare foot), coloured per layer from that layer's own reference
// pixels named in sample (the bare foot in body, the shoe in the outfit overlays; a layer with no foot there skips it)
function tiptoeFeet(d, k, img, fx, items) {
  for (const v of variantsOf(d, k)) if (v.tiptoe?.foot) {
    const t = v.tiptoe, f = t.foot;
    if (!Object.values(f.sample).every(([sx, sy]) => opaque(img, fx + sx, sy))) continue;
    const cs = Object.fromEntries(Object.entries(f.sample).map(([c, [sx, sy]]) => [c, hexAt(img, fx + sx, sy)]));
    f.rows.forEach((row, r) => [...row].forEach((c, j) => { if (c !== '.') items.push([t.z ?? (t.side === d.far ? 0 : 2), f.at[0] + j, f.at[1] + r, cs[c], 'tiptoe']); }));
  }
}
function frontalFrame(dir, k) {
  const d = FR.views[dir], fx = order.indexOf(dir) * FRAME;
  const srcLayers = [['body', body, partMap], ['arms', arms, partMap], ...overlayLayers.map((l) => [l.name, l.img, l.map])];
  const out = {}, src = {};
  for (const [name, img, map] of srcLayers) {
    const items = [];
    for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
      if (!opaque(img, fx + x, y)) continue;
      const part = partNear(map, fx, x, y);
      if (!part) throw new Error(`${name} ${dir}: pixel ${x},${y} has no rig part`);
      const { rows, dx, z } = frontalMove(d, k, part, y, x);
      for (const ny of rows) for (const wx of widenXs(d, dir, part, x, y)) items.push([z, wx + dx, ny, hexAt(img, fx + x, y), key(x, y)]);
    }
    tiptoeFeet(d, k, img, fx, items);
    // armBand: a raised arm seen at an angle is drawn as the authored band arm (constant thickness, authored fist)
    // from the view's shoulder pivot, its segment lengths scaled for foreshortening
    if (name === 'body' && d.legBand) for (const lg of frontalLegs(d, k)) for (const [q, c] of lg.legMap) {
      const sy = lg.isFar ? farShade[c] : c, [x, y] = unkey(q);
      items.push([lg.z, x, y, sy === 'o' ? BLACK : pal[sy], 'band']);
      // a leg kicking toward the viewer (z 3 and up) is in front of the arms: its pixels are cut out of the arms layer
      // and the arm accessories above it, so the leg and foot take layering priority
      if (lg.z >= 3) (LEG_FRONT[`${dir}:${k}`] ??= new Set()).add(q);
    }
    // a band arm in front of the body (z 3 and up) goes into the arms layer; one behind it (the far arm, z below 3) goes
    // into the body layer under the torso, so the body really covers it
    // (decided per pixel, so one arm can be split between the two)
    if (name === 'arms' || name === 'body') for (const sd of Object.keys(d.armBand || {})) {
      const fb = frontalBand(d, k, sd);
      if (!fb) continue;
      const mine = (q) => (fb.zs.get(q) >= 3) === (name === 'arms');
      // the far arm is one shade darker, as in E
      for (const [q, c] of fb.pixels) { if (!mine(q)) continue; const [x, y] = unkey(q), sy = sd === d.far ? farShade[c] : c; items.push([fb.zs.get(q), x, y, sy === 'o' ? BLACK : pal[sy], `band:${sd}`]); }
      // outline: a band arm keeps its own outline wherever it lies over the body or another part (readability and
      // layering), except where it joins the shoulder; outline: false turns it off
      const olv = d.armBand[sd]?.outline, ol = (Array.isArray(olv) ? olv[k] : olv) ?? true;
      if (ol) {
        const pv = d.armBand[sd].pivot, px0 = pv[0] + twistOf(d, k, 'torso', AR.shoulder) + (Array.isArray(d.armBand[sd].pivotDx) ? d.armBand[sd].pivotDx[k] : 0) + rotateArmDx(d, k, sd);
        const py0 = pv[1] + bobOf(d, k) + armDelta(k) + (d.crouch || 0) + viewDrop(d) + (d.variants?.[k] ? variantShear(d, k, pv[0], AR.shoulder, 'torso') : 0);
        for (const q of fb.pixels.keys()) {
          if (!mine(q)) continue;
          const [x, y] = unkey(q);
          for (const [dx2, dy2] of N4) {
            const n = key(x + dx2, y + dy2);
            if (!fb.pixels.has(n) && Math.hypot(x + dx2 + 0.5 - px0, y + dy2 + 0.5 - py0) > 3) items.push([fb.zs.get(q) - 0.5, x + dx2, y + dy2, BLACK, `bandol:${sd}`]);
          }
        }
      }
    }
    const m = new Map(), sm = new Map(), hz = new Set();
    for (const [z, x, y, c, s0] of items.sort((a, c) => a[0] - c[0])) { m.set(key(x, y), c); sm.set(key(x, y), s0); if (d.headZ > 3 && z === d.headZ) hz.add(key(x, y)); else hz.delete(key(x, y)); }
    if (name === 'arms') for (const q of LEG_FRONT[`${dir}:${k}`] || []) { m.delete(q); sm.delete(q); }
    out[name] = m; src[name] = sm;
    if (name === 'body') HEAD_FRONT[`${dir}:${k}`] = hz;
    // band-arm pixels still showing after the layer is drawn (a far arm behind the torso is mostly covered)
    for (const [q, s0] of sm) if (typeof s0 === 'string' && s0.startsWith('band:')) (BAND_SHOWN[`${dir}:${k}:${s0.slice(5)}`] ??= new Set()).add(q);
  }
  // weaponOver (per side, per frame): the band arm's pixels that still show (fill and outline, either layer) are
  // recorded in the helper mask arm-weapon-mask.png, so the weapon tool can draw that hand's blade over the arm while
  // the torso still covers it (N: the arm reaching across in front of the body, seen from behind)
  for (const sd of Object.keys(d.armBand || {})) {
    const wv = d.armBand[sd].weaponOver;
    if (!(Array.isArray(wv) ? wv[k] : wv)) continue;
    const S = (WEAPON_ARM[`${dir}:${k}`] ??= new Set());
    for (const L of [src.body, src.arms]) for (const [q, s0] of L) if (s0 === `band:${sd}` || s0 === `bandol:${sd}`) S.add(q);
  }
  const fig = new Map([...out.body, ...out.arms]), refx = exposedInReference(fx);
  let outlined = 0, fills = 0;
  for (const [p, c] of [...fig]) {
    if (c === BLACK) continue;
    const s0 = out.arms.has(p) ? src.arms.get(p) : src.body.get(p);
    const [x, y] = unkey(p);
    // an edge already open in the reference stays as drawn, unless the edit moved it from above the outline-check
    // rows (where the reference leaves a few loose pixels) down into them
    if (refx.has(s0) && !(unkey(s0)[1] < spec.cleanup.notchFromRow && y >= spec.cleanup.notchFromRow)) continue;
    for (const [dx, dy] of N4) { const q = key(x + dx, y + dy); if (!fig.has(q)) { out.body.set(q, BLACK); fig.set(q, BLACK); outlined++; } }
  }
  // a background pixel boxed in on all 4 sides (where a moved limb's outline meets another) becomes outline
  for (let y = spec.cleanup.notchFromRow; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
    if (!fig.has(key(x, y)) && N4.every(([dx, dy]) => fig.has(key(x + dx, y + dy)))) { out.body.set(key(x, y), BLACK); fig.set(key(x, y), BLACK); fills++; }
  }
  report.frontalOutlineAdded[`${dir}:${k}`] = outlined;
  report.frontalHoleFills[`${dir}:${k}`] = fills;
  return out;
}
for (const dir of Object.keys(FR?.views || {})) {
  const v = FR.views[dir], lift = v.legLift || FR.legLift;
  if (v.legPose) for (const s of ['R', 'L']) {
    if (v.legPose[s].length !== F) throw new Error(`frontal ${dir} ${s} legPose needs ${F} entries`);
    for (const n of v.legPose[s]) if (!v.legPoseRows[n]) throw new Error(`frontal ${dir}: unknown leg pose ${n}`);
    if (Math.max(...bob) + (v.crouch || 0) > (Array.isArray(v.bobRows) ? v.bobRows : v.bobRows[s]).length) throw new Error(`frontal ${dir} needs ${Math.max(...bob) + (v.crouch || 0)} bob rows`);
  }
  for (const s of ['R', 'L']) {
    for (const [n, t] of [['handDy', v.handDy[s]], ['legLift', lift[s]], ...['hipDx', 'footDx', 'handDx'].filter((n) => v[n]).map((n) => [n, v[n][s]])]) {
      if (t.length !== F) throw new Error(`frontal ${dir} ${s} ${n} needs ${F} entries`);
    }
    const needLeg = Math.max(...lift[s].map((l, k) => l + bob[k])), needRep = Math.max(0, ...lift[s].map((l, k) => -(l + bob[k])));
    const needArm = Math.max(...v.handDy[s].map(Math.abs));
    if (!v.legPose && !v.legBand && needLeg > v.legRows[s].length) throw new Error(`frontal ${dir} ${s} leg needs ${needLeg} removable rows`);
    if (!v.legPose && !v.legBand && needRep > (v.legRepeatRows?.[s]?.length || 0)) throw new Error(`frontal ${dir} ${s} leg needs ${needRep} repeatable rows`);
    if (needArm > v.armRows[s].length || needArm > v.armRepeatRows[s].length) throw new Error(`frontal ${dir} ${s} arm needs ${needArm} edit rows`);
  }
}
const frontalFrames = Object.fromEntries(Object.keys(FR?.views || {}).map((dir) => [dir, Array.from({ length: F }, (_, k) => frontalFrame(dir, k))]));

// A mirror swaps the character's sides, so a mirrored direction plays its source half a cycle later (frameShift):
// every direction then has the same anatomical leg forward at the same frame and the walk can switch direction on
// any frame.
const mirrorFrames = (fr) => Object.fromEntries(Object.entries(fr).map(([n, m]) => [n, new Map([...m].map(([p, c]) => { const [x, y] = unkey(p); return [key(FRAME - 1 - x, y), c]; }))]));
const framesFor = (dir) => {
  if (dir === spec.sourceDirection) return srcFrames;
  if (frontalFrames[dir]) return frontalFrames[dir];
  const { from, frameShift = 0 } = mirrors[dir];
  const base = framesFor(from);
  return base.map((_, k) => mirrorFrames(base[(k + frameShift) % F]));
};

// ---- clothing (Layer 2) ------------------------------------------------------------------------------------
// Clothing follows the body it is registered to. Front/back/diagonal views move every clothing pixel exactly like
// the body pixel of the same part (frontalMove). The authored profile view (E) maps each trouser row onto the posed
// leg: thigh and shin rows are resampled onto the pose's thigh and shin rows and shifted by the leg's back edge;
// wrap and shoe follow the ankle (reference-ankle poses) or the shin line and the authored foot (line poses), where a
// toe-down foot is the foot's own shape in the shoe colours. The far trouser leg is the near one on the far pose,
// shaded darker and drawn behind. A mirrored direction whose clothing is not an exact mirror (the Gi was reworked per
// direction) is built from its own clothing frame, flipped through its source's motion. New edges get outline.
const CL = spec.clothing || { layers: [] };
const clothingLayers = CL.layers.map((name) => {
  const l = overlays.layers.find((o) => path.basename(o.partMap, '.png') === name);
  if (!l) throw new Error(`clothing ${name} not in overlays.json`);
  const c = CL[name];
  return { name, img: readPng(path.join(root, l.source)), map: readPng(path.join(rigDir, l.partMap)), aboveArms: l.class === 'component',
    outline: c.outline.slice(1).toLowerCase(), shoe: c.shoe?.slice(1).toLowerCase(),
    gapFill: c.gapFill?.colour.slice(1).toLowerCase(),
    legRows: c.legRows || { wrap: 56, foot: 59 },
    wrap: c.wrap && { ...c.wrap, colours: Object.fromEntries(Object.entries(c.wrap.colours).map(([a, b]) => [a, b.slice(1).toLowerCase()])) },
    trouser: c.trouser && { ...c.trouser, colours: Object.fromEntries(Object.entries(c.trouser.colours).map(([a, b]) => [a, b.slice(1).toLowerCase()])) },
    shade: Object.fromEntries(Object.entries(c.farShade || {}).map(([a, b]) => [a.slice(1).toLowerCase(), b.slice(1).toLowerCase()])) };
});
const swapSide = (p) => (p?.startsWith('R-') ? 'L-' + p.slice(2) : p?.startsWith('L-') ? 'R-' + p.slice(2) : p);
// pixels of a clothing frame seen in the orientation of `geom` (flipped and side-swapped when the frame is a mirror)
function clothingPixels(l, dir, flip) {
  const fx = order.indexOf(dir) * FRAME, out = [];
  for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
    const sx = flip ? FRAME - 1 - x : x;
    if (!opaque(l.img, fx + sx, y)) continue;
    const part = partNear(l.map, fx, sx, y);
    if (!part) throw new Error(`${l.name} ${dir}: pixel ${sx},${y} has no rig part`);
    out.push({ x, y, c: hexAt(l.img, fx + sx, y), part: flip ? swapSide(part) : part, src: key(sx, y) });
  }
  // the outline row closing the bottom of a hanging sash/flap belongs to the flap, so it swings with it
  const at = new Map(out.map((p) => [key(p.x, p.y), p]));
  for (const p of out) {
    if (p.part === 'sash' || (p.c !== l.outline && p.c !== BLACK)) continue;
    if (at.get(key(p.x, p.y - 1))?.part === 'sash') p.part = 'sash';
  }
  return out;
}
const rowsOf = (m) => { const r = {}; for (const p of m.keys()) { const [x, y] = unkey(p); r[y] = Math.min(r[y] ?? 99, x); } return r; };
const nearestRow = (r, t) => { if (r[t] !== undefined) return r[t]; for (let d = 1; d < FRAME; d++) { if (r[t - d] !== undefined) return r[t - d]; if (r[t + d] !== undefined) return r[t + d]; } return 0; };
const refLegBack = (() => {
  const r = {};
  for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) if (nearSide.leg.includes(bodyPart(x, y))) r[y] = Math.min(r[y] ?? 99, x);
  return r;
})();
const resample = (t, t0, t1, s0, s1) => (t1 === t0 ? s0 : s0 + roundHalfEven((t - t0) * (s1 - s0) / (t1 - t0)));
// One posed leg's garment (trouser rows authored on the leg, wrap or boot shaft, shoe): byRow holds the profile
// garment's leg pixels by row (used for the reference ankle block and the flat shoe).
function legGarment(l, items, byRow, isFar, z, pose, legMap) {
  const LR = l.legRows, BODY_WRAP = 56;
    const col = (c) => (isFar ? (l.shade[c] ?? c) : c);
    if (legMap.limb) return kickGarment(l, items, isFar, z, legMap, col);
    const put = (srcRow, t, dx) => { for (const p of byRow[srcRow] || []) items.push([z, p.x + dx, t, col(p.c), p.src]); };
    // Trouser rows are authored on the posed leg: each row spans the leg's outline widened by the reference
    // trouser margins, shaded with the trouser row pattern; the row above the wrap is the hem (outline).
    const T = l.trouser, extent = {};
    for (const p of legMap.keys()) { const [x, y] = unkey(p); const e = (extent[y] ??= [99, -1]); e[0] = Math.min(e[0], x); e[1] = Math.max(e[1], x); }
    const shift = pose.wrapRow - BODY_WRAP, hemRow = LR.wrap + shift - 1;
    // a raised band thigh can rise above the hip row; its trouser starts at the leg's top row
    const legTop = pose.construction === 'band' ? Math.min(...[...legMap.keys()].map((q) => unkey(q)[1])) + 1 : pose.hipRow;
    for (let t = Math.min(pose.hipRow, legTop) - 1; t <= hemRow; t++) {
      const e = extent[t] ?? extent[t + 1] ?? extent[t - 1];
      const x0 = e[0] - T.back, x1 = e[1] + T.front, n = x1 - x0 - 1;
      const hem = t === hemRow, thighRow = t <= pose.kneeRow;
      const half = Math.ceil((n - 2) / 2), pat = hem ? 'a'.repeat(n) : 'd' + 'c'.repeat(half) + 'b'.repeat(n - 2 - half) + (thighRow ? T.thighFront : T.shinFront);
      const row = 'a' + (t === pose.kneeRow + 1 && !hem ? pat.slice(0, 1) + 'd' + pat.slice(2) : pat) + 'a';
      [...row].forEach((c, j) => items.push([z, x0 + j, t, col(T.colours[c]), null]));
    }
    if (pose.construction === 'reference-ankle') {
      for (let sr = LR.wrap; sr < FRAME; sr++) put(sr, sr + shift, pose.ankleX - ankleX);
    } else {
      // wrap rows follow the shin line: each is the leg's wrap span widened by the reference wrap margins,
      // striped with the wrap pattern
      const Wp = l.wrap;
      for (let t = LR.wrap + shift; t <= pose.wrapRow + 2; t++) {
        const e = extent[t], x0 = e[0] - Wp.margin, n = e[1] - e[0] + 2 * Wp.margin - 1;
        const row = 'a' + (Wp.pattern + Wp.fill.repeat(Math.max(0, n - Wp.pattern.length))).slice(0, n) + 'a';
        [...row].forEach((c, j) => items.push([z, x0 + j, t, col(Wp.colours[c]), null]));
      }
      const bot = pose.wrapRow + 2;
      if (pose.foot === 'flat') for (let sr = LR.foot; sr < FRAME; sr++) put(sr, sr + shift, pose.footX - ankleX);
      else L.feet[pose.foot].rows.forEach((row, r) => [...row].forEach((c, j) => {
        if (c !== '.') items.push([z, pose.footX - 1 + (L.feet[pose.foot].dx || 0) + j, bot + 1 + r, col(c === '#' ? l.outline : l.shoe), null]);
      }));
    }
}
// garment on a kick leg, drawn along the limb: the trouser is the thigh and shin bands widened by the reference
// margins (back/front), shaded across the limb back to front like a profile trouser row, ending in a hem line one
// pixel before the wrap; the wrap/boot shaft and the shoe take the leg's own wrap and foot pixels.
function kickGarment(l, items, isFar, z, legMap, col) {
  const T = l.trouser, Wp = l.wrap, { th, sh, kx, ky, wrapLen, seg, section } = legMap.limb, hemU = sh.len - wrapLen - 1;
  // the trouser's back margin tapers from the reference margin at the hip to 1 px at the knee, so a raised or folded
  // thigh is not a block
  const across = (v, half, front, back = T.back) => {
    const lo = -half - back, hi = half + front, n = Math.round(hi - lo), i = Math.floor(v - lo);
    if (i < 0 || i >= n) return null;
    if (i === 0 || i === n - 1) return 'a';
    const m = n - 2, j = i - 1, h = Math.ceil((m - 2) / 2);
    return j === 0 ? 'd' : j === m - 1 ? 'F' : j <= h ? 'c' : 'b';
  };
  for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
    const q = key(x, y), sg = seg.get(q);
    if (sg === 'wrap') { const [, sv] = sh.uv(x, y); items.push([z, x, y, col(Wp.colours[sv < -0.5 ? Wp.pattern : Wp.fill] ?? Wp.colours[Wp.fill]), null]); continue; }
    if (sg === 'foot') { const c = legMap.get(q); items.push([z, x, y, col(c === '#' || c === 'o' ? l.outline : l.shoe), null]); continue; }
    const [tu, tv] = th.uv(x, y), [su, sv] = sh.uv(x, y);
    let c = null;
    // front/back-view legs (section) keep a 1 px margin all along, so a lifted thigh meets the shorts without a step
    const taper = section ? 1 : Math.max(1, roundHalfEven(T.back - (T.back - 1) * Math.max(0, Math.min(1, tu / th.len))));
    if (tu >= -1 && tu <= th.len) c = across(tv, 2.5, 1.5 + T.front, taper);
    if (!c && su >= 0 && su <= hemU) c = su > hemU - 1 ? (across(sv, 2, 1 + T.front) && 'a') : across(sv, 2, 1 + T.front);
    if (!c && Math.hypot(x + 0.5 - kx, y + 0.5 - ky) <= 3.5) c = 'c';
    // (crease legs) a slanted shin leaves bits of leg between the hem and the wrap; they take the wrap colour
    if (!c && legMap.limb.crease && sg && legMap.get(q) !== 'o' && legMap.get(q) !== '#') { items.push([z, x, y, col(Wp.colours[Wp.fill]), null]); continue; }
    if (!c) continue;
    const front = (tu >= -2 && tu <= th.len) ? T.thighFront : T.shinFront;
    items.push([z, x, y, col(T.colours[c === 'F' ? front : c]), null]);
  }
  // front/back-view stance legs (pose.crease): a bent knee gets a short crease on the inside of the bend (along the bisector of the angle
  // between thigh and shin, toward the hip-ankle line)
  if (legMap.limb.crease) {
    const { hip, ankle } = legMap.limb, n = (v) => { const l = Math.hypot(v[0], v[1]); return [v[0] / l, v[1] / l]; };
    const a = n([hip[0] - kx, hip[1] - ky]), b = n([ankle[0] - kx, ankle[1] - ky]), m = [a[0] + b[0], a[1] + b[1]], ml = Math.hypot(m[0], m[1]);
    if (ml > 0.3) for (const t of [1.5, 2.5]) items.push([z + 0.05, Math.floor(kx + m[0] / ml * t), Math.floor(ky + m[1] / ml * t), col(T.colours.d), null]);
  }
}
function posedClothing(l, px, k) {
  const noLag = spec.overlays?.noLagFrames?.includes(k);   // the sash flaps follow the body with no lag on these frames too
  const b = bob[k], cap = b, up = noLag ? cap : Math.min(bob[(k - 1 + F) % F], cap), lo = noLag ? cap : Math.min(bob[(k - 2 + F) % F], up), dyOf = [cap, up, lo];
  const items = [];
  // In the profile the trousers are drawn as one silhouette (the far leg's slivers are its back edge), so every
  // leg pixel forms the trouser that is placed on each posed leg.
  const legPx = px.filter((p) => LIMB[p.part]?.[0] === 'leg');
  const byRow = {}; for (const p of legPx) (byRow[p.y] ??= []).push(p);
  const legRows = Object.keys(byRow).map(Number), top = Math.min(...legRows);
  const LR = l.legRows, BODY_WRAP = 56;   // LR.wrap: first rigid row of the garment's ankle (wrap / boot); LR.foot: first shoe row
  for (const [which, z] of legPx.length ? [['far', 0], ['near', 2]] : []) legGarment(l, items, byRow, which === 'far', z, L.poses[L[which][k]], legPoses[L[which][k]]);
  // Jacket under the reference near arm: the arm swings away from it, so its under-arm shading becomes jacket
  // base colour (the pixel against the jacket's own outline keeps the edge shade).
  const sway = sashSway(spec.sourceDirection, px, k, l);
  const under = CL[l.name].underArm && Object.fromEntries(Object.entries(CL[l.name].underArm).map(([k2, v]) => [k2, v.slice(1).toLowerCase()])), at = new Map(px.map((p) => [key(p.x, p.y), p]));
  const T = leanOf('torso', k, AR.shoulder), nearArm = (y) => armShift(A.near[k])(y) + T, farArm = (y) => armShift(A.far[k])(y) + T;
  // accessories on a band arm: each band pixel takes the accessory pixel of the reference arm at the same place
  // along and across the arm (provisional placement until per-pose accessory variants are authored)
  const armAt = new Map(px.filter((p) => LIMB[p.part]?.[0] === 'arm').map((p) => [key(p.x, p.y), p]));
  for (const [which, z] of [['near', 4], ['far', -1]]) {
    const ap = A[which][k];
    if (ap.construction !== 'band') continue;   // (elbow arms included)
    const ref = bandRef(ap);
    for (const q of bandArm(ap).keys()) {
      const [x, y] = unkey(q), [rx, ry] = ref(x, y), hit = armAt.get(key(rx, ry));
      if (!hit || !nearSide.arm.includes(hit.part)) continue;
      if (which === 'near') items.push([z, x + T, y + DROP + b + armDelta(k), hit.c, hit.src]);
      else items.push([z, x + T, y + DROP + b + armDelta(k), l.shade[hit.c] ?? hit.c, null, 'farArm']);
    }
  }
  for (const p of px) {
    if (LIMB[p.part]?.[0] === 'leg') continue;
    if (LIMB[p.part]?.[0] === 'arm') {
      const near = nearSide.arm.includes(p.part), nr = armRow(A.near[k])(p.y), fr = armRow(A.far[k])(p.y);
      const ny = near ? nr : fr;
      const bandNear = A.near[k].construction === 'band', bandFar = A.far[k].construction === 'band';
      if (ny !== null && !(near ? bandNear : bandFar)) items.push([near ? 4 : -1, p.x + (near ? nearArm : farArm)(p.y), ny + DROP + b + armDelta(k), p.c, p.src]);
      // the far arm is hidden in the profile reference, so its pieces are the near ones on the far arm, shaded
      // darker and kept only where the far arm itself shows
      if (near && fr !== null && !bandFar) items.push([-1, p.x + farArm(p.y), fr + DROP + b + armDelta(k), l.shade[p.c] ?? p.c, null, 'farArm']);
      continue;
    }
    let c = p.c;
    if (under && p.part === 'torso' && refArm.has(key(p.x, p.y)) && c !== l.outline) c = at.get(key(p.x + 1, p.y))?.c === l.outline ? under.edge : under.base;
    const lag = p.part === 'sash' && !isBand(p, l) ? lagOf('sash') : 0;
    const g = leanGroup(p.part, p.y), ln = leanOf(g, k, p.y), ly = leanY(g, p.y);
    if (ly === null) continue;
    items.push([p.part === 'sash' ? 3 : 1, p.x + sway(p) + ln, ly + dyOf[lag], c, p.src]);
    if (p.part === 'sash' && !isBand(p, l) && l.gapFill) items.push([-2, p.x + ln, ly + dyOf[lag], l.gapFill, null, 'backing']);
  }
  return items;
}
function frontalClothing(l, geom, px, k) {
  const d = FR.views[geom], items = [], sway = sashSway(geom, px, k, l);
  // accessories on a band arm: each band pixel takes the view's reference accessory pixel at the same place along
  // and across the arm (as on the E band arms)
  for (const sd of Object.keys(d.armBand || {})) {
    const fb = frontalBand(d, k, sd, geom);
    if (!fb) continue;
    // the accessory's own row span on this arm: a band pixel takes the accessory pixel at the same fraction across it,
    // so the piece keeps its stripes and inner outline lines at the band's thickness
    const acc = px.filter((p) => LIMB[p.part]?.[0] === 'arm' && LIMB[p.part][1] === sd), accRow = {};
    for (const p of acc) (accRow[p.y] ??= []).push(p);
    for (const r of Object.values(accRow)) r.sort((a, b) => a.x - b.x);
    // an accessory shows only on the part of the band arm that is itself visible (not on a far arm behind the torso),
    // and with accessoryTo only up to that many reference rows from the shoulder (no far-hand armour)
    const shown = BAND_SHOWN[`${geom}:${k}:${sd}`] || new Set(), aTo = d.armBand[sd].accessoryTo;
    for (const [q, [ry, f]] of fb.across) {
      const r = accRow[ry];
      if (!r || !shown.has(q) || (aTo !== undefined && ry - d.armBand[sd].pivot[1] > aTo)) continue;
      const x0 = r[0].x, x1 = r[r.length - 1].x, hit = r.find((p) => p.x === x0 + Math.floor(f * (x1 - x0 + 1)));
      if (hit) { const [x, y] = unkey(q); items.push([fb.zs.get(q), x, y, sd === d.far ? (l.shade[hit.c] ?? hit.c) : hit.c, null]); }
    }
  }
  if (d.legBand) {
    // garments on band legs are authored on each leg as in E, from the profile garment's leg rows
    const byRow = {};
    for (const p of clothingPixels(l, spec.sourceDirection, false)) if (LIMB[p.part]?.[0] === 'leg') (byRow[p.y] ??= []).push(p);
    if (Object.keys(byRow).length) for (const lg of frontalLegs(d, k)) legGarment(l, items, byRow, lg.isFar, lg.z, lg.pose, lg.legMap);
  }
  for (const p of px) {
    const part = p.part === 'sash' && isBand(p, l) ? 'pelvis' : p.part;
    const { rows, dx, z } = frontalMove(d, k, part, p.y, p.x);
    for (const ny of rows) {
      for (const wx of widenXs(d, geom, part, p.x, p.y)) items.push([p.part === 'sash' ? 3 : z, wx + dx + sway(p), ny, p.c, p.src]);
      // cloth behind a swinging flap: shows only where the flap swings off the body
      if (p.part === 'sash' && !isBand(p, l) && l.gapFill) items.push([-2, p.x + dx, ny, l.gapFill, null, 'backing']);
    }
  }
  tiptoeFeet(d, k, l.img, order.indexOf(geom) * FRAME, items);
  return items;
}
// The sash's hanging flaps swing from the knot: rows below the knot row shift sideways, growing to sashSway[k] at the
// flaps' lowest row (a pendulum, phased with the step). The band and knot stay with the waist.
// With bandFollowsBody the band and knot (rows down to knotRow) move exactly with the waist; only the flaps lag.
const knotOf = (l) => CL[l.name]?.sashKnotRow ?? CL.sash.knotRow;
const isBand = (p, l) => !!CL.sash?.bandFollowsBody && p.y <= knotOf(l);
function sashSway(geom, px, k, l) {
  const sw = CL.sash, table = sw?.sway?.[geom];
  if (!table) return () => 0;
  if (table.length !== F) throw new Error(`clothing.sash.sway.${geom} has ${table.length} entries; spec has ${F} frames`);
  const rows = px.filter((p) => p.part === 'sash').map((p) => p.y), bottom = Math.max(...rows);
  const knot = knotOf(l);
  return (p) => (p.part === 'sash' && p.y > knot && bottom > knot ? roundHalfEven(table[k] * (p.y - knot) / (bottom - knot)) : 0);
}
const refClothingExposed = {};
function clothingFrame(l, dir, k, fr) {
  const m = mirrors[dir], geom = m ? m.from : dir;
  const flip = !!m, kk = m ? (k + (m.frameShift || 0)) % F : k;
  const px = clothingPixels(l, dir, flip);
  const items = (geom === spec.sourceDirection ? posedClothing(l, px, kk) : frontalClothing(l, geom, px, kk))
    .filter((it) => it[5] !== 'farArm' || FAR_ARM_PX[kk].has(key(it[1], it[2])))
    .filter((it) => it[5] !== 'backing' || fr.body.has(key(flip ? FRAME - 1 - it[1] : it[1], it[2])));
  const layer = new Map(), src = new Map(), headFront = HEAD_FRONT[`${dir}:${k}`];
  // arm accessories (drawn above the arms) give way to a leg kicking toward the viewer, like the arms do
  const legFront = l.aboveArms ? LEG_FRONT[`${geom}:${kk}`] : null;
  for (const [, x, y, c, s0] of items.sort((a, c) => a[0] - c[0])) {
    const X = flip ? FRAME - 1 - x : x;
    if (headFront?.has(key(X, y))) continue;
    if (legFront?.has(key(x, y))) continue;
    layer.set(key(X, y), c); src.set(key(X, y), s0);
  }
  // Under the hanging sash there is no cloth in the reference; where the flaps swing or the legs move out from under
  // it, the uncovered body (skin or shorts) gets the trouser colour, but only between clothing pixels on the same row,
  // so a hand beside the body stays visible.
  let filled = 0;
  // A body outline pixel left showing inside the garment (where hip-shifted leg cloth parts from the waist cloth)
  // is filled too when cloth touches it on both sides or directly above and below (pinholes only, not the gap between legs).
  for (const [p, c] of fr.body) {
    if (layer.has(p) || fr.arms.has(p)) continue;
    const [x, y] = unkey(p);
    if (!l.gapFill || y < CL[l.name].gapFill.fromRow) continue;
    const near = (dx, reach) => Array.from({ length: reach }, (_, i) => i + 1).some((i) => layer.has(key(x + dx * i, y)));
    // cloth (not outline) on both sides: a pinhole; between two outlines it is the gap between the legs, left as is
    const clothAt = (q) => layer.has(q) && layer.get(q) !== l.outline && layer.get(q) !== BLACK;
    const boxed = (clothAt(key(x - 1, y)) && clothAt(key(x + 1, y))) || (clothAt(key(x, y - 1)) && clothAt(key(x, y + 1)));
    if (c === BLACK ? boxed : near(1, 3) && near(-1, 3)) { layer.set(p, l.gapFill); filled++; }
  }
  // In the front/back/diagonal views every body pixel outside the arms belongs to the trunk or legs, so leg or hip
  // skin the garment moved off (it touches cloth) is covered with the gap colour before the outline is drawn.
  if (l.gapFill && geom !== spec.sourceDirection) {
    const skinHex = new Set(Object.entries(pal).filter(([sy]) => 'LmsdD'.includes(sy)).map(([, h]) => h));
    for (const [p, c] of fr.body) {
      if (!skinHex.has(c) || layer.has(p) || fr.arms.has(p)) continue;
      const [x, y] = unkey(p);
      if (y < CL[l.name].gapFill.fromRow) continue;
      if (N4.some(([dx, dy]) => layer.has(key(x + dx, y + dy)) && layer.get(key(x + dx, y + dy)) !== l.outline)) { layer.set(p, l.gapFill); filled++; }
    }
  }
  report.clothingGapFill[`${l.name} ${dir}:${k}`] = filled;
  // outline where clothing newly meets empty space
  const fx = order.indexOf(dir) * FRAME, refKey = `${l.name}:${dir}`;
  if (!refClothingExposed[refKey]) {
    const ref = new Map();
    for (const img of [body, arms, l.img]) for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) if (opaque(img, fx + x, y)) ref.set(key(x, y), hexAt(img, fx + x, y));
    refClothingExposed[refKey] = new Set([...Array(FRAME * FRAME).keys()].map((i) => key(i % FRAME, Math.floor(i / FRAME)))
      .filter((p) => { if (!opaque(l.img, fx + unkey(p)[0], unkey(p)[1])) return false; const [x, y] = unkey(p); return N4.some(([dx, dy]) => !ref.has(key(x + dx, y + dy))); }));
  }
  const fig = new Map([...fr.body, ...fr.arms, ...layer]);
  const closingAdded = new Set();
  let added = 0;
  for (const [p, c] of [...layer]) {
    if (c === l.outline || c === BLACK) continue;
    const s0 = src.get(p);
    if (s0 && refClothingExposed[refKey].has(s0)) continue;
    const [x, y] = unkey(p);
    for (const [dx, dy] of N4) { const q = key(x + dx, y + dy); if (!fig.has(q)) { layer.set(q, l.outline); fig.set(q, l.outline); closingAdded.add(q); added++; } }
  }
  // second pass after the outline: a body pixel still showing between cloth (left/right or above/below) is a
  // pinhole and takes the gap colour
  if (l.gapFill) for (const [p, c] of fr.body) {
    if (c === BLACK || layer.has(p) || fr.arms.has(p)) continue;
    const [x, y] = unkey(p);
    if (y < CL[l.name].gapFill.fromRow) continue;
    if ((layer.has(key(x - 1, y)) && layer.has(key(x + 1, y))) || (layer.has(key(x, y - 1)) && layer.has(key(x, y + 1)))) { layer.set(p, l.gapFill); filled++; }
  }
  report.clothingGapFill[`${l.name} ${dir}:${k}`] = filled;
  // Loose bits between the legs: cloth specks of 1-2 px cut off from the garment, and outline pixels that no
  // longer border any cloth, are removed (lower body only, where moved leg pieces can leave them behind). Bits that
  // are already loose in the reference drawing are kept.
  const looseIn = (m, isCloth) => {
    const out = new Set(), seen = new Set();
    for (const [p] of m) {
      const [, y] = unkey(p);
      if (y < CL.looseFromRow || seen.has(p) || !isCloth(p)) continue;
      const comp = [p], stack = [p]; seen.add(p);
      while (stack.length) { const [cx, cy] = unkey(stack.pop()); for (const [dx, dy] of N4) { const q = key(cx + dx, cy + dy); if (!seen.has(q) && isCloth(q)) { seen.add(q); comp.push(q); stack.push(q); } } }
      if (comp.length <= 2) comp.forEach((q) => out.add(q));
    }
    for (const [p] of m) {
      const [x, y] = unkey(p);
      if (y < CL.looseFromRow || isCloth(p)) continue;
      let any = false;
      for (let dy = -1; dy <= 1 && !any; dy++) for (let dx = -1; dx <= 1 && !any; dx++) if ((dx || dy) && isCloth(key(x + dx, y + dy))) any = true;
      if (!any) out.add(p);
    }
    return out;
  };
  const refLooseKey = `loose:${l.name}:${dir}`;
  if (!refClothingExposed[refLooseKey]) {
    const ref = new Map();
    for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) if (opaque(l.img, fx + x, y)) ref.set(key(x, y), hexAt(l.img, fx + x, y));
    refClothingExposed[refLooseKey] = looseIn(ref, (q) => ref.has(q) && ref.get(q) !== l.outline && ref.get(q) !== BLACK);
  }
  let loose = 0;
  for (let pass = 0; pass < 4; pass++) {
    const drop = [...looseIn(layer, (q) => layer.has(q) && layer.get(q) !== l.outline && layer.get(q) !== BLACK)]
      // only reference pixels left behind (and outline the renderer added around them); authored pieces such as a
      // drawn toe-down shoe are never touched
      .filter((p) => (src.get(p) ? !refClothingExposed[refLooseKey].has(src.get(p)) : closingAdded.has(p)))
      // never uncover the body: a far boot or trouser sliver that still covers a foot or leg stays
      .filter((p) => !fr.body.has(p) || fr.body.get(p) === BLACK);
    if (!drop.length) break;
    for (const p of drop) layer.delete(p);
    loose += drop.length;
  }
  report.clothingOutlineAdded[`${l.name} ${dir}:${k}`] = added;
  report.clothingLooseRemoved[`${l.name} ${dir}:${k}`] = loose;
  return layer;
}
report.clothingOutlineAdded = {}; report.clothingGapFill = {}; report.clothingLooseRemoved = {};

// ---- sheets ---------------------------------------------------------------------------------------------
const W = F * FRAME, H = spec.directions.length * FRAME;
layerNames.push(...clothingLayers.map((l) => l.name));
// ---- expressions and impact FX (optional, per frame) ---------------------------------------------------
// expressions: a facial expression per frame (eyes shut, grimace) drawn in the eye layers: on a listed frame each eye
// layer's pixels are replaced by the named shape, placed at the top-left of that frame's eye pixels (mirrored about the
// eye block in a mirrored direction). Shapes hold only eye, lid, brow and mouth pixels, never skin, so the face under
// them is the untouched body. fx: an effect layer of its own (drawn over every character layer), a named shape per
// frame placed at the eye block plus the shape's own offsets (x toward the facing).
// spec.fx with a layer name is the per-frame shape FX (impact-fx); spec.fx without one is the smear/splash layer below
const EX = spec.expressions, FX = spec.fx?.layer ? spec.fx : null, SFX = spec.fx && !spec.fx.layer ? spec.fx : null;
if (FX) layerNames.push(FX.layer);
function applyFace(dir, k, fr) {
  const m = mirrors[dir], srcDir = m?.from ?? dir, kk = (k + (m?.frameShift || 0)) % F, flip = !!m;
  if (FX) fr[FX.layer] = new Map();
  const eyes = fr[(EX || FX)?.eyeLayers?.[0]];
  if (!eyes || !eyes.size) return;
  const xs = [...eyes.keys()].map((p) => unkey(p)[0]), ys = [...eyes.keys()].map((p) => unkey(p)[1]);
  const ax = flip ? Math.max(...xs) : Math.min(...xs), ay = Math.min(...ys);
  // a shape colour '@dx,dy' keeps the layer's own pixel at that offset (an iris keeps its eye colour)
  const at = (dx, dy) => key(flip ? ax - dx : ax + dx, ay + dy);
  const place = (shape, own = new Map()) => new Map(shape.map(([dx, dy, c]) => [at(dx, dy), c.startsWith('@') ? own.get(at(...c.slice(1).split(',').map(Number))) : c.replace(/^#/, '')]).filter(([, c]) => c));
  const ex = EX?.frames?.[srcDir]?.[kk];
  if (ex) { const sh = EX.shapes[ex]?.[srcDir]; if (!sh) throw new Error(`expression ${ex} has no ${srcDir} shape`); for (const n of EX.eyeLayers) fr[n] = place(sh, fr[n]); }
  const fx = FX?.frames?.[srcDir]?.[kk];
  if (fx) { const sh = FX.shapes[fx]; if (!sh) throw new Error(`fx shape ${fx} not defined`); fr[FX.layer] = place(sh); }
}
const sheets = Object.fromEntries(layerNames.map((n) => [n, Buffer.alloc(W * H * 4)]));
const all = {};
spec.directions.forEach((dir, r) => {
  all[dir] = framesFor(dir).map((fr, k) => ({ ...fr, ...Object.fromEntries(clothingLayers.map((l) => [l.name, clothingFrame(l, dir, k, fr)])) }));
  // borrowed frames: a frame of the source direction may be another state's rendered frame of another direction
  // (a spin passes through the directional bodies); its mirrors take it flipped
  const srcDir = mirrors[dir]?.from ?? dir;
  // borrow.byDirection gives a frontal view its own borrowed frames (the spin passes through different bodies)
  const borrowed = srcDir === spec.sourceDirection ? spec.borrow?.frames : spec.borrow?.byDirection?.[srcDir];
  for (const [kk, b] of Object.entries(borrowed || {})) {
    const other = JSON.parse(fs.readFileSync(path.join(animDir, `${b.state}.json`), 'utf8')), row = other.directions.indexOf(b.dir);
    if (row < 0) throw new Error(`borrow: ${b.state} has no ${b.dir} row`);
    const fr = {};
    for (const n of layerNames) {
      const img = readPng(path.join(animDir, b.state, `${n}.png`)), m = new Map();
      for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
        const sx = b.frame * FRAME + x, sy = row * FRAME + y;
        if (opaque(img, sx, sy)) { const bx = x + (b.dx || 0); if (bx < 0 || bx >= FRAME) throw new Error(`borrow ${kk}: dx pushes pixels out of the frame`); m.set(key(mirrors[dir] ? FRAME - 1 - bx : bx, y + (b.dy || 0)), hexAt(img, sx, sy)); }
      }
      fr[n] = m;
    }
    all[dir][Number(kk)] = fr;
  }
  all[dir].forEach((fr, k) => {
    if (EX || FX) applyFace(dir, k, fr);
    for (const n of layerNames) for (const [p, c] of fr[n]) {
      const [x, y] = unkey(p);
      if (!(x >= 0 && y >= 0 && x < FRAME && y < FRAME)) throw new Error(`${n} ${dir}:${k} leaves the 64x64 frame at ${p}`);
      const i = ((r * FRAME + y) * W + k * FRAME + x) * 4;
      Buffer.from(c + 'ff', 'hex').copy(sheets[n], i);
    }
  });
});

// ---- QC -------------------------------------------------------------------------------------------------
const qc = { mirrorValid, unoutlinedEdges: {}, holes: {}, groundContact: true, offPalette: {}, outlineNotches: {} };
const palette = new Set(Object.values(pal));
const edgeCount = (fig) => [...fig].filter(([p, c]) => { const [x, y] = unkey(p); return y >= spec.cleanup.notchFromRow && c !== BLACK && N4.some(([dx, dy]) => !fig.has(key(x + dx, y + dy))); }).length;
// Unoutlined edge pixels already present in the reference frame (e.g. a stray Arms1 pixel) are not counted against a frame.
const refEdges = (dir) => {
  const fx = order.indexOf(dir) * FRAME, fig = new Map();
  for (const img of [body, arms]) for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) if (opaque(img, fx + x, y)) fig.set(key(x, y), hexAt(img, fx + x, y));
  return edgeCount(fig);
};
qc.referenceEdges = {};
const footLine = (dir) => {
  const fx = order.indexOf(dir) * FRAME, low = {};
  for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
    if (!opaque(body, fx + x, y)) continue;
    const p = colourToPart.get(hexAt(partMap, fx + x, y));
    if (p === 'R-shin-foot' || p === 'L-shin-foot') low[p] = Math.max(low[p] ?? 0, y);
  }
  return Math.min(...Object.values(low));
};
for (const dir of spec.directions) all[dir].forEach((fr, k) => {
  const fig = new Map([...fr.body, ...fr.arms]), id = `${dir}:${k}`;
  qc.referenceEdges[dir] ??= refEdges(dir);
  let holes = 0, notches = 0, off = 0;
  const edges = Math.max(0, edgeCount(fig) - qc.referenceEdges[dir]);
  for (const [, c] of fig) if (!palette.has(c)) off++;
  for (let y = spec.cleanup.notchFromRow; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
    if (fig.has(key(x, y))) continue;
    const n = N4.filter(([dx, dy]) => fig.has(key(x + dx, y + dy))).length;
    if (n === 4) holes++; else if (n === 3) notches++;   // a 3-sided notch is a dent in the outline line (no colour touches it)
  }
  if (edges) qc.unoutlinedEdges[id] = edges;
  if (holes) qc.holes[id] = holes;
  if (notches) qc.outlineNotches[id] = notches;
  if (off) qc.offPalette[id] = off;
  // a planted foot must sit as low as the higher of the reference's two feet (in a diagonal the far foot stands higher)
  // frames listed as airborne (the flight phase of a run) have both feet off the ground
  if (!(spec.airborneFrames || []).includes(k) && Math.max(...[...fig.keys()].map((p) => unkey(p)[1])) < footLine(dir)) qc.groundContact = false;
});
qc.cleanup = report;
qc.pass = Object.values(mirrorValid).every(Boolean) && qc.groundContact
  && !Object.keys(qc.unoutlinedEdges).length && !Object.keys(qc.holes).length && !Object.keys(qc.offPalette).length;

const definition = JSON.stringify({
  schema: 'astro-fighters-character-animation-output/v1',
  body: bodyName, state, status: spec.status, frames: F, fps: spec.fps,
  frameSize: [FRAME, FRAME], pivot: [32, 63],
  sheetLayout: { rows: spec.directions, columns: `frames 0–${F - 1}` },
  layers: Object.fromEntries([...layerNames, ...(spec.arms.farLayer ? ["far-arm"] : []), ...(SFX ? ["fx"] : [])].map((n) => [n, `${n}.png`])),
  pendingLayers: spec.overlays.pending,
  drawOrder: overlays.drawOrder,
  rootMotion: Object.fromEntries(spec.directions.map((d) => [d, spec.rootMotion[d]])),
  ...(spec.clips ? { clips: spec.clips } : {}),
  ...(spec.events ? { events: spec.events } : {}),
  qc
}, null, 2) + '\n';

// arms.farLayer: in the side view the far arm is drawn in the body layer; for paired animations (the clinch) it is
// split out into its own 'far-arm' sheet, so the partner's body can be drawn between it and this body
if (spec.arms.farLayer) {
  const far = Buffer.alloc(W * H * 4), bodyBuf = sheets.body;
  for (const dir of spec.directions) {
    if (FR?.views?.[dir]) continue;
    const m = mirrors[dir], shift = m?.frameShift || 0, r = spec.directions.indexOf(dir);
    for (let k = 0; k < F; k++) {
      const ks = m ? (k + shift) % F : k;
      for (const q of FAR_ARM_PX[ks] || []) {
        let [x, y] = unkey(q); if (m) x = FRAME - 1 - x;
        if (x < 0 || y < 0 || x >= FRAME || y >= FRAME) continue;
        const i = ((r * FRAME + y) * W + k * FRAME + x) * 4;
        bodyBuf.copy(far, i, i, i + 4); bodyBuf.fill(0, i, i + 4);
      }
    }
  }
  sheets['far-arm'] = far;
}
// bodyRotation (per frame): the whole fighter turned about a pivot for a throw (thrown over the hip, upside down, lying).
// Quarter turns only (0, 90, 180, 270 degrees), so every pixel moves whole and none is resampled (locked base-geometry
// rule: no rotation or resampling of parts); all runtime layers take the same mapping and stay registered. angle is
// clockwise on screen in the source direction (a mirrored direction turns the other way); dx/dy move the turned fighter;
// groundSnap drops the frame so the body's lowest pixel sits on the bottom row (hair and clothing follow; a hair layer
// that hangs lower is cut at the frame edge).
// faceFlip (per frame): the fighter turned around (a throw that turns its back in): the frame is mirrored about the
// pivot column, so it faces the other way.
const BR = spec.bodyRotation, FF = spec.faceFlip;
if (BR || FF) {
  const names = Object.keys(sheets);
  for (const dir of spec.directions) {
    if (FR?.views?.[dir]) continue;
    const m = !!mirrors[dir], r = spec.directions.indexOf(dir);
    for (let k = 0; k < F; k++) {
      const a0 = BR?.angle?.[k] || 0;
      if (((a0 % 90) + 90) % 90) throw new Error(`bodyRotation.angle[${k}] = ${a0}: quarter turns only`);
      const q = ((((m ? -a0 : a0) / 90) % 4) + 4) % 4, ddx = (BR?.dx?.[k] || 0) * (m ? -1 : 1), ddy = BR?.dy?.[k] || 0;
      const flip = !!FF?.[k], snap = !!BR?.groundSnap?.[k];
      if (!q && !ddx && !ddy && !flip && !snap) continue;
      const pv = BR?.pivot || [32, 44], px = m ? FRAME - 1 - pv[0] : pv[0], py = pv[1];
      const idx = (x, y) => ((r * FRAME + y) * W + k * FRAME + x) * 4;
      // destination pixel -> source pixel (or -1)
      const map = new Int32Array(FRAME * FRAME).fill(-1);
      for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
        let ux = x - ddx - px, uy = y - ddy - py;
        for (let t = 0; t < q; t++) [ux, uy] = [uy, -ux]; // undo clockwise quarter turns
        let sx = ux + px; const sy = uy + py;
        if (flip) sx = FRAME - 1 - sx;
        if (sx >= 0 && sy >= 0 && sx < FRAME && sy < FRAME) map[y * FRAME + x] = sy * FRAME + sx;
      }
      let shift = 0;
      if (snap) {
        let low = -1;
        for (let i = 0; i < FRAME * FRAME; i++) if (map[i] >= 0 && sheets.body[idx(map[i] % FRAME, Math.floor(map[i] / FRAME)) + 3]) low = Math.floor(i / FRAME);
        if (low >= 0) shift = FRAME - 1 - low;
      }
      for (const nm of names) {
        const b = sheets[nm], cell = Buffer.alloc(FRAME * FRAME * 4);
        for (let i = 0; i < FRAME * FRAME; i++) {
          const ty = Math.floor(i / FRAME) + shift;
          if (map[i] < 0 || ty < 0 || ty >= FRAME) continue;
          const si = idx(map[i] % FRAME, Math.floor(map[i] / FRAME));
          b.copy(cell, (ty * FRAME + (i % FRAME)) * 4, si, si + 4);
        }
        for (let y = 0; y < FRAME; y++) cell.copy(b, idx(0, y), y * FRAME * 4, (y + 1) * FRAME * 4);
      }
    }
  }
}
const outDir = path.join(animDir, state);
// fx (per frame): effect pixels in their own 'fx' sheet, drawn over the fighter; never part of the body geometry.
//   smear  motion streaks for a throw: arcs about the turned fighter's pivot (bodyRotation pivot + dy of that frame),
//          sweeping from 'from' to 'to' degrees (0 = straight up, clockwise in the source direction) at each radius;
//          each streak is a hard 1 px line (radii are paired into 2 px bands); every other band is broken toward the trailing end
//   splash an authored pixel pattern (rows, palette keys) placed with its bottom-left at 'at' (x, bottom row)
if (SFX) {
  const fx = Buffer.alloc(W * H * 4), FP = spec.fx.palette;
  const hex = (h) => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  for (const dir of spec.directions) {
    if (FR?.views?.[dir]) continue;
    const m = !!mirrors[dir], r = spec.directions.indexOf(dir);
    const put = (k, x, y, c) => {
      x = Math.round(x); y = Math.round(y); if (m) x = FRAME - 1 - x;
      if (x < 0 || y < 0 || x >= FRAME || y >= FRAME) return;
      const i = ((r * FRAME + y) * W + k * FRAME + x) * 4, [R, G, B] = hex(c);
      fx[i] = R; fx[i + 1] = G; fx[i + 2] = B; fx[i + 3] = 255;
    };
    for (const e of spec.fx.frames) {
      const k = e.frame;
      if (e.smear) {
        const pv = spec.bodyRotation?.pivot || [32, 44], cx = pv[0] + (spec.bodyRotation?.dx?.[k] || 0), cy = pv[1] + (spec.bodyRotation?.dy?.[k] || 0);
        e.smear.radii.forEach((rad, j) => {
          const span = e.smear.to - e.smear.from, gap = (j >> 1) % 2 ? 0.35 : 0; // every other pair of streaks stops short of the trailing end
          const steps = Math.ceil(Math.abs(span) * Math.PI / 180 * rad * 2);
          for (let t = 0; t <= steps; t++) {
            const f = t / steps; if (f < gap) continue;
            const a = (e.smear.from + span * f) * Math.PI / 180;
            put(k, cx + rad * Math.sin(a), cy - rad * Math.cos(a), f < 0.5 ? FP[e.smear.tail] : FP[e.smear.head]);
          }
        });
      }
      for (const sp of e.splash || []) {
        const rows = spec.fx.patterns[sp.pattern], h = rows.length;
        rows.forEach((row, y) => [...row].forEach((ch, x) => { if (ch !== '.') put(k, sp.at[0] + x, sp.at[1] - (h - 1) + y, FP[ch]); }));
      }
    }
  }
  sheets.fx = fx;
}
const files = { ...Object.fromEntries(Object.entries(sheets).map(([n, buf]) => [`${n}.png`, encodePng(W, H, buf)])), 'animation.json': definition };
// arms.farWeaponOver (per frame): in the side view the far arm is drawn in the body layer, so its showing pixels go
// into the same helper mask (mirrored for a mirrored direction) and the far hand's blade can be drawn over it
const fwo = spec.arms.farWeaponOver;
if (fwo) for (const dir of spec.directions) {
  if (FR?.views?.[dir]) continue;
  const m = mirrors[dir], shift = m?.frameShift || 0;
  for (let k = 0; k < F; k++) {
    const ks = m ? (k + shift) % F : k;
    if (!(Array.isArray(fwo) ? fwo[ks] : fwo)) continue;
    const S = (WEAPON_ARM[`${dir}:${k}`] ??= new Set());
    for (const q of FAR_ARM_PX[ks] || []) { const [x, y] = unkey(q); S.add(m ? key(FRAME - 1 - x, y) : q); }
  }
}
// helper (not a runtime layer): where a weaponOver band arm shows, per direction row and frame column
if (Object.keys(WEAPON_ARM).length) {
  const mask = Buffer.alloc(W * H * 4);
  for (const [id, S] of Object.entries(WEAPON_ARM)) {
    const [dir, k] = id.split(':'), r = spec.directions.indexOf(dir);
    for (const q of S) { const [x, y] = unkey(q); if (x < 0 || y < 0 || x >= FRAME || y >= FRAME) continue; mask.fill(255, ((r * FRAME + y) * W + Number(k) * FRAME + x) * 4, ((r * FRAME + y) * W + Number(k) * FRAME + x) * 4 + 4); }
  }
  files['arm-weapon-mask.png'] = encodePng(W, H, mask);
}
if (flag === '--check') {
  const tmp = path.join(outDir, '.check.png');
  const stale = Object.entries(files).filter(([rel, data]) => {
    const file = path.join(outDir, rel);
    if (!fs.existsSync(file)) return true;
    if (!rel.endsWith('.png')) return fs.readFileSync(file, 'utf8') !== data;
    fs.writeFileSync(tmp, data);
    try { return !readPng(file).px.equals(readPng(tmp).px); } finally { fs.rmSync(tmp, { force: true }); }
  });
  if (stale.length) { console.error(`Animation ${bodyName}/${state} outputs are stale (${stale.map(([r]) => r).join(', ')}); rerun node tools/character-posed.mjs ${bodyName} ${state}`); process.exit(1); }
  if (!qc.pass) { console.error(`Animation ${bodyName}/${state} fails QC: ${JSON.stringify(qc)}`); process.exit(1); }
  console.log(`Animation ${bodyName}/${state} outputs are current and pass QC.`);
} else {
  fs.mkdirSync(outDir, { recursive: true });
  for (const [rel, data] of Object.entries(files)) fs.writeFileSync(path.join(outDir, rel), data);
  console.log(`Wrote ${Object.keys(files).length} files to ${path.relative(root, outDir)}/`);
  console.log(`QC: ${JSON.stringify(qc)}`);
}
