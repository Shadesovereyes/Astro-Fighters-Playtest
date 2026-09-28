// PNG production QA against production/asset-manifest.json.
//
//   node tools/validate-source-png.mjs world <asset-id> <source|runtime> <png>
//   node tools/validate-source-png.mjs sheet <png>                  approved 512×64 base sheet
//   node tools/validate-source-png.mjs overlay <overlay.png> <base.png>
//   node tools/validate-source-png.mjs inspection <native.png> <inspection.png>
//
// Exit code 1 on contract failure; warnings are printed but do not fail.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parsePng, inspect, inspectRegion, alphaAt, rgbaAt } from './lib/png.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'production', 'asset-manifest.json'), 'utf8'));
const scale = manifest.canonical.playerScale;
const [SHEET_W, SHEET_H] = scale.sheetCanvas;
const [FRAME_W, FRAME_H] = scale.frame;

function usage(message) {
  if (message) console.error(message);
  console.error('Usage:');
  console.error('  node tools/validate-source-png.mjs world <asset-id> <source|runtime> <png-file>');
  console.error('  node tools/validate-source-png.mjs sheet <png-file>');
  console.error('  node tools/validate-source-png.mjs overlay <overlay-png> <base-sheet-png>');
  console.error('  node tools/validate-source-png.mjs inspection <native-png> <inspection-png>');
  process.exit(2);
}

const errors = [];
const warnings = [];
const info = [];

function load(file) {
  try { return parsePng(path.resolve(process.cwd(), file)); }
  catch (error) { console.error(`PNG QA FAILED (${file}): ${error.message}`); process.exit(1); }
}

function finish(label) {
  if (warnings.length) {
    console.warn(`PNG QA warnings (${warnings.length}) for ${label}:`);
    warnings.forEach((w) => console.warn(`  - ${w}`));
  }
  if (errors.length) {
    console.error(`PNG QA FAILED (${errors.length}) for ${label}:`);
    errors.forEach((e) => console.error(`  - ${e}`));
    process.exit(1);
  }
  console.log(`PNG QA passed: ${label}`);
  info.forEach((line) => console.log(`  ${line}`));
}

function checkSheetCanvas(image, what) {
  if (image.width !== SHEET_W || image.height !== SHEET_H) errors.push(`${what} is ${image.width}×${image.height}; contract requires ${SHEET_W}×${SHEET_H} (${scale.framesPerSheet} × ${FRAME_W}×${FRAME_H}).`);
}

function frames(image) {
  return scale.frameOrder.map((dir, i) => ({ dir, i, x: i * FRAME_W, ...inspectRegion(image, i * FRAME_W, 0, FRAME_W, FRAME_H) }));
}

function worldMode(key, stage, file) {
  if (!['source', 'runtime'].includes(stage)) usage(`Invalid stage: ${stage}`);
  const dep = manifest.activePackage.worldDependencies.find((item) => item.id === key);
  if (!dep) usage(`Unknown world asset id: ${key}`);
  const image = load(file);
  const stats = inspect(image);
  const [w, h] = stage === 'source' ? dep.sourceCanvas : dep.runtimeCanvas;
  if (image.width !== w || image.height !== h) errors.push(`Canvas is ${image.width}×${image.height}; contract requires ${w}×${h}.`);
  if (stats.opaque === 0) errors.push('Asset contains no visible pixels.');
  if (stats.softAlpha > 0) errors.push(`Asset contains ${stats.softAlpha} soft-alpha pixels; production art requires hard alpha (interpolated edges are prohibited).`);
  const requireTransparency = dep.layer !== 'ground';
  if (requireTransparency && stats.transparent === 0) errors.push('Asset has no transparent unused pixels.');
  if (stats.bbox && requireTransparency) {
    const [minX, minY, maxX, maxY] = stats.bbox;
    if (minX === 0 || minY === 0 || maxX === image.width - 1 || maxY === image.height - 1) warnings.push('Opaque bounding box touches a canvas edge; inspect for clipping or neighboring-item contamination.');
  }
  if (stats.colors > 192) warnings.push(`Asset uses ${stats.colors} opaque RGB colors; inspect for accidental anti-aliasing or off-palette ramps.`);
  warnings.push(`Scale is not proven by canvas size. Test ${dep.id} beside the 64×64 player in the Phaser scale reference scene.`);
  info.push(`canvas: ${image.width}×${image.height}`, `opaque: ${stats.opaque}`, `colors: ${stats.colors}`, `bbox: ${stats.bbox ? stats.bbox.join(',') : 'none'}`);
  finish(`${dep.id} (${stage})`);
}

