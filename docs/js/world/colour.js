/* Astro Fighters — OKLCH colour helpers for mechanical palette derivation (eye tints).
   Pure functions; no pixel geometry is created or moved by anything here. */
(() => {
  'use strict';
  const toLin = (c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
  const toSrgb = (c) => (c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055);
  function hexToOklch(hex) {
    const [r, g, b] = [1, 3, 5].map((i) => toLin(parseInt(hex.slice(i, i + 2), 16)));
    const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
    const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
    const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
    const L = 0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s;
    const A = 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s;
    const B = 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s;
    return [L, Math.hypot(A, B), (Math.atan2(B, A) * 180) / Math.PI];
  }
  function oklchToRgb([L, C, H]) {
    const a = C * Math.cos((H * Math.PI) / 180), b = C * Math.sin((H * Math.PI) / 180);
    const l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3, m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3, s = (L - 0.0894841775 * a - 1.291485548 * b) ** 3;
    return [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s, -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s].map(toSrgb);
  }
  /** OKLCH → hex, reducing chroma (never lightness or hue) until the colour is displayable. */
  function oklchToHex([L, C, H]) {
    L = Math.min(1, Math.max(0, L));
    let rgb = oklchToRgb([L, C, H]);
    for (let i = 0; i < 40 && rgb.some((v) => v < -1e-4 || v > 1 + 1e-4); i += 1) { C *= 0.93; rgb = oklchToRgb([L, C, H]); }
    return '#' + rgb.map((v) => Math.round(Math.min(1, Math.max(0, v)) * 255).toString(16).padStart(2, '0')).join('');
  }
  /** Shift measured between a reference pair of shades (light → dark). */
  function measureShift(light, dark) {
    const a = hexToOklch(light), b = hexToOklch(dark);
    return { dL: b[0] - a[0], cMul: a[1] > 1e-6 ? b[1] / a[1] : 1, dH: b[2] - a[2] };
  }
  /** Lighter shade for a chosen darker shade: the reference light→dark shift, reversed. */
  function lightenByShift(dark, shift) {
    const [L, C, H] = hexToOklch(dark);
    return oklchToHex([L - shift.dL, shift.cMul > 1e-6 ? C / shift.cMul : C, H - shift.dH]);
  }
  window.AF_COLOUR = { hexToOklch, oklchToHex, measureShift, lightenByShift };
})();
