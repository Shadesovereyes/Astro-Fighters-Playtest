// Derives runtime copies under /docs from the committed source folders.
//
//   node tools/sync-runtime-assets.mjs          write runtime copies
//   node tools/sync-runtime-assets.mjs --check  exit 1 if any runtime copy is stale
//
// Paperdolls (docs/js/world/characters.js): byte-identical copies only.
// World modules (docs/js/world/world-modules.js): 'copy' or 'alpha-snap' (see that file).
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import { parsePng, encodePng, snapAlpha } from './lib/png.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const docs = path.join(root, 'docs');
const check = process.argv.includes('--check');
const sandbox = { window: {} };
vm.createContext(sandbox);
for (const f of ['js/world/characters.js', 'js/world/world-modules.js']) vm.runInContext(fs.readFileSync(path.join(docs, f), 'utf8'), sandbox);
const { AF_CHARACTERS: CHARS, AF_WORLD_MODULES: MODS } = sandbox.window;

const jobs = [];
for (const d of Object.values(CHARS.sexes)) {
  for (const sk of Object.values(d.skin)) jobs.push(sk.body, sk.arms);
  for (const k of ['hair', 'eyes']) for (const o of Object.values(d[k])) jobs.push(o.layer);
  for (const o of Object.values(d.outfits)) { jobs.push(o.clothing); if (o.shoulders) jobs.push(o.shoulders); }
}
for (const m of Object.values(MODS)) jobs.push(m);

let stale = 0, written = 0;
for (const j of jobs) {
  const src = path.join(root, j.source), dst = path.join(docs, j.path);
  if (!fs.existsSync(src)) { console.error(`missing source: ${j.source}`); stale += 1; continue; }
  let bytes = fs.readFileSync(src), note = 'copy';
  if (j.derivation === 'alpha-snap') {
    const { image, changed } = snapAlpha(parsePng(src));
    bytes = encodePng(image); note = `alpha-snap (${changed} px)`;
  }
  const same = fs.existsSync(dst) && fs.readFileSync(dst).equals(bytes);
  if (same) continue;
  if (check) { console.error(`stale runtime copy: ${j.path} ← ${j.source}`); stale += 1; continue; }
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  fs.writeFileSync(dst, bytes); written += 1;
  console.log(`wrote ${j.path} ← ${j.source} [${note}]`);
}
if (check && stale) process.exit(1);
console.log(check ? `runtime assets current (${jobs.length})` : `sync complete: ${written} written, ${jobs.length} tracked`);
