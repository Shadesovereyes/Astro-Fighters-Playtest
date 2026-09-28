// Validates runtime world data and character-sheet contracts against the production manifest.
//
//   node tools/validate-world-data.mjs
//
// Checks: player-scale mirror vs manifest, approved sheet + overlay registry (512×64, eight
// 64×64 frames, hard alpha, byte-identical Paperdolls copies, full registration), authored world
// module registry, map integrity (bounds, collisions, exits, arrivals, placements, layers),
// and Slice 0 scaffold proportions against the player-relative scale guide.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import { parsePng, inspect, inspectRegion, alphaAt, rgbaAt } from './lib/png.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const docs = path.join(root, 'docs');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'production/asset-manifest.json'), 'utf8'));
const ps = manifest.canonical.playerScale;

const errors = [];
const notes = [];
const fail = (m) => errors.push(m);
const assert = (c, m) => { if (!c) fail(m); };
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);

// Load browser world-data scripts in a sandbox.
const sandbox = { window: {}, document: { createElement: () => { throw new Error('canvas not available in validator'); } }, console };
vm.createContext(sandbox);
for (const f of ['js/world/scaffold-textures.js', 'js/world/scale-guide.js', 'js/world/characters.js', 'js/world/maps.js']) {
  vm.runInContext(fs.readFileSync(path.join(docs, f), 'utf8'), sandbox, { filename: f });
}
const { AF_SCALE: SCALE, AF_CHARACTERS: CHARS, AF_WORLD: WORLD, AF_SCAFFOLD: SCAFFOLD } = sandbox.window;
const docPath = (rel) => path.join(docs, rel);

/* ---- player scale contract ---- */
assert(same(ps.sheetCanvas, [512, 64]) && same(ps.frame, [64, 64]) && ps.framesPerSheet === 8, 'Manifest playerScale must lock a 512×64 sheet of eight 64×64 frames.');
assert(same(ps.inspectionCanvas, [5120, 640]) && ps.inspectionScale === 10, 'Manifest inspection contract must be 10× = 5120×640.');
assert(ps.frame[0] * ps.framesPerSheet === ps.sheetCanvas[0] && ps.frame[1] === ps.sheetCanvas[1], 'Sheet canvas must equal framesPerSheet contiguous frames.');
assert(same(SCALE.player.sheetCanvas, ps.sheetCanvas), 'scale-guide.js sheetCanvas drifted from manifest.');
assert(same(SCALE.player.frame, ps.frame), 'scale-guide.js frame drifted from manifest.');
assert(SCALE.player.framesPerSheet === ps.framesPerSheet, 'scale-guide.js framesPerSheet drifted from manifest.');
assert(same(SCALE.player.frameOrder, ps.frameOrder), 'scale-guide.js frameOrder drifted from manifest.');
assert(SCALE.player.pivotX === ps.pivotX, 'scale-guide.js pivotX drifted from manifest.');
assert(same([SCALE.player.collision.w, SCALE.player.collision.h], ps.collision.size), 'scale-guide.js player collision drifted from manifest.');
assert(ps.collision.independentOfSprite === true && ps.collision.size[0] < ps.frame[0], 'Player collision must be authored independently of (and smaller than) the sprite frame.');
assert(SCALE.player.interactionRange === ps.interactionRange, 'scale-guide.js interactionRange drifted from manifest.');
assert(fs.existsSync(path.join(root, ps.scaleReference)), `Scale reference ${ps.scaleReference} is missing.`);
for (const [k, g] of Object.entries(SCALE.guide)) assert(g.r > 0 && g.tol > 0 && g.label, `Scale guide entry ${k} is incomplete.`);

