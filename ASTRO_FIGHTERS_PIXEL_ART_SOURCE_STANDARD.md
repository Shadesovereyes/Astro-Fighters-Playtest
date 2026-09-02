# Astro Fighters — Pixel-Art Source Standard

**Status:** LOCKED production rule  
**Scope:** all character, clothing, equipment, prop, VFX, and environment source art intended to become runtime/in-game pixel art.  
**Purpose:** clearly separate permissive reference-art rendering from the mandatory pixel-art standard for production game assets.

---

# 1. Governing Rule

Astro Fighters is a **pixel-art game**, but its **reference material is not required to be pixel art**.

Polished illustration, cel-shaded art, painted turnarounds, anatomy studies, garment-construction studies, equipment studies, material studies, and other high-fidelity non-pixel images are allowed when they are used strictly as **reference material**.

Anything identified for actual game use — including a modular source layer, source master, sprite sheet, runtime frame, Phaser asset, animation frame, prop, VFX asset, environment module, or any file intended to ship in gameplay — must already be **true pixel art** at its production stage.

The 480×640 character source lattice is therefore a high-information **pixel-art production canvas**, not a concept-art canvas.

> **POLISHED REFERENCE ART → PIXEL-AUTHORED SOURCE ASSET → TARGET PIXEL CLEANUP → IN-GAME ASSET**
>
> not
>
> **PAINTED ILLUSTRATION → SHRINK / QUANTIZE / CROP → CALL IT GAME PIXEL ART**

---

# 1A. Reference-Material Exception

Non-pixel polished art is acceptable for:

- character identity and facial-feature studies;
- anatomy and proportion studies;
- clothing / garment-construction studies;
- weapon and equipment mounting studies;
- directional turnaround references;
- pose, silhouette, material, and color studies;
- concept boards and presentation art;
- visual targets used to guide later pixel-authoring.

Such files must be clearly identified as **`REFERENCE ONLY`** or **`REFERENCE PASS`** and must not be described as source sprites, runtime sprites, Phaser assets, or game-ready assets.

A reference image may establish design intent, proportions, palette relationships, garment construction, hidden geometry, and attachment logic. It does **not** become production art merely because it is transparent, uses a checkerboard background, is labeled `480×640`, contains filenames, or visually resembles a sprite sheet.

Reference art may be more polished, painterly, or illustrative than the final game asset. That is acceptable because its job is to communicate the target, not to ship in-game.

---

# 1B. Promotion Boundary — When Pixel Art Becomes Mandatory

The moment a file is identified as any of the following, the pixel-art standard becomes mandatory:

- `SOURCE CANDIDATE`;
- `PIXEL SOURCE`;
- `SOURCE PASS`;
- `RUNTIME CANDIDATE`;
- `RUNTIME PASS`;
- `IN-GAME`;
- `PHASER ASSET`;
- a production PNG/atlas/layer loaded or intended to be loaded by the game.

A non-pixel reference illustration must therefore be **re-authored as pixel art** before it crosses into the production-source stage.

Cropping a reference illustration into pieces, reducing it with nearest-neighbor, quantizing its palette, applying a pixelation filter, or tracing its visible silhouette does **not** satisfy this requirement. Those operations may assist analysis, but they do not replace deliberate pixel authoring.

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

## 2A. No-Mixle Rule

For Astro Fighters production QA, a **mixle** means any pixel whose final value is created by interpolation, anti-aliasing, filtered scaling, partial-alpha blending, soft-edge resampling, or other automatic mixing between intended authored pixel values.

Mixles are **not valid production pixels**.

Production pixel art must therefore satisfy all of the following:

- alpha is hard unless a specifically approved VFX asset requires controlled translucency;
- ordinary character/environment sprite alpha uses only `0` or `255`;
- silhouette pixels are not anti-aliased against a matte, checkerboard, paper color, presentation background, or neighboring color;
- no bilinear, bicubic, Lanczos, diffusion, smooth scaling, or browser interpolation may define source/runtime pixel values;
- palette colors are deliberate authored values, not intermediate RGB values created between neighboring colors;
- nearest-neighbor previews/expansions must reproduce the logical pixel grid exactly;
- if a production source is intentionally built as an integer expansion of a logical pixel grid, every expanded block must be exactly uniform in RGBA value;
- zoomed QA must expose individual pixel boundaries clearly enough to detect mixed/interpolated edge colors and matte residue.

