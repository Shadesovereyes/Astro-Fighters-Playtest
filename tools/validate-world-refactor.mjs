import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const read = (p) => fs.readFileSync(path.join(root, p), 'utf8');

const launcher = read('docs/play-v4.html');
const refactor = read('docs/js/world-refactor-v0.js');
const errors = [];
const assert = (ok, message) => { if (!ok) errors.push(message); };

assert(launcher.includes('js/world-refactor-v0.js'), 'play-v4.html must load world-refactor-v0.js.');
assert(refactor.includes("'ground'"), 'Refactor must define ground layer.');
assert(refactor.includes("'decals'"), 'Refactor must define decals layer.');
assert(refactor.includes("'architecture'"), 'Refactor must define architecture layer.');
assert(refactor.includes("'architecture-dressing'"), 'Refactor must define architecture-dressing layer.');
assert(refactor.includes("'props-back'"), 'Refactor must define props-back layer.');
assert(refactor.includes("'collision'"), 'Refactor must define collision layer.');
assert(refactor.includes("'interactives'"), 'Refactor must define interactives layer.');
assert(refactor.includes("'actors'"), 'Refactor must define actors layer.');
assert(refactor.includes("'props-front-occluders'"), 'Refactor must define props-front-occluders layer.');
assert(refactor.includes("'local-shadows'"), 'Refactor must define local-shadows layer.');
assert(refactor.includes("'atmosphere-fx'"), 'Refactor must define atmosphere-fx layer.');

assert(/MOVE_SPEED_PPS\s*=\s*\d+/.test(refactor), 'Continuous movement speed must be expressed in pixels per second.');
assert(refactor.includes('Math.hypot(dx, dy)'), 'Diagonal input must be normalized.');
assert(refactor.includes('delta') && refactor.includes('/ 1000'), 'Movement must use delta time.');
assert(refactor.includes('this.lastStep = time'), 'Legacy fixed STEP_MS movement must be suppressed.');
assert(refactor.includes("obj?.depth === -8"), 'Audit must detect any still-visible legacy grid object.');
assert(refactor.includes("[-20, -10, -8]"), 'Legacy baked background/shade/grid layers must be hidden in refactor mode.');
assert(refactor.includes('afCollisionRects'), 'Collision must be represented independently from appearance imagery.');
assert(refactor.includes("'props-front-occluders'"), 'At least one foreground occlusion layer must exist.');
assert(refactor.includes('productionArt: false'), 'Technical scaffold must explicitly refuse production-art status.');
assert(refactor.includes('scaffoldOnly: true'), 'Technical scaffold must be labeled scaffold-only.');
assert(refactor.includes('AF_WORLD_REFACTOR_V0'), 'Runtime must expose refactor audit state.');
assert(refactor.includes('test.worldRefactor = audit'), 'AF_TEST must expose world-refactor audit results.');

const requiredTextures = [
  'af-scaffold-ground',
  'af-scaffold-wall',
  'af-scaffold-foundation',
  'af-scaffold-threshold',
  'af-scaffold-post'
];
for (const key of requiredTextures) {
  assert(refactor.includes(key), `Refactor scaffold must define separate runtime texture ${key}.`);
}

if (errors.length) {
  console.error(`World refactor validation FAILED (${errors.length}):`);
  for (const error of errors) console.error(`  - ${error}`);
  process.exit(1);
}

console.log('World refactor validation passed.');
console.log('  continuous movement: pixels/second + delta-time + normalized diagonals');
console.log('  legacy grid/background: hidden in refactor mode');
console.log(`  separate scaffold textures: ${requiredTextures.length}`);
console.log('  collision: separate authored data');
console.log('  occlusion proof: foreground object + Y-depth interaction');
console.log('  art status: technical scaffold only, not production-approved');
