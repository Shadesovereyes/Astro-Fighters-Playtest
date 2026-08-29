import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const manifestPath = path.join(root, 'production', 'asset-manifest.json');
const registryPath = path.join(root, 'docs', 'data', 'shared-foundation-runtime.json');
const launcherPath = path.join(root, 'docs', 'play-v4.html');
const loaderPath = path.join(root, 'docs', 'js', 'shared-foundation-assets-v0.js');

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const registry = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
const launcher = fs.readFileSync(launcherPath, 'utf8');
const loader = fs.readFileSync(loaderPath, 'utf8');
const failures = [];

const fail = (message) => failures.push(message);
const allowed = new Set(registry.allowedActivationStatuses || []);
const manifestAssets = new Map((manifest.activePackage?.worldDependencies || []).map((asset) => [asset.id, asset]));

if (registry.packageId !== manifest.activePackage?.id) {
  fail(`Runtime registry packageId must match active package ${manifest.activePackage?.id}.`);
}

if (!launcher.includes('js/shared-foundation-assets-v0.js')) {
  fail('docs/play-v4.html must load shared-foundation-assets-v0.js after the world refactor.');
}

if (!loader.includes("data/shared-foundation-runtime.json")) {
  fail('Shared-foundation loader must use the guarded runtime registry.');
}

function readPngDimensions(filePath) {
  const bytes = fs.readFileSync(filePath);
  const signature = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  if (bytes.length < 24 || !bytes.subarray(0, 8).equals(signature)) {
    throw new Error('not a PNG');
  }
  return [bytes.readUInt32BE(16), bytes.readUInt32BE(20)];
}

for (const asset of registry.assets || []) {
  const contracted = manifestAssets.get(asset.id);
  if (!contracted) {
    fail(`Registry asset ${asset.id} is not contracted in production/asset-manifest.json.`);
    continue;
  }

  const manifestRuntimePath = contracted.runtimePath.replace(/^docs\//, '');
  if (asset.runtimePath !== manifestRuntimePath) {
    fail(`${asset.id}: registry runtimePath ${asset.runtimePath} must match manifest ${manifestRuntimePath}.`);
  }

  if (JSON.stringify(asset.runtimeCanvas) !== JSON.stringify(contracted.runtimeCanvas)) {
    fail(`${asset.id}: runtimeCanvas must match manifest ${JSON.stringify(contracted.runtimeCanvas)}.`);
  }

  if (asset.status !== contracted.status) {
    fail(`${asset.id}: registry status ${asset.status} must match manifest status ${contracted.status}.`);
  }

  if (!asset.enabled) continue;

  if (!allowed.has(asset.status)) {
    fail(`${asset.id}: enabled assets require runtime-candidate, integrated, or approved status; got ${asset.status}.`);
  }

  const diskPath = path.join(root, 'docs', asset.runtimePath);
  if (!fs.existsSync(diskPath)) {
    fail(`${asset.id}: enabled runtime file is missing at docs/${asset.runtimePath}.`);
    continue;
  }

  try {
    const dimensions = readPngDimensions(diskPath);
    if (JSON.stringify(dimensions) !== JSON.stringify(asset.runtimeCanvas)) {
      fail(`${asset.id}: PNG dimensions ${dimensions.join('x')} do not match contracted ${asset.runtimeCanvas.join('x')}.`);
    }
  } catch (error) {
    fail(`${asset.id}: runtime file failed PNG validation (${error.message}).`);
  }
}

if (registry.reviewState !== 'not-ready-for-art-review' && (registry.assets || []).some((asset) => !asset.enabled)) {
  fail('Registry may not claim an art-review-ready state while benchmark assets remain disabled.');
}

if (failures.length) {
  console.error(`Shared-foundation runtime validation FAILED (${failures.length}):`);
  for (const failure of failures) console.error(`  - ${failure}`);
  process.exit(1);
}

const enabled = (registry.assets || []).filter((asset) => asset.enabled).map((asset) => asset.id);
console.log(`Shared-foundation runtime validation passed. Enabled assets: ${enabled.length ? enabled.join(', ') : 'none (scaffold-only gate remains active)'}.`);