Automatic failures include:

- semi-transparent fringe pixels on an otherwise hard-alpha character sprite;
- brown, gray, white, checkerboard, or other matte-colored pixels occupying air/negative space around a character or prop;
- single-pixel blended halos produced by resizing or compositing;
- color values that exist only because an edge was interpolated between foreground and background;
- a file that looks crisp at normal size but reveals mixed/soft pixels when inspected at nearest-neighbor zoom.

A machine `NO-MIXLE PASS` may verify hard alpha, exact nearest-neighbor expansion, and absence of interpolated block values, but it does **not** replace manual pixel-art review. Deliberate authored cluster quality still requires human/source review.

---

# 3. Palette Discipline

Production source art must use the approved Astro Fighters palette authority or an explicitly approved source palette derived from it.

- no arbitrary continuous RGB color drift;
- no hundreds/thousands of near-duplicate painted colors;
- no anti-aliasing colors created only by interpolation;
- no color-noise texture standing in for pixel detail;
- shadows/highlights must use intentional palette steps;
- metallic, cloth, skin, hair, rope, leather, wood, stone, water, and VFX materials must each retain their approved ramp behavior.

A source image that requires heavy palette quantization before it resembles pixel art is **not** an approved source master.

Reference illustrations are exempt from production palette-count restrictions unless the reference itself is specifically being used as a palette authority. That exemption ends when the asset enters production-source status.

---

# 4. Scaling / Resampling Rule

For authored pixel assets:

- nearest-neighbor is the default scaling method;
- bilinear, bicubic, Lanczos, diffusion, painterly upscaling, or other smoothing filters may not define final source pixels;
- diagnostic previews may use other resampling only if clearly labeled and never promoted as source authority;
- a mechanically reduced 48×64 image remains a candidate until manual target-pixel cleanup is complete.

The source master must not rely on downsampling to hide soft edges, anatomy errors, color noise, or painterly detail.

A polished non-pixel reference may be scaled freely for presentation or study because it is not a game asset. That does not authorize using the scaled result as production sprite pixels.

---

# 5. Character Source Rule

For character packages such as Kairo:

- polished illustration may be used as a **REFERENCE ONLY** authority for identity, anatomy, garment construction, equipment placement, and directional intent;
- all 480×640 body, hair, garment, equipment, hand, footwear, and accessory files promoted to production source status are pixel-art source assets;
- modular production layers must satisfy `ASTRO_FIGHTERS_MODULAR_SOURCE_LAYER_INTEGRITY_RULES.md` **and** this pixel-art source standard;
- clean component geometry does not compensate for painterly rendering;
- a component may pass clipping/occlusion QA and still fail source approval if its rendering is not pixel art;
- S, SE, E, NE, N, NW, W, and SW must remain stylistically coherent at the pixel-cluster level.

---

# 6. Automatic Production-Source Failures

The following are automatic failures **when presented as production/source/runtime/in-game assets**:

- smooth cel-shaded/anime illustration presented as a sprite source;
- painterly 480×640 character renders with soft edges;
- anti-aliased silhouettes or garment borders;
- high-resolution concept/reference art cropped into modular pieces and called source sprites;
- generative presentation boards whose component images are painted illustrations and are presented as game assets;
- assets that only look pixel-art-like after aggressive shrinking;
- arbitrary dithering/quantization used to disguise non-pixel source art;
- filtered enlargement of a low-resolution frame masquerading as a 480×640 master;
- mixles: interpolated/anti-aliased/partial-alpha production pixels where discrete authored pixels are required;
- acceptance based on labels such as “pixel art,” “480×640,” or “32 colors” embedded inside an image rather than the actual pixels.

