# Astro Fighters — Pixel-Art Source Standard

**Status:** LOCKED production rule  
**Scope:** all character, clothing, equipment, prop, VFX, and environment source art intended to become runtime pixel art.  
**Purpose:** prevent painterly/cel-shaded illustration from being mistaken for valid high-resolution pixel-art source.

---

# 1. Governing Rule

Astro Fighters is a **pixel-art game at both source and runtime stages**.

The 480×640 character source lattice is a high-information pixel-art canvas. It is **not** a concept-art canvas and is **not** permission to use smooth digital painting, airbrushed gradients, anti-aliased linework, painterly brush textures, or cel-shaded illustration that is expected to become pixel art only after reduction.

> **SOURCE PIXEL ART → TARGET PIXEL CLEANUP**
>
> not
>
> **PAINTED ILLUSTRATION → SHRINK → CALL IT PIXEL ART**

---

# 2. Source-Stage Pixel Requirements

Every production source asset must already exhibit:

- deliberate pixel clusters;
- hard, intentional pixel edges;
- controlled stair-step diagonals and curves;
- palette-driven shading rather than smooth RGB interpolation;
- discrete highlight / midtone / shadow ramps;
- material-specific cluster patterns;
- purposeful outline / edge treatment;
- no anti-aliased fringe pixels around silhouettes;
- no painterly soft brushes;
- no blur, glow, bloom, airbrush, or soft-focus rendering used to define the asset;
- no smooth gradient shading that only resolves after downscaling;
- no photographic or illustration texture baked into the sprite;
- no automatic resampling artifacts accepted as authored pixels.

Source resolution may contain **more pixel information** than runtime resolution, but it must still be recognizably authored pixel art when viewed at 100% scale.

---

# 3. Palette Discipline

Source art must use the approved Astro Fighters palette authority or an explicitly approved source palette derived from it.

- no arbitrary continuous RGB color drift;
- no hundreds/thousands of near-duplicate painted colors;
- no anti-aliasing colors created only by interpolation;
- no color-noise texture standing in for pixel detail;
- shadows/highlights must use intentional palette steps;
- metallic, cloth, skin, hair, rope, leather, wood, stone, water, and VFX materials must each retain their approved ramp behavior.

A source image that requires heavy palette quantization before it resembles pixel art is **not** an approved source master.

---

# 4. Scaling / Resampling Rule

For authored pixel assets:

- nearest-neighbor is the default scaling method;
- bilinear, bicubic, Lanczos, diffusion, painterly upscaling, or other smoothing filters may not define final source pixels;
- diagnostic previews may use other resampling only if clearly labeled and never promoted as source authority;
- a mechanically reduced 48×64 image remains a candidate until manual target-pixel cleanup is complete.

The source master must not rely on downsampling to hide soft edges, anatomy errors, color noise, or painterly detail.

---

# 5. Character Source Rule

For character packages such as Kairo:

- all 480×640 body, hair, garment, equipment, hand, footwear, and accessory layers are pixel-art source assets;
- modular layers must satisfy `ASTRO_FIGHTERS_MODULAR_SOURCE_LAYER_INTEGRITY_RULES.md` **and** this pixel-art source standard;
- clean component geometry does not compensate for painterly rendering;
- a component may pass clipping/occlusion QA and still fail source approval if its rendering is not pixel art;
- S, SE, E, NE, N, NW, W, and SW must remain stylistically coherent at the pixel-cluster level.

---

# 6. Automatic Source Failures

The following are automatic failures:

- smooth cel-shaded/anime illustration presented as a sprite source;
- painterly 480×640 character renders with soft edges;
- anti-aliased silhouettes or garment borders;
- high-resolution concept art cropped into modular pieces and called source sprites;
- generative presentation boards whose component images are painted illustrations;
- assets that only look pixel-art-like after aggressive shrinking;
- arbitrary dithering/quantization used to disguise non-pixel source art;
- filtered enlargement of a low-resolution frame masquerading as a 480×640 master;
- acceptance based on labels such as “pixel art,” “480×640,” or “32 colors” embedded inside an image rather than the actual pixels.

---

# 7. Mandatory Source Review

Before `SOURCE PASS`, review the asset at:

1. **100% source scale** — inspect actual cluster construction and edge treatment;
2. **zoomed pixel inspection** — verify hard alpha, palette steps, and absence of smoothing artifacts;
3. **normal assembled composite** — verify the pieces still read as one coherent fighter/world asset;
4. **48×64 candidate** — confirm the source contains the right information to reduce cleanly without depending on blur/averaging.

A valid source must pass both:

- **component / construction integrity**, and
- **pixel-art rendering integrity**.

---

# 8. Review Vocabulary

- **REFERENCE PASS** — visual design target approved; may still be non-production reference art.
- **COMPONENT INTEGRITY PASS** — modular shapes / hidden underlayers are valid.
- **PIXEL SOURCE PASS** — source pixels satisfy the Astro Fighters pixel-art standard.
- **SOURCE PASS** — registration + component integrity + pixel source quality + composite fidelity all pass.
- **RUNTIME PASS** — 48×64 target pixels have been manually cleaned and validated.

No direction may advance on `COMPONENT INTEGRITY PASS` alone.

---

# 9. Immediate Kairo Application

The recent painterly/cel-shaded SE rebuilds are **reference/construction aids only** and are not production source art.

SE remains blocked until its continuous, unclipped component geometry is recreated in the approved Astro Fighters pixel-art language on the shared 480×640 lattice. Only after SE earns both **COMPONENT INTEGRITY PASS** and **PIXEL SOURCE PASS** may it receive `SOURCE PASS` and unblock E.

---

## Locked summary

> **ASTRO FIGHTERS SOURCE ART IS PIXEL ART.**  
> **HIGHER SOURCE RESOLUTION MEANS MORE AUTHORED PIXELS, NOT SMOOTHER PAINTING.**  
> **DOWN-SCALING REFINES PIXEL ART; IT DOES NOT CREATE PIXEL ART FROM ILLUSTRATION.**