function sheetMode(file) {
  const image = load(file);
  checkSheetCanvas(image, 'Sheet');
  if (errors.length) finish(file);
  const stats = inspect(image);
  if (stats.softAlpha > 0) errors.push(`Sheet contains ${stats.softAlpha} soft-alpha pixels; approved sheets use hard alpha.`);
  const fr = frames(image);
  const contacts = [];
  for (const f of fr) {
    if (!f.opaque) { errors.push(`Frame ${f.i} (${f.dir}) is empty.`); continue; }
    const [minX, minY, maxX, maxY] = f.bbox;
    if (minX === 0 || maxX === FRAME_W - 1) warnings.push(`Frame ${f.i} (${f.dir}) touches a side edge; inspect for bleed into the neighbouring frame.`);
    const cx = (minX + maxX) / 2;
    if (Math.abs(cx - scale.pivotX) > 8) warnings.push(`Frame ${f.i} (${f.dir}) visible centre x=${cx.toFixed(1)} is far from pivot x=${scale.pivotX}.`);
    contacts.push(maxY);
    info.push(`frame ${f.i} ${f.dir.padEnd(2)} bbox ${f.bbox.join(',')} stature ${maxY - minY + 1}px foot y=${maxY}`);
  }
  if (contacts.length && Math.max(...contacts) - Math.min(...contacts) > 2) warnings.push(`Foot-contact rows vary across frames (${contacts.join(', ')}); confirm the shared ground line.`);
  info.unshift(`canvas ${image.width}×${image.height}; ${fr.length} frames; frame order assumed ${scale.frameOrder.join(' ')} (${scale.frameOrderStatus})`);
  finish(`base sheet ${file}`);
}

function overlayMode(file, baseFile) {
  if (!baseFile) usage('overlay mode needs the base sheet it registers to.');
  const ov = load(file), base = load(baseFile);
  checkSheetCanvas(ov, 'Overlay'); checkSheetCanvas(base, 'Base sheet');
  if (errors.length) finish(file);
  const st = inspect(ov);
  if (st.softAlpha > 0) errors.push(`Overlay contains ${st.softAlpha} soft-alpha pixels; overlays use hard alpha.`);
  if (!st.opaque) errors.push('Overlay contains no visible pixels.');
  const R = 6; // registration tolerance: overlay pixels may extend this far beyond the base silhouette (loose garments)
  let copied = 0, far = 0;
  for (const f of frames(ov)) {
    let fOpaque = 0, fFar = 0;
    for (let y = 0; y < FRAME_H; y += 1) for (let x = f.x; x < f.x + FRAME_W; x += 1) {
      if (!alphaAt(ov, x, y)) continue;
      fOpaque += 1;
      if (alphaAt(base, x, y) && rgbaAt(ov, x, y) === rgbaAt(base, x, y)) copied += 1;
      let near = false;
      for (let dy = -R; dy <= R && !near; dy += 1) for (let dx = -R; dx <= R && !near; dx += 1) {
        const nx = x + dx, ny = y + dy;
        if (nx >= f.x && nx < f.x + FRAME_W && ny >= 0 && ny < FRAME_H && alphaAt(base, nx, ny)) near = true;
      }
      if (!near) { fFar += 1; far += 1; }
    }
    info.push(`frame ${f.i} ${f.dir.padEnd(2)} overlay px ${fOpaque}${fFar ? `, ${fFar} unregistered` : ''}`);
  }
  if (copied > 0) errors.push(`${copied} overlay pixels are exact copies of base pixels; overlays must not carry replacement body/hair/face pixels.`);
  if (far > 0) errors.push(`${far} overlay pixels sit more than ${R}px from the base silhouette; check frame registration.`);
  finish(`overlay ${file} on ${baseFile}`);
}

function inspectionMode(nativeFile, inspFile) {
  if (!inspFile) usage('inspection mode needs the native sheet and the inspection sheet.');
  const nat = load(nativeFile), insp = load(inspFile);
  const k = scale.inspectionScale;
  if (insp.width !== nat.width * k || insp.height !== nat.height * k) errors.push(`Inspection is ${insp.width}×${insp.height}; expected ${nat.width * k}×${nat.height * k} (${k}× integer nearest-neighbour).`);
  else {
    let bad = 0;
    for (let y = 0; y < insp.height && bad < 50; y += 1) for (let x = 0; x < insp.width; x += 1) {
      if (rgbaAt(insp, x, y) !== rgbaAt(nat, Math.floor(x / k), Math.floor(y / k))) { bad += 1; if (bad >= 50) break; }
    }
    if (bad) errors.push(`Inspection pixels differ from the ${k}× nearest-neighbour derivative of the native sheet (${bad}+ mismatches); resampling or edits are prohibited.`);
  }
  info.push(`native ${nat.width}×${nat.height} → inspection ${insp.width}×${insp.height}`);
  finish(`inspection ${inspFile}`);
}

const [mode, a, b, c] = process.argv.slice(2);
if (mode === 'world') { if (!a || !b || !c) usage(); worldMode(a, b, c); }
else if (mode === 'sheet') { if (!a) usage(); sheetMode(a); }
else if (mode === 'overlay') { if (!a) usage(); overlayMode(a, b); }
else if (mode === 'inspection') { if (!a) usage(); inspectionMode(a, b); }
else usage(mode ? `Unknown mode: ${mode}` : undefined);
