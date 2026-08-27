import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'production', 'asset-manifest.json'), 'utf8'));
const PNG_SIGNATURE = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);

function usage(message) {
  if (message) console.error(message);
  console.error('Usage:');
  console.error('  node tools/validate-source-png.mjs world <asset-id> <source|runtime> <png-file>');
  console.error('  node tools/validate-source-png.mjs character <direction> <source|runtime> <png-file> [base|dressed|layer]');
  process.exit(2);
}

function paeth(a, b, c) {
  const p = a + b - c;
  const pa = Math.abs(p - a);
  const pb = Math.abs(p - b);
  const pc = Math.abs(p - c);
  if (pa <= pb && pa <= pc) return a;
  if (pb <= pc) return b;
  return c;
}

function parsePng(filePath) {
  const data = fs.readFileSync(filePath);
  if (data.length < 33 || !data.subarray(0, 8).equals(PNG_SIGNATURE)) throw new Error('Not a valid PNG signature.');

  let offset = 8;
  let ihdr = null;
  const idat = [];

  while (offset + 12 <= data.length) {
    const length = data.readUInt32BE(offset);
    const type = data.toString('ascii', offset + 4, offset + 8);
    const start = offset + 8;
    const end = start + length;
    if (end + 4 > data.length) throw new Error(`Truncated PNG chunk ${type}.`);
    const chunk = data.subarray(start, end);

    if (type === 'IHDR') {
      ihdr = {
        width: chunk.readUInt32BE(0),
        height: chunk.readUInt32BE(4),
        bitDepth: chunk[8],
        colorType: chunk[9],
        compression: chunk[10],
        filter: chunk[11],
        interlace: chunk[12]
      };
    } else if (type === 'IDAT') {
      idat.push(chunk);
    } else if (type === 'IEND') {
      break;
    }
    offset = end + 4;
  }

  if (!ihdr) throw new Error('PNG has no IHDR chunk.');
  if (!idat.length) throw new Error('PNG has no IDAT data.');
  if (ihdr.bitDepth !== 8) throw new Error(`PNG bit depth ${ihdr.bitDepth} is unsupported; production QA requires 8-bit channels.`);
  if (ihdr.colorType !== 6) throw new Error(`PNG color type ${ihdr.colorType} is unsupported; production QA requires RGBA (color type 6).`);
  if (ihdr.compression !== 0 || ihdr.filter !== 0) throw new Error('PNG uses unsupported compression/filter method.');
  if (ihdr.interlace !== 0) throw new Error('Interlaced PNGs are not accepted for production source/runtime assets.');

  const bpp = 4;
  const rowBytes = ihdr.width * bpp;
  const inflated = zlib.inflateSync(Buffer.concat(idat));
  const expectedBytes = ihdr.height * (rowBytes + 1);
  if (inflated.length !== expectedBytes) throw new Error(`Unexpected decompressed PNG size: ${inflated.length}; expected ${expectedBytes}.`);

  const pixels = Buffer.alloc(rowBytes * ihdr.height);
  let src = 0;
  for (let y = 0; y < ihdr.height; y += 1) {
    const filterType = inflated[src++];
    const rowStart = y * rowBytes;
    const prevStart = (y - 1) * rowBytes;
    for (let x = 0; x < rowBytes; x += 1) {
      const raw = inflated[src++];
      const left = x >= bpp ? pixels[rowStart + x - bpp] : 0;
      const up = y > 0 ? pixels[prevStart + x] : 0;
      const upLeft = y > 0 && x >= bpp ? pixels[prevStart + x - bpp] : 0;
      let value;
      switch (filterType) {
        case 0: value = raw; break;
        case 1: value = (raw + left) & 255; break;
        case 2: value = (raw + up) & 255; break;
        case 3: value = (raw + Math.floor((left + up) / 2)) & 255; break;
        case 4: value = (raw + paeth(left, up, upLeft)) & 255; break;
        default: throw new Error(`Unsupported PNG row filter ${filterType} at y=${y}.`);
      }
      pixels[rowStart + x] = value;
    }
  }

  return { ...ihdr, pixels };
}

function inspect(image) {
  let opaque = 0;
  let transparent = 0;
  let softAlpha = 0;
  let minX = image.width;
  let minY = image.height;
  let maxX = -1;
  let maxY = -1;
  const colors = new Set();

  for (let y = 0; y < image.height; y += 1) {
    for (let x = 0; x < image.width; x += 1) {
      const i = (y * image.width + x) * 4;
      const r = image.pixels[i];
      const g = image.pixels[i + 1];
      const b = image.pixels[i + 2];
      const a = image.pixels[i + 3];
      if (a === 0) {
        transparent += 1;
      } else {
        opaque += 1;
        if (a !== 255) softAlpha += 1;
        minX = Math.min(minX, x);
        minY = Math.min(minY, y);
        maxX = Math.max(maxX, x);
        maxY = Math.max(maxY, y);
        colors.add((r << 16) | (g << 8) | b);
      }
    }
  }

  return {
    opaque,
    transparent,
    softAlpha,
    colors: colors.size,
    bbox: opaque ? [minX, minY, maxX, maxY] : null
  };
}

