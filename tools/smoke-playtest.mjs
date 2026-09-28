// Headless browser smoke test for the Phaser playtest under /docs.
// Serves /docs locally, runs the in-game ?selftest suite, drives a short real-time
// input sequence, and optionally captures canvas screenshots.
//
// Usage: node tools/smoke-playtest.mjs [--shots <dir>]
// Requires the `playwright` package (global or local) and a Chromium build.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const here = path.dirname(fileURLToPath(import.meta.url));
const docsRoot = path.resolve(here, '..', 'docs');
const shotsArg = process.argv.indexOf('--shots');
const shotsDir = shotsArg > 0 ? path.resolve(process.argv[shotsArg + 1]) : null;

async function loadPlaywright() {
  try { return await import('playwright'); } catch {}
  const require = createRequire(import.meta.url);
  const { execSync } = await import('node:child_process');
  const globalRoot = execSync('npm root -g').toString().trim();
  return require(path.join(globalRoot, 'playwright'));
}

const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.png': 'image/png', '.jpg': 'image/jpeg', '.json': 'application/json' };
const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://x');
  const file = path.join(docsRoot, decodeURIComponent(url.pathname === '/' ? '/index.html' : url.pathname));
  if (!file.startsWith(docsRoot) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); res.end('not found'); return; }
  res.writeHead(200, { 'content-type': types[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
await new Promise((r) => server.listen(0, r));
const base = `http://127.0.0.1:${server.address().port}`;

const { chromium } = await loadPlaywright();
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const problems = [];
page.on('pageerror', (e) => problems.push(`pageerror: ${e.message}`));
page.on('console', (m) => { if (m.type() === 'error') problems.push(`console: ${m.text()}`); });
page.on('response', (r) => { if (r.status() >= 400) problems.push(`HTTP ${r.status()} ${r.url()}`); });

let failed = false;
try {
  await page.goto(`${base}/index.html?selftest`);
  await page.waitForFunction(() => window.__AF_SELFTEST, null, { timeout: 30000 });
  const result = await page.evaluate(() => window.__AF_SELFTEST);
  for (const r of result.results) console.log(`${r.ok ? 'PASS' : 'FAIL'}  ${r.name}${r.ok ? '' : ` — ${r.error}`}`);
  if (!result.ok) failed = true;

  // Drive real keyboard input: hold a direction and confirm continuous displacement.
  await page.evaluate(() => AF_TEST.enterMap('Imperial Docks'));
  const before = await page.evaluate(() => AF_TEST.getState());
  await page.keyboard.down('d'); await page.waitForTimeout(400); await page.keyboard.up('d');
  const after = await page.evaluate(() => AF_TEST.getState());
  const dx = after.x - before.x;
  console.log(`${dx > 20 && dx < 80 ? 'PASS' : 'FAIL'}  Held input moves player continuously (dx=${dx.toFixed(1)}px in ~400ms)`);
  if (!(dx > 20 && dx < 80)) failed = true;

  if (shotsDir) {
    fs.mkdirSync(shotsDir, { recursive: true });
    const poses = {
      'Imperial Docks': [300, 222], 'Civic Ward': [320, 206], 'Academy': [320, 278], 'Fringe Ward': [200, 250], 'Slice 0': [480, 330],
      'Scale Reference': [330, 180], 'Scale Reference|canal': [650, 330], 'Scale Reference|ruler': [96, 470]
    };
    for (const [name, [x, y]] of Object.entries(poses)) {
      const map = name.split('|')[0];
      await page.evaluate(([m, px, py]) => { AF_TEST.enterMap(m); AF_TEST.teleport(px, py); }, [map, x, y]);
      await page.waitForTimeout(900);
      const file = path.join(shotsDir, `${name.toLowerCase().replace(/\W+/g, '-')}.png`);
      await page.locator('#game-root canvas').screenshot({ path: file });
      console.log(`shot  ${file}`);
    }
  }
} catch (e) {
  failed = true;
  console.error(e);
} finally {
  for (const p of problems) console.log(`WARN  ${p}`);
  if (problems.some((p) => p.startsWith('pageerror'))) failed = true;
  await browser.close();
  server.close();
}
process.exit(failed ? 1 : 0);