/* ---- character sheets (Paperdolls registry) ---- */
const [FW, FH] = ps.frame;
const ch = manifest.activePackage.characterDependencies;
const pd = ch.paperdolls;
assert(same(CHARS.frameOrder, ps.frameOrder), 'characters.js frameOrder must equal manifest playerScale.frameOrder.');
assert(same(CHARS.drawOrder, pd.drawOrder), 'characters.js drawOrder must equal manifest paperdolls.drawOrder.');
assert(CHARS.starterOutfit === pd.starterOutfit, 'characters.js starterOutfit must equal manifest.');
const sheets = new Map();
function loadSheet(ref, label) {
  const rt = docPath(ref.path), src = path.join(root, ref.source);
  if (!fs.existsSync(rt)) { fail(`${label}: runtime file missing ${ref.path}`); return null; }
  if (!fs.existsSync(src)) { fail(`${label}: source missing ${ref.source}`); return null; }
  if (!ref.source.startsWith(pd.sourceRoot)) fail(`${label}: source must live under ${pd.sourceRoot}`);
  if (!fs.readFileSync(src).equals(fs.readFileSync(rt))) fail(`${label}: runtime copy is not byte-identical to ${ref.source} (edits/resampling prohibited).`);
  const img = parsePng(rt);
  if (img.width !== ps.sheetCanvas[0] || img.height !== ps.sheetCanvas[1]) { fail(`${label} is ${img.width}×${img.height}; must be ${ps.sheetCanvas.join('×')}.`); return null; }
  const st = inspect(img);
  if (st.softAlpha) fail(`${label} has ${st.softAlpha} soft-alpha pixels.`);
  sheets.set(ref.source, img);
  return img;
}
const registered = new Set();
let stature = null;
for (const [sex, d] of Object.entries(CHARS.sexes)) {
  const bodies = [];
  for (const [id, sk] of Object.entries(d.skin)) {
    for (const part of ['body', 'arms']) {
      registered.add(sk[part].source);
      const img = loadSheet(sk[part], `${sex} ${part} ${id}`);
      if (img && part === 'body') {
        bodies.push(img);
        ps.frameOrder.forEach((dir, i) => { const r = inspectRegion(img, i * FW, 0, FW, FH); if (!r.opaque) fail(`${sex} body ${id} frame ${i} (${dir}) is empty.`); });
        if (sex === 'male' && id === Object.keys(d.skin)[0]) { const r = inspectRegion(img, ps.frameOrder.indexOf('S') * FW, 0, FW, FH); stature = r.bbox[3] - r.bbox[1] + 1; }
      }
    }
  }
  const overlays = [];
  for (const k of ['hair', 'eyes']) for (const [id, o] of Object.entries(d[k])) overlays.push([`${sex} ${k} ${id}`, o.layer]);
  for (const [id, o] of Object.entries(d.outfits)) {
    overlays.push([`${sex} clothing ${id}`, o.clothing]);
    if (o.shoulders) overlays.push([`${sex} shoulders ${id}`, o.shoulders]);
    const avail = pd.outfitAvailability?.[id];
    assert(avail?.includes(sex), `outfit ${id} registered for ${sex} but manifest outfitAvailability does not list it.`);
  }
  for (const [label, ref] of overlays) {
    registered.add(ref.source);
    const img = loadSheet(ref, label);
    if (!img) continue;
    // Overlays must not carry replacement base-body pixels (compared against every skin tone).
    let copied = 0;
    for (const body of bodies) for (let y = 0; y < img.height; y += 1) for (let x = 0; x < img.width; x += 1) {
      if (alphaAt(img, x, y) && alphaAt(body, x, y) && rgbaAt(img, x, y) === rgbaAt(body, x, y)) copied += 1;
    }
    if (copied) notes.push(`${label}: ${copied} px match base-body colour at the same position (inspect for copied base pixels)`);
  }
}
for (const [id, sexes] of Object.entries(pd.outfitAvailability || {})) for (const sex of sexes) assert(CHARS.sexes[sex]?.outfits?.[id], `manifest lists outfit ${id} for ${sex} but characters.js has no layers for it.`);
const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
for (const f of walk(path.join(root, pd.sourceRoot))) if (f.endsWith('.png')) {
  const rel = path.relative(root, f).split(path.sep).join('/');
  if (!registered.has(rel)) fail(`Paperdolls sheet ${rel} is not registered in characters.js.`);
}
for (const [sex, b] of Object.entries(ch.baseSheets)) assert(Object.values(CHARS.sexes[sex]?.skin || {}).some((sk) => sk.body.source === b.sourcePath && `docs/${sk.body.path}` === b.runtimePath), `manifest baseSheets.${sex} must match a registered body sheet.`);
notes.push(`stature S=${stature}px measured from the male base body (south frame)`);
notes.push(`${registered.size} Paperdolls sheets registered; runtime copies byte-identical`);

