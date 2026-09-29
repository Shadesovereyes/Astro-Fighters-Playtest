// Derives additional paper-doll skin tones as palette swaps of an approved neighbouring tone.
// Geometry is untouched: every pixel keeps its position and alpha; only skin-ramp colours are
// replaced through the explicit tables below. Non-skin colours (outline, shorts, wraps) must be
// listed in KEEP; any other colour fails the run so nothing is recoloured by accident.
//
//   node tools/derive-skin-tones.mjs          write Paperdolls/<Sex>/... Body0/Body3 and Arms0/Arms3
//   node tools/derive-skin-tones.mjs --check  exit 1 if the committed sheets differ from the tables
//
// tone0 (Fair)  ← tone1 (Body1/Arms1): OKLCH L +0.07–0.10, chroma ×0.78, hue +0–4° toward yellow.
// tone3 (Umber) ← tone2 (Body2/Arms2): OKLCH L ×0.8 (floor 0.215), chroma ×0.72, hue +8° toward brown.
// Edit a hex below and re-run to adjust a ramp.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parsePng, encodePng } from './lib/png.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const check = process.argv.includes('--check');
const KEEP = new Set(['#000000', '#ffffff', '#e3e3e3']);
const TONE0 = {
    '#f6a35b': '#ffc187',
    '#f6a15b': '#ffbf86',
    '#c87845': '#d5976e',
    '#9e4a31': '#af6c56',
    '#9d4a31': '#ae6c56',
    '#803712': '#93593e',
    '#70241d': '#84473f',
    '#702219': '#84463c',
    '#70241c': '#84473e',
    '#70231b': '#84473d',
    '#70241b': '#84473d',
    '#663300': '#7b5232',
    '#3f0505': '#552824',
    '#3f0404': '#552723',
    '#400404': '#562823'
  };
const TONE3 = {
    '#b24b36': '#7e3b21',
    '#96392b': '#692d19',
    '#7b2b21': '#562212',
    '#4a1510': '#321006'
  };
const JOBS = [];
for (const sex of ['Male', 'Female']) {
  JOBS.push([`Paperdolls/${sex}/Layer 1 - Base Body/${sex} Base Body1.png`, `Paperdolls/${sex}/Layer 1 - Base Body/${sex} Base Body0.png`, TONE0]);
  JOBS.push([`Paperdolls/${sex}/Layer 3 - Arms/${sex} Arms1.png`, `Paperdolls/${sex}/Layer 3 - Arms/${sex} Arms0.png`, TONE0]);
  JOBS.push([`Paperdolls/${sex}/Layer 1 - Base Body/${sex} Base Body2.png`, `Paperdolls/${sex}/Layer 1 - Base Body/${sex} Base Body3.png`, TONE3]);
  JOBS.push([`Paperdolls/${sex}/Layer 3 - Arms/${sex} Arms2.png`, `Paperdolls/${sex}/Layer 3 - Arms/${sex} Arms3.png`, TONE3]);
}
const hex = (p, i) => '#' + [p[i], p[i + 1], p[i + 2]].map((v) => v.toString(16).padStart(2, '0')).join('');
let bad = 0;
for (const [from, to, table] of JOBS) {
  const img = parsePng(path.join(root, from));
  const px = Buffer.from(img.pixels);
  const unknown = new Set();
  let swapped = 0;
  for (let i = 0; i < px.length; i += 4) {
    if (!px[i + 3]) continue;
    const h = hex(px, i), n = table[h];
    if (n) { px[i] = parseInt(n.slice(1, 3), 16); px[i + 1] = parseInt(n.slice(3, 5), 16); px[i + 2] = parseInt(n.slice(5, 7), 16); swapped += 1; }
    else if (!KEEP.has(h)) unknown.add(h);
  }
  if (unknown.size) { console.error(`${from}: unmapped colours ${[...unknown].join(' ')}`); bad += 1; continue; }
  const bytes = encodePng({ ...img, pixels: px });
  const dst = path.join(root, to);
  if (check) {
    if (!fs.existsSync(dst) || Buffer.compare(parsePng(dst).pixels, px) !== 0) { console.error(`stale: ${to}`); bad += 1; }
    continue;
  }
  fs.writeFileSync(dst, bytes);
  console.log(`wrote ${to} (${swapped} skin px recoloured from ${path.basename(from)})`);
}
if (bad) process.exit(1);
if (check) console.log(`skin tones current (${JOBS.length})`);
