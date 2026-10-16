// Copies the approved character runtime from the playtest branch into the hex testbed.
// Source: docs/data/characters/<body>.json and docs/assets/characters/<body>/ on a playtest ref
// (default origin/playtest/claude/busy-dirac-ejzeh7, the branch the rig is authored on).
// Destination: web/characters/<body>.json and web/characters/<body>/. Sheets are byte copies;
// nothing is re-rendered or resampled. Asset paths in the JSON are rewritten to be web/-relative.
// Usage: node tools/import-playtest-rig.mjs [body] [ref]
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const body = process.argv[2] || 'male';
const ref = process.argv[3] || 'origin/playtest/claude/busy-dirac-ejzeh7';
const git = (...args) => execFileSync('git', ['-C', root, ...args], { maxBuffer: 1 << 28 });

const commit = git('rev-parse', '--short', ref).toString().trim();
const def = JSON.parse(git('show', `${ref}:docs/data/characters/${body}.json`).toString());
const files = git('ls-tree', '-r', '--full-tree', '--name-only', ref, `docs/assets/characters/${body}/`).toString().trim().split('\n').filter(Boolean);

const outDir = path.join(root, 'web/characters', body);
fs.rmSync(outDir, { recursive: true, force: true });
for (const file of files) {
  const rel = file.slice('docs/assets/characters/'.length);
  const dest = path.join(root, 'web/characters', rel);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.writeFileSync(dest, git('show', `${ref}:${file}`));
}

const rewrite = (v) => typeof v === 'string' ? v.replace(/^assets\/characters\//, 'characters/')
  : Array.isArray(v) ? v.map(rewrite)
  : v && typeof v === 'object' ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, rewrite(x)])) : v;
const out = rewrite(def);
out.source = { ref: ref.replace(/^origin\//, ''), commit, importedBy: 'tools/import-playtest-rig.mjs' };
fs.writeFileSync(path.join(root, 'web/characters', `${body}.json`), JSON.stringify(out) + '\n');
console.log(`imported ${body} from ${ref} @ ${commit}: ${files.length} sheets, ${Object.keys(out.states).length} states`);
