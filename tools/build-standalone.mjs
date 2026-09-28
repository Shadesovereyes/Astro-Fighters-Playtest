// Builds a single self-contained HTML file from /docs for offline or sandboxed play.
// Inlines the stylesheet, every local <script src>, and runtime images (as the
// window.AF_ASSET_DATA fallback map the runtime already understands).
//
// Usage: node tools/build-standalone.mjs [output]   (default: dist/astro-fighters-standalone.html)
// The output is a generated artifact; /docs remains the source of truth.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const docs = path.join(root, 'docs');
const out = path.resolve(root, process.argv[2] || 'dist/astro-fighters-standalone.html');

let html = fs.readFileSync(path.join(docs, 'index.html'), 'utf8');
const escScript = (s) => s.replace(/<\/script/gi, '<\\/script');

html = html.replace(/<link rel="stylesheet" href="([^"]+)"\s*\/?>/g, (_, href) =>
  `<style>\n${fs.readFileSync(path.join(docs, href), 'utf8')}\n</style>`);

const assetRoot = path.join(docs, 'assets', 'runtime');
const assets = {};
const mime = { '.png': 'image/png', '.jpg': 'image/jpeg' };
(function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (mime[path.extname(entry.name)]) {
      const rel = path.relative(docs, full).split(path.sep).join('/');
      assets[rel] = `data:${mime[path.extname(entry.name)]};base64,${fs.readFileSync(full).toString('base64')}`;
    }
  }
})(assetRoot);
const assetScript = `<script>\nwindow.AF_ASSET_DATA = Object.assign(window.AF_ASSET_DATA || {}, ${JSON.stringify(assets)});\n</script>`;

let inserted = false;
html = html.replace(/<script src="([^"]+)"><\/script>/g, (_, src) => {
  const tag = `<script>\n${escScript(fs.readFileSync(path.join(docs, src), 'utf8'))}\n</script>`;
  // Asset data must exist before the game runtime resolves asset paths.
  if (!inserted && src === 'js/game.js') { inserted = true; return `${assetScript}\n  ${tag}`; }
  return tag;
});
if (!inserted) throw new Error('js/game.js script tag not found in docs/index.html');

html = `<!-- Astro Fighters — generated standalone build (tools/build-standalone.mjs). Do not edit; edit /docs instead. -->\n${html}`;
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, html);
console.log(`Wrote ${path.relative(root, out)} (${(fs.statSync(out).size / 1024 / 1024).toFixed(2)} MB, ${Object.keys(assets).length} inlined images)`);
