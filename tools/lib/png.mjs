// Minimal dependency-free PNG decoding and pixel statistics for production QA tools.
import fs from 'node:fs';
import zlib from 'node:zlib';

const PNG_SIGNATURE = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);

function paeth(a, b, c) {
  const p = a + b - c;
  const pa = Math.abs(p - a);
  const pb = Math.abs(p - b);
  const pc = Math.abs(p - c);
  if (pa <= pb && pa <= pc) return a;
  if (pb <= pc) return b;
  return c;
}

export function parsePng(filePath) {
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

export function inspect(image) {
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


/** Alpha statistics for one rectangular region (e.g. a 64×64 directional frame). */
export function inspectRegion(image, rx, ry, rw, rh) {
  let opaque = 0, soft = 0, minX = rw, minY = rh, maxX = -1, maxY = -1;
  for (let y = 0; y < rh; y += 1) {
    for (let x = 0; x < rw; x += 1) {
      const a = image.pixels[((ry + y) * image.width + rx + x) * 4 + 3];
      if (!a) continue;
      opaque += 1; if (a !== 255) soft += 1;
      if (x < minX) minX = x; if (y < minY) minY = y; if (x > maxX) maxX = x; if (y > maxY) maxY = y;
    }
  }
  return { opaque, soft, bbox: opaque ? [minX, minY, maxX, maxY] : null };
}

export const alphaAt = (image, x, y) => image.pixels[(y * image.width + x) * 4 + 3];
export const rgbaAt = (image, x, y) => image.pixels.readUInt32BE((y * image.width + x) * 4);

const CRC_TABLE = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n += 1) { let c = n; for (let k = 0; k < 8; k += 1) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
function crc32(buf) { let c = 0xffffffff; for (const b of buf) c = CRC_TABLE[(c ^ b) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; }
function chunk(type, data) {
  const len = Buffer.alloc(4); len.writeUInt32BE(data.length);
  const td = Buffer.concat([Buffer.from(type, 'ascii'), data]);
  const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(td));
  return Buffer.concat([len, td, crc]);
}
/** Encode an 8-bit RGBA image ({width,height,pixels}) as PNG (filter 0, no interlace). */
export function encodePng(image) {
  const { width: w, height: h, pixels } = image;
  const raw = Buffer.alloc((w * 4 + 1) * h);
  for (let y = 0; y < h; y += 1) { raw[y * (w * 4 + 1)] = 0; pixels.copy(raw, y * (w * 4 + 1) + 1, y * w * 4, (y + 1) * w * 4); }
  const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4); ihdr[8] = 8; ihdr[9] = 6;
  return Buffer.concat([PNG_SIGNATURE, chunk('IHDR', ihdr), chunk('IDAT', zlib.deflateSync(raw, { level: 9 })), chunk('IEND', Buffer.alloc(0))]);
}
/** Runtime derivation for near-opaque export artefacts: alpha >= 128 → 255, else 0. RGB is untouched. */
export function snapAlpha(image) {
  const pixels = Buffer.from(image.pixels);
  let changed = 0;
  for (let i = 3; i < pixels.length; i += 4) { const a = pixels[i], n = a >= 128 ? 255 : 0; if (n !== a) { pixels[i] = n; changed += 1; } }
  return { image: { ...image, pixels }, changed };
}