function expectedContract(scope, key, stage) {
  if (!['source', 'runtime'].includes(stage)) usage(`Invalid stage: ${stage}`);
  if (scope === 'world') {
    const dep = manifest.activePackage.worldDependencies.find((item) => item.id === key);
    if (!dep) usage(`Unknown world asset id: ${key}`);
    return {
      label: `${dep.id} — ${dep.name}`,
      dimensions: stage === 'source' ? dep.sourceCanvas : dep.runtimeCanvas,
      requireTransparency: dep.layer !== 'ground',
      contactY: null,
      centerX: null,
      paletteFamilies: dep.palette
    };
  }

  if (scope === 'character') {
    if (!manifest.canonical.directions.includes(key)) usage(`Invalid canonical character direction: ${key}`);
    const ch = manifest.activePackage.characterDependencies;
    return {
      label: `${ch.benchmarkId} — ${key}`,
      dimensions: stage === 'source' ? ch.sourceCanvas : ch.runtimeFrame,
      requireTransparency: true,
      contactY: stage === 'source' ? ch.footContactY : ch.runtimePivot[1],
      centerX: stage === 'source' ? ch.bodyCenter[0] : ch.runtimePivot[0],
      paletteFamilies: ch.paletteFamilies
    };
  }

  usage(`Unknown scope: ${scope}`);
}

const [scope, key, stage, fileArg, characterKind = 'dressed'] = process.argv.slice(2);
if (!scope || !key || !stage || !fileArg) usage();
if (scope === 'character' && !['base', 'dressed', 'layer'].includes(characterKind)) usage(`Invalid character kind: ${characterKind}`);

const contract = expectedContract(scope, key, stage);
const filePath = path.resolve(process.cwd(), fileArg);
const errors = [];
const warnings = [];

let image;
try {
  image = parsePng(filePath);
} catch (error) {
  console.error(`PNG QA FAILED: ${error.message}`);
  process.exit(1);
}

const stats = inspect(image);
const [expectedWidth, expectedHeight] = contract.dimensions;
if (image.width !== expectedWidth || image.height !== expectedHeight) {
  errors.push(`Canvas is ${image.width}×${image.height}; contract requires ${expectedWidth}×${expectedHeight}.`);
}
if (stats.opaque === 0) errors.push('Asset contains no visible pixels.');
if (stats.softAlpha > 0) errors.push(`Asset contains ${stats.softAlpha} pixels with soft alpha; production art requires hard alpha.`);
if (contract.requireTransparency && stats.transparent === 0) errors.push('Asset has no transparent unused pixels.');

if (stats.bbox) {
  const [minX, minY, maxX, maxY] = stats.bbox;
  const touchesEdge = minX === 0 || minY === 0 || maxX === image.width - 1 || maxY === image.height - 1;
  if (touchesEdge && contract.requireTransparency) warnings.push('Opaque bounding box touches a canvas edge; inspect for clipping or neighboring-item contamination.');

  if (scope === 'character') {
    const bboxCenter = (minX + maxX) / 2;
    const tolerance = stage === 'source' ? 60 : 6;
    if (Math.abs(bboxCenter - contract.centerX) > tolerance) warnings.push(`Visible bounding-box center ${bboxCenter.toFixed(1)} is far from shared center x=${contract.centerX}; inspect registration.`);

    if (characterKind !== 'layer') {
      const contactTolerance = stage === 'source' ? 8 : 1;
      if (Math.abs(maxY - contract.contactY) > contactTolerance) warnings.push(`Lowest visible pixel y=${maxY} does not closely match foot/contact authority y=${contract.contactY}; inspect baseline/contact shadow.`);
    }
  }
}

const colorWarning = scope === 'character' ? 96 : 192;
if (stats.colors > colorWarning) warnings.push(`Asset uses ${stats.colors} opaque RGB colors; inspect for accidental anti-aliasing, off-palette colors, or excessive ramps.`);

if (warnings.length) {
  console.warn(`PNG QA warnings (${warnings.length}) for ${contract.label}:`);
  warnings.forEach((warning) => console.warn(`  - ${warning}`));
}

if (errors.length) {
  console.error(`PNG QA FAILED (${errors.length}) for ${contract.label}:`);
  errors.forEach((error) => console.error(`  - ${error}`));
  process.exit(1);
}

console.log(`PNG QA passed: ${contract.label}`);
console.log(`  stage: ${stage}`);
console.log(`  canvas: ${image.width}×${image.height}`);
console.log(`  opaque pixels: ${stats.opaque}`);
console.log(`  transparent pixels: ${stats.transparent}`);
console.log(`  unique opaque RGB colors: ${stats.colors}`);
console.log(`  bounding box: ${stats.bbox ? stats.bbox.join(',') : 'none'}`);
console.log(`  palette/material authority: ${contract.paletteFamilies.join(', ')}`);