The same imagery may remain valid as **REFERENCE ONLY** material if it is clearly classified and is not promoted into the production asset pipeline.

---

# 7. Mandatory Production-Source Review

Before `PIXEL SOURCE PASS` or `SOURCE PASS`, review the asset at:

1. **100% source scale** — inspect actual cluster construction and edge treatment;
2. **zoomed pixel inspection** — verify hard alpha, palette steps, absence of mixles, and absence of smoothing artifacts;
3. **normal assembled composite** — verify the pieces still read as one coherent fighter/world asset;
4. **48×64 candidate** — confirm the source contains the right information to reduce cleanly without depending on blur/averaging.

A valid production source must pass both:

- **component / construction integrity**, and
- **pixel-art rendering integrity**.

Reference approval is a separate upstream gate and does not satisfy either production-source requirement.

---

# 8. Required Status Vocabulary

Use these labels precisely in filenames, manifests, Markdown status, QA reports, and handoffs:

- **REFERENCE ONLY** — exploratory/reference material; may be illustrative or painterly; never an in-game asset.
- **REFERENCE PASS** — approved visual/design authority; may still be non-pixel and non-production.
- **COMPONENT INTEGRITY PASS** — modular shapes / hidden underlayers are valid; rendering may still require pixel-source approval.
- **PIXEL SOURCE PASS** — production source pixels satisfy the Astro Fighters pixel-art standard, including the no-mixle rule.
- **SOURCE PASS** — registration + component integrity + pixel-source quality + composite fidelity all pass.
- **RUNTIME CANDIDATE** — derived target-resolution sprite awaiting manual target-pixel cleanup/validation.
- **RUNTIME PASS** — target-resolution asset has been manually cleaned and validated for game use.
- **IN-GAME / PHASER ASSET** — production runtime asset actually loaded or approved to be loaded by gameplay; must already have `RUNTIME PASS` unless explicitly marked temporary/debug-only.

Never call an illustrative reference `SOURCE`, `RUNTIME`, `GAME READY`, or `IN-GAME` merely because it resembles the intended design.

No direction may advance on `REFERENCE PASS` or `COMPONENT INTEGRITY PASS` alone.

---

# 9. Repository / File-Role Separation

Where practical, keep illustrative reference authorities and production pixel assets visibly distinct in repository structure and metadata.

Recommended intent separation:

- `reference/` — design authorities, turnarounds, studies, approved illustrative targets;
- `source/` — actual pixel-authored production masters and modular layers;
- `runtime/` or established Phaser asset paths — target-resolution game assets.

A manifest that points to a reference image must explicitly identify it as reference authority rather than production source.

Git history may preserve earlier experiments, but the active paths must not make a painterly reference look like the current game asset.

---

# 10. Immediate Kairo Application

The polished/cel-shaded Kairo S/SE images remain useful as **REFERENCE ONLY / REFERENCE PASS** material for Afro-feature identity, anatomy, clothing construction, directional pose, and anatomical-left weapon mounting.

They are not rejected merely because they are illustrative.

They are, however, **not production game assets**.

SE remains blocked until its continuous, unclipped component geometry is **re-authored in the approved Astro Fighters pixel-art language** on the shared 480×640 lattice. Only after SE earns both **COMPONENT INTEGRITY PASS** and **PIXEL SOURCE PASS** may it receive `SOURCE PASS` and unblock E.

---

## Locked summary

> **ILLUSTRATION IS ALLOWED FOR REFERENCE.**  
> **ANYTHING IDENTIFIED FOR GAME USE MUST BE PIXEL ART.**  
> **REFERENCE ART GUIDES THE PIXEL ASSET; IT DOES NOT BECOME THE PIXEL ASSET BY SHRINKING, CROPPING, OR FILTERING.**  
> **MIXLES ARE NOT PRODUCTION PIXELS.**  
> **HIGHER SOURCE RESOLUTION MEANS MORE AUTHORED PIXELS, NOT SMOOTHER PAINTING.**
