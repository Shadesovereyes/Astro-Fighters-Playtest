/* Astro Fighters canonical 8-way facing convention.
   Gameplay/runtime authority: S = front, N = back.
   Reference-sheet source slots are remapped explicitly; never infer them by filename. */
(() => {
  "use strict";
  const canonicalToSource = Object.freeze({
    n: "s",
    ne: "se",
    e: "e",
    se: "ne",
    s: "n",
    sw: "nw",
    w: "w",
    nw: "sw"
  });
  const profiles = Object.freeze({
    n: "back",
    ne: "back-right-3q",
    e: "right-profile",
    se: "front-right-3q",
    s: "front",
    sw: "front-left-3q",
    w: "left-profile",
    nw: "back-left-3q"
  });
  const sourceToCanonical = Object.freeze(Object.fromEntries(
    Object.entries(canonicalToSource).map(([canonical, source]) => [source, canonical])
  ));
  window.AF_KAIRO_DIRECTION = Object.freeze({
    order: Object.freeze(["n","ne","e","se","s","sw","w","nw"]),
    front: "s",
    back: "n",
    canonicalToSource,
    sourceToCanonical,
    profiles,
    sourceSlotFor(canonical) { return canonicalToSource[String(canonical).toLowerCase()] || null; },
    canonicalForSource(source) { return sourceToCanonical[String(source).toLowerCase()] || null; }
  });
})();
