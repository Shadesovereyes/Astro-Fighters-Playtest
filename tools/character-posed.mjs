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
    L.feet[p.foot].rows.forEach((row, r) => [...row].forEach((c, j) => { if (c !== '.') out.set(key(p.footX - 1 + j, bot + 1 + r), c); }));
    closeLeg(out, true);
  } else throw new Error(`unknown leg construction ${p.construction}`);
  pinchFill(out);
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
function buildArm(p) {
  let shift;
  if (p.construction === 'reference') shift = () => 0;
  else if (p.construction === 'pendulum') shift = (y) => roundHalfEven(p.total * (Math.min(y, AR.pendulumRigidFrom) - AR.shoulder) / (AR.pendulumRigidFrom - AR.shoulder));
  else if (p.construction === 'line') {
    const e = (y) => (y <= AR.elbow ? refBack[AR.shoulder] + p.upper * (y - AR.shoulder) / (AR.elbow - AR.shoulder)
      : refBack[AR.shoulder] + p.upper + p.lean * (y - AR.elbow) / (AR.lineHand - AR.elbow));
    shift = (y) => Math.floor(e(Math.min(y, AR.lineHand)) + 0.5) - refBack[Math.min(y, AR.lineHand)];
  } else throw new Error(`unknown arm construction ${p.construction}`);
  if (Math.min(...armRows) < AR.shoulder) throw new Error('reference arm starts above the shoulder row');
  const out = new Map();
  for (const [k, c] of refArm) { const [x, y] = unkey(k); out.set(key(x + shift(y), y), c); }
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

// ---- overlays (hair, eyes) ------------------------------------------------------------------------------
const overlayLayers = spec.overlays.layers.map((name) => {
  const l = overlays.layers.find((o) => path.basename(o.partMap, '.png') === name);
  if (!l) throw new Error(`overlay ${name} not in overlays.json`);
  return { name, img: readPng(path.join(root, l.source)), map: readPng(path.join(rigDir, l.partMap)) };
});
const lagOf = (part) => (part === 'head' ? 0 : overlays.overlayParts?.[part]?.lagFrames);

// ---- frames -------------------------------------------------------------------------------------------
const bob = spec.bob.dy;
const report = { cleanupRemoved: [], cleanupMerged: [], frontalHoleFills: {} };
function frame(k) {
  const b = bob[k];
  const bodyL = new Map(), armsL = new Map();
  const far = legPoses[L.far[k]], near = legPoses[L.near[k]];
  const na = closeArm(buildArm(A.near[k]), (x, y, q) => y < AR.shoulder || bodyRest.has(q));
  const fa = closeArm(buildArm(A.far[k]), (x, y) => y < AR.shoulder);
  for (const [p, c] of far) bodyL.set(p, colourOf(farShade[c]));
  for (const [p, c] of fa) { const [x, y] = unkey(p); bodyL.set(key(x, y + b), colourOf(farShade[c])); }
  const farKeys = new Set(bodyL.keys());
  for (const [p, c] of near) bodyL.set(p, colourOf(c));
  for (const [p, c] of bodyRest) { const [x, y] = unkey(p); bodyL.set(key(x, y + b), colourOf(c)); }
  for (const [p, c] of na) { const [x, y] = unkey(p); armsL.set(key(x, y + b), colourOf(c)); }
  const nearPos = new Set([...near.keys(), ...[...bodyRest.keys(), ...na.keys()].map((p) => { const [x, y] = unkey(p); return key(x, y + b); })]);
  const farPx = new Set([...farKeys].filter((p) => !nearPos.has(p)));
  const comp = () => { const m = new Map(bodyL); for (const [p, c] of armsL) m.set(p, c); return m; };
  let img = comp();
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
  const cap = b, up = Math.min(bob[(k - 1 + F) % F], cap), lo = Math.min(bob[(k - 2 + F) % F], up), dyOf = [cap, up, lo];
  const ov = {};
  for (const l of overlayLayers) {
    const m = new Map();
    for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
      if (!opaque(l.img, ox + x, y)) continue;
      const part = colourToPart.get(hexAt(l.map, ox + x, y)), lag = lagOf(part);
      if (lag === undefined) throw new Error(`${l.name}: pixel ${x},${y} has part ${part}, which has no walk motion`);
      m.set(key(x, y + dyOf[lag]), hexAt(l.img, ox + x, y));
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
for (const [dir, from] of Object.entries(spec.mirror || {})) {
  if (dir === 'rule') continue;
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
const LIMB = { 'R-thigh': ['leg', 'R'], 'R-shin-foot': ['leg', 'R'], 'L-thigh': ['leg', 'L'], 'L-shin-foot': ['leg', 'L'],
  'R-upper-arm': ['arm', 'R'], 'R-forearm-hand': ['arm', 'R'], 'L-upper-arm': ['arm', 'L'], 'L-forearm-hand': ['arm', 'L'] };
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
function frontalFrame(dir, k) {
  const d = FR.views[dir], fx = order.indexOf(dir) * FRAME, b = FR.bob[k];
  const cap = b, up = Math.min(FR.bob[(k - 1 + F) % F], cap), lo = Math.min(FR.bob[(k - 2 + F) % F], up), dyOf = [cap, up, lo];
  const srcLayers = [['body', body, partMap], ['arms', arms, partMap], ...overlayLayers.map((l) => [l.name, l.img, l.map])];
  const out = {};
  for (const [name, img, map] of srcLayers) {
    const m = new Map();
    for (let y = 0; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
      if (!opaque(img, fx + x, y)) continue;
      const part = partNear(map, fx, x, y), limb = LIMB[part];
      let rows;
      if (limb?.[0] === 'leg') rows = rowMap(y, b, d.legRows[limb[1]].slice(0, FR.legLift[limb[1]][k] + b), []);
      else if (limb?.[0] === 'arm') {
        const h = d.handDy[limb[1]][k];
        rows = rowMap(y, b, h < 0 ? d.armRows[limb[1]].slice(0, -h) : [], h > 0 ? d.armRepeatRows[limb[1]].slice(0, h) : []);
      } else if (part === 'head' || overlays.overlayParts?.[part]?.lagFrames !== undefined) rows = [y + dyOf[lagOf(part)]];
      else if (part) rows = [y + b];
      else throw new Error(`${name} ${dir}: pixel ${x},${y} has no rig part`);
      for (const ny of rows) m.set(key(x, ny), hexAt(img, fx + x, y));
    }
    out[name] = m;
  }
  // a background pixel boxed in on all 4 sides (where a moved arm's outline meets the trunk's) becomes outline
  const fig = new Map([...out.body, ...out.arms]);
  let fills = 0;
  for (let y = spec.cleanup.notchFromRow; y < FRAME; y++) for (let x = 0; x < FRAME; x++) {
    if (!fig.has(key(x, y)) && N4.every(([dx, dy]) => fig.has(key(x + dx, y + dy)))) { out.body.set(key(x, y), BLACK); fills++; }
  }
  report.frontalHoleFills[`${dir}:${k}`] = fills;
  return out;
}
for (const dir of Object.keys(FR?.views || {})) {
  const v = FR.views[dir];
  for (const s of ['R', 'L']) {
    if (v.handDy[s].length !== F || FR.legLift[s].length !== F) throw new Error(`frontal ${dir} ${s} tables need ${F} entries`);
    const needLeg = Math.max(...FR.legLift[s].map((l, k) => l + FR.bob[k])), needArm = Math.max(...v.handDy[s].map(Math.abs));
    if (needLeg > v.legRows[s].length) throw new Error(`frontal ${dir} ${s} leg needs ${needLeg} removable rows`);
    if (needArm > v.armRows[s].length || needArm > v.armRepeatRows[s].length) throw new Error(`frontal ${dir} ${s} arm needs ${needArm} edit rows`);
  }
}
const frontalFrames = Object.fromEntries(Object.keys(FR?.views || {}).map((dir) => [dir, Array.from({ length: F }, (_, k) => frontalFrame(dir, k))]));

const framesFor = (dir) => (dir === spec.sourceDirection ? srcFrames : frontalFrames[dir] ? frontalFrames[dir]
  : srcFrames.map((fr) => Object.fromEntries(Object.entries(fr).map(([n, m]) => [n, new Map([...m].map(([p, c]) => { const [x, y] = unkey(p); return [key(FRAME - 1 - x, y), c]; }))]))));

// ---- sheets ---------------------------------------------------------------------------------------------
const W = F * FRAME, H = spec.directions.length * FRAME;
const sheets = Object.fromEntries(layerNames.map((n) => [n, Buffer.alloc(W * H * 4)]));
const all = {};
spec.directions.forEach((dir, r) => {
  all[dir] = framesFor(dir);
  all[dir].forEach((fr, k) => {
    for (const n of layerNames) for (const [p, c] of fr[n]) {
      const [x, y] = unkey(p);
      if (x < 0 || y < 0 || x >= FRAME || y >= FRAME) throw new Error(`${n} ${dir}:${k} leaves the 64x64 frame at ${p}`);
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
  if (![...fig.keys()].some((p) => unkey(p)[1] === FRAME - 1)) qc.groundContact = false;
});
qc.cleanup = report;
qc.pass = Object.values(mirrorValid).every(Boolean) && qc.groundContact
  && !Object.keys(qc.unoutlinedEdges).length && !Object.keys(qc.holes).length && !Object.keys(qc.offPalette).length;

const definition = JSON.stringify({
  schema: 'astro-fighters-character-animation-output/v1',
  body: bodyName, state, status: spec.status, frames: F, fps: spec.fps,
  frameSize: [FRAME, FRAME], pivot: [32, 63],
  sheetLayout: { rows: spec.directions, columns: `frames 0–${F - 1}` },
  layers: Object.fromEntries(layerNames.map((n) => [n, `${n}.png`])),
  pendingLayers: spec.overlays.pending,
  drawOrder: overlays.drawOrder,
  rootMotion: Object.fromEntries(spec.directions.map((d) => [d, spec.rootMotion[d]])),
  qc
}, null, 2) + '\n';

const outDir = path.join(animDir, state);
const files = { ...Object.fromEntries(Object.entries(sheets).map(([n, buf]) => [`${n}.png`, encodePng(W, H, buf)])), 'animation.json': definition };
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
