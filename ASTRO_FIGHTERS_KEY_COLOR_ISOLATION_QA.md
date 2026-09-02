# Astro Fighters — Key-Color Isolation & Transparency QA

**Status:** LOCKED production QA rule  
**Scope:** all pixel-authored character paper-doll layers, sprites, equipment, props, VFX cutouts, and other production assets that require transparency.  
**Purpose:** make foreground/background separation unambiguous while preventing matte contamination, accidental holes, clipped silhouettes, and false transparency.

---

# 1. Canonical QA Key Color

Use the following mono-color as the default Astro Fighters transparency/isolation review background:

- **QA key color:** `#FF00FF`
- RGB: `255, 0, 255`
- Role: **QA / staging only**
- Production use: **FORBIDDEN**

`#FF00FF` is intentionally outside the current Astro Fighters master palette and is reserved as an unmistakable inspection color. It must never be treated as an approved art color, costume color, VFX color, UI color, palette entry, or runtime sprite color.

If the master palette is ever revised to contain `#FF00FF`, choose and document a new reserved QA key color before continuing isolation work.

---

# 2. Why the Key Color Exists

Checkerboards are useful for general transparency review, but they can visually blend with skin, cloth, outlines, shadows, or matte residue.

The mono-color key background exists to expose:

- background/matte pixels accidentally baked into an asset;
- holes inside body, hair, clothing, weapons, props, or other solid components;
- alpha gaps created by bad segmentation or cleanup;
- clipped contours that incorrectly follow an occluder;
- anti-aliased or interpolated edge pixels / mixles;
- near-background fringe pixels that would be difficult to see over a checkerboard;
- stray isolated pixels outside the intended silhouette.

The key background is a diagnostic surface. It is not part of the asset.

---

# 3. Required Key-Color Review Workflow

For every production asset or modular source layer that uses transparency:

1. keep the actual production file as RGBA with transparent unused pixels;
2. composite the asset over a flat `#FF00FF` QA background;
3. inspect the asset at 100% and nearest-neighbor zoom;
4. verify every intended exterior/negative-space region reads as uninterrupted key color;
5. verify every intended solid component remains fully authored and does **not** reveal key color through accidental holes;
6. verify intended openings — such as the space between separated limbs, open garment regions, sleeve openings, weapon gaps, or genuine holes in an object — reveal the key color cleanly;
7. inspect the silhouette for any magenta-contaminated, pink-blended, semi-transparent, or interpolated fringe pixels;
8. repeat the same review over a checkerboard and an alpha-only mask;
9. only after all three views agree may transparency/isolation be considered clean.

A transparent PNG is not approved merely because its alpha channel exists. The shape of the transparency must be correct.

---

# 4. Hole Classification Rule

Transparency inside an asset must be classified as either intentional or accidental.

## Valid transparency

Examples include:

- air between separated arms and torso;
- air between legs where the pose creates a real gap;
- open haori / coat regions;
- real sleeve or collar openings;
- negative space around a sword/scabbard/cord;
- intentionally perforated or ring-shaped equipment;
- gaps between separate hair locks when the approved silhouette genuinely contains them.

## Invalid transparency

Automatic failures include:

- missing pixels inside a solid torso, limb, hand, head, hair mass, garment panel, pant leg, shoe, sword, scabbard, sash, pouch, or prop;
- holes created by color segmentation rather than physical construction;
- transparency that traces another layer's overlap/occlusion boundary;
- isolated one-pixel or small-pixel holes with no approved structural reason;
- missing outline pixels that expose the QA background through a continuous edge;
- transparent regions created accidentally while removing matte/background colors.

When uncertain, compare against the approved reference/design construction. Do not guess that a hole is intentional simply because it is small.

---

# 5. Exact-Key Removal Rule

If a key-colored staging image is used during extraction or cleanup:

- remove only the **exact reserved key value** after the sprite pixels are already hard-edged;
- do not use broad color tolerance that could erase legitimate nearby art colors;
- do not use feathering, soft selection, anti-aliasing, or chroma-key blending;
- any near-key edge colors created by interpolation are **mixles** and must be manually removed/re-authored rather than accepted;
- final transparent pixels must have RGB zeroed or otherwise normalized according to the pipeline so hidden matte RGB does not survive under alpha zero;
- final sprite alpha is hard `0/255` unless an explicitly approved translucent VFX contract says otherwise.

The key color is a review aid, not a substitute for authored alpha.

---

# 6. Paper-Doll Specific Rule

For character paper-doll assets, run the key-color test on:

- base body/underlayer;
- hair back/front;
- inner top;
- pants / lower garment;
- footwear;
- outerwear back/front/near/far pieces;
- hands/cuffs;
- sash / belt / ties;
- weapons / scabbards / cords;
- accessories;
- assembled character composite.

Each layer must be reviewed individually before the full stack is accepted.

For hidden-underlayer QA, remove the occluding upper layer and review the newly exposed lower component over `#FF00FF`. Hidden continuation must remain solid where the physical component continues; the key color must not expose an amputated or clipped visibility slice.

---

# 7. Required QA Views

Before `COMPONENT INTEGRITY PASS`, `PIXEL SOURCE PASS`, or `SOURCE PASS`, retain diagnostic views sufficient to inspect:

1. **key-color view** — actual production pixels over `#FF00FF`;
2. **checkerboard view** — general alpha/edge readability;
3. **alpha-mask view** — binary silhouette/opening structure;
4. **nearest-neighbor pixel zoom** — actual pixel boundaries, not smoothed display pixels;
5. **occluder-toggle view** for modular overlaps.

A contact sheet may include these views, but it must not crop the full nontransparent alpha extent of the asset.

---

# 8. Automatic Failures

The following automatically fail transparency/isolation QA:

- any `#FF00FF` pixel in a final production asset;
- any near-magenta interpolation fringe caused by key-color compositing/removal;
- any matte/background color occupying air around the asset;
- any accidental key-color hole inside a solid component during review;
- any hidden RGB/matte contamination that becomes visible under transformation/compositing;
- any mixle or partial-alpha sprite edge where hard alpha is required;
- any contact/review image that hides, crops, or makes the transparency defect difficult to inspect.

---

# 9. Gate Language

Use these terms precisely:

- **KEY-COLOR QA PASS** — no matte contamination, accidental holes, key-color residue, or edge mixles found in the reviewed asset.
- **ALPHA-MASK PASS** — transparent/opaque structure matches the approved component construction.
- **COMPONENT INTEGRITY PASS** — includes required key-color and alpha-mask review plus hidden-underlayer/occluder-toggle integrity.

`KEY-COLOR QA PASS` alone does not imply `SOURCE PASS`; it is one mandatory input to the larger source gate.

---

## Locked summary

> **USE A FORBIDDEN MONO-COLOR TO MAKE TRANSPARENCY ERRORS OBVIOUS.**  
> **THE KEY COLOR IS QA-ONLY AND MUST NEVER SHIP.**  
> **OUTSIDE THE ASSET = KEY COLOR IN REVIEW / TRANSPARENT IN PRODUCTION.**  
> **INSIDE A SOLID COMPONENT = AUTHORED PIXELS, NOT ACCIDENTAL HOLES.**  
> **CHECK KEY COLOR + CHECKERBOARD + ALPHA MASK + PIXEL ZOOM BEFORE APPROVAL.**