/* ---- world modules ---- */
const deps = new Map(manifest.activePackage.worldDependencies.map((d) => [d.id, d]));
for (const [id, spec] of Object.entries(SCAFFOLD.SPECS)) if (deps.has(id)) assert(same(spec, deps.get(id).runtimeCanvas), `scaffold ${id} canvas ${spec} must equal manifest runtimeCanvas ${deps.get(id).runtimeCanvas}.`);
for (const [id, rel] of Object.entries(WORLD.authoredModules || {})) {
  const dep = deps.get(id);
  if (!dep) { fail(`authoredModules registers unknown id ${id}.`); continue; }
  assert(`docs/${rel}` === dep.runtimePath, `authored module ${id} path must equal manifest runtimePath.`);
  if (!fs.existsSync(docPath(rel))) { fail(`authored module ${id} file missing: ${rel}`); continue; }
  const img = parsePng(docPath(rel));
  assert(img.width === dep.runtimeCanvas[0] && img.height === dep.runtimeCanvas[1], `authored module ${id} is ${img.width}×${img.height}; manifest requires ${dep.runtimeCanvas.join('×')}.`);
  assert(inspect(img).softAlpha === 0, `authored module ${id} has soft alpha.`);
}
for (const m of Object.values(WORLD.MAPS)) if (m.backdrop) assert(fs.existsSync(docPath(m.backdrop)), `backdrop missing: ${m.backdrop}`);

/* ---- map integrity ---- */
const layers = manifest.canonical.worldLayerOrder;
const HW = ps.collision.size[0] / 2, FHh = ps.collision.size[1];
const hits = (map, x, y) => {
  const b = { x: x - HW, y: y - FHh, w: HW * 2, h: FHh };
  if (b.x < 0 || b.y < 0 || b.x + b.w > map.width || b.y + b.h > map.height) return 'out of bounds';
  const c = (map.colliders || []).find((r) => b.x < r.x + r.w && b.x + b.w > r.x && b.y < r.y + r.h && b.y + b.h > r.y);
  return c ? `inside collider ${JSON.stringify(c)}` : null;
};
const inZone = (z, x, y) => x >= z.x - 10 && x <= z.x + z.w + 10 && y >= z.y - 10 && y <= z.y + z.h + 10;
for (const [name, map] of Object.entries(WORLD.MAPS)) {
  assert(map.width > 0 && map.height > 0, `${name}: needs width/height.`);
  for (const c of map.colliders || []) assert(c.x >= 0 && c.y >= 0 && c.x + c.w <= map.width && c.y + c.h <= map.height && c.w > 0 && c.h > 0, `${name}: collider out of bounds ${JSON.stringify(c)}`);
  const pts = [['spawn', map.spawn], ...Object.entries(map.arrivals || {}).map(([k, v]) => [`arrival ${k}`, v])];
  for (const [label, pt] of pts) { const h = hits(map, pt.x, pt.y); assert(!h, `${name}: ${label} (${pt.x},${pt.y}) ${h}.`); }
  for (const a of [...(map.npcs || []), ...(map.enemies || []), ...(map.interactables || [])]) {
    if (map.interactables?.includes(a)) continue; // interactables may sit on architecture
    const h = hits(map, a.x, a.y); assert(!h, `${name}: ${a.id} (${a.x},${a.y}) ${h}.`);
  }
  for (const e of map.exits || []) {
    const target = WORLD.MAPS[e.target];
    if (!target) { fail(`${name}: exit ${e.id} targets unknown map ${e.target}.`); continue; }
    const arr = target.arrivals?.[e.arrive];
    assert(arr, `${name}: exit ${e.id} arrival '${e.arrive}' missing in ${e.target}.`);
    if (arr) for (const z of target.exits || []) if (z.auto) assert(!inZone(z, arr.x, arr.y), `${name}: arrival '${e.arrive}' lands inside auto exit ${z.id} of ${e.target} (would bounce).`);
  }
  for (const p of map.placements || []) {
    assert(layers.includes(p.layer), `${name}: placement ${p.tex} uses noncanonical layer ${p.layer}.`);
    assert(SCAFFOLD.SPECS[p.tex] || WORLD.authoredModules?.[p.tex], `${name}: placement ${p.tex} has no module.`);
  }
  for (const g of map.guideItems || []) assert(SCALE.items[g.item], `${name}: unknown guide item ${g.item}.`);
  if (map.proportions) for (const [k, v] of Object.entries(map.proportions)) {
    assert(SCALE.guide[k], `${name}: proportion ${k} is not in the scale guide.`);
    if (SCALE.guide[k]) assert(SCALE.within(k, v, stature), `${name}: ${k}=${v}px is ${(v / stature).toFixed(2)}S; guide ${SCALE.guide[k].r}S ±${Math.round(SCALE.guide[k].tol * 100)}%.`);
  }
}

if (errors.length) {
  console.error(`World data validation FAILED (${errors.length}):`);
  errors.forEach((e) => console.error(`  - ${e}`));
  process.exit(1);
}
console.log('World data validation passed.');
notes.forEach((n) => console.log(`  note: ${n}`));
console.log(`  maps: ${Object.keys(WORLD.MAPS).length}; player collision ${ps.collision.size.join('×')}; frame ${ps.frame.join('×')}`);
