# Astro Fighters — Slice 0 Source Art Brief

**Status:** Active execution brief  
**Package:** `AF-IC-SHARED-FOUNDATION`  
**Milestone:** Imperial City Early Player Experience v0  
**Target:** Slice 0 — Foundation Courtyard  
**Runtime:** Phaser/browser under `/docs`

This is a temporary production brief. Retire/archive it after Slice 0 is locked and the next package becomes authoritative.

---

# 1. Purpose

Slice 0 is the first proof that Imperial City world art, the playable character, projection, lighting, layering, hidden-grid concealment, traversal, collision, and occlusion can coexist at production quality.

The first visual reference is a **target**, not a baked gameplay background and not a substitute for modular source files.

It must answer:

> **Can a finished Astro Fighters street-fighter character inhabit a compact Imperial City material/architecture slice and make the whole image read as one premium game?**

Only after the reference target is visually sound should purpose-built modular source production proceed.

---

# 2. Relationship to the active manifest

`production/asset-manifest.json` contracts **14 shared-foundation world dependencies**.

Slice 0 does **not** require all 14 to appear as equal-weight hero elements in the first assembly. Its minimum architectural/material proof uses this **8-asset core subset**:

1. `stone-clean`
2. `building-threshold`
3. `drainage-channel`
4. `drainage-grate`
5. `timber-post`
6. `horizontal-beam`
7. `timber-plaster-wall`
8. `aged-stone-foundation`

The remaining contracted shared-foundation dependencies—`stone-cracked`, `stone-patched`, `stone-timber-transition`, `cracks`, `stains`, and `cart-wear`—remain part of the active package contract and should be added where they help prove variation/grid concealment or immediately after the core assembly is stable.

Do not interpret the 8-asset core as replacing the 14-asset manifest.

---

# 3. Reference composition

Create one compact gameplay-oriented courtyard/street-edge composition in the locked flat-faced 3/4 cabinet projection.

It should visibly contain:

- irregular worn Imperial civic stone;
- street-to-building threshold;
- drainage channel + restrained grate;
- aged stone foundation;
- timber/plaster wall;
- timber structural post;
- horizontal timber beam;
- restrained roof/eave implication or upper architectural edge;
- one analog dressing cue such as a hanging lantern, blank sign mount, or noren-style cloth;
- one foreground occluder such as low railing, planter, or foliage edge;
- one fully dressed benchmark player at believable gameplay scale.

Do not make:

- a grand plaza;
- palace vista;
- decorative key illustration;
- dense market scene;
- infographic/status board;
- palette chart;
- UI-framed presentation image.

---

# 4. Character benchmark

Use the shared-foundation identity:

- brown-skinned male fighter;
- short Afro;
- sleeveless fighter wrap;
- short utility jacket;
- loose fighter trousers;
- sneaker-hybrid martial shoes;
- cloth sash;
- wrist wraps;
- neck cord/charm;
- no weapon required;
- restrained contact shadow.

He should read as an early-game Academy/street-fighter trainee, not a generic fantasy adventurer.

The reference character is a visual benchmark only. Production still requires eight distinct source masters and the modular character source set on the contracted `480×640` lattice.

---

# 5. World material language

## Imperial stone

- pale-to-warm civic stone;
- irregular authored blocks/repair seams;
- localized cracks, grime, and cart wear;
- dry matte surface;
- no mirrored reflection;
- no square tiling cadence exposing the hidden 32×32 grid;
- wear crosses implied movement-cell boundaries.

## Timber

- warm aged structural timber;
- gameplay-readable grain only;
- darkened contact/joinery edges;
- restrained clean-iron or patinated-copper hardware where useful;
- no steampunk ornament.

## Plaster

- warm off-white/earth tone;
- broad calm wall planes;
- localized age/staining/repairs;
- enough negative space for Japandi restraint.

## Aged stone foundation

- older/heavier masonry than the street;
- restrained moss/grime;
- load-bearing city fabric, not dungeon stone.

## Analog dressing

Use practical integrated fixtures only. Prefer sealed/recessed housings, restrained clean iron, patinated copper, wood, cloth, paper, and weak single-purpose analog indicators where needed.

Do not use generic neon, wet-reflective cyberpunk, boiler/gear/clockwork, generic pipework, or decorative machinery as the identity.

---

# 6. Projection, scale, and layering

The reference and final source assembly must obey runtime logic:

- flat-faced 3/4 cabinet projection;
- character feet establish the ground plane;
- vertical wall faces remain legible;
- no isometric diamond distortion;
- foreground occluder must be reproducible as a separate runtime layer;
- architecture must support separate ground, architecture, dressing, actors, and front-occluder layers;
- no impossible flattened overlap that Phaser cannot reproduce.

The hidden 32×32 grid is structural only. Do not reveal it through paving, timber spacing, drainage rhythm, decal cadence, or prop spacing.

---

# 7. Lighting

Default source lighting:

- upper-left / northwest key;
- daylight or neutral warm daytime for the first benchmark;
- restrained contact/local shadows;
- material-specific value separation;
- no dramatic backlight hiding construction.

Night variants are downstream. Do not use magenta/cyan, generic neon, or glossy wet streets to make the reference attractive.

---

# 8. Composition restraint

Use one hero relationship:

> **finished player + finished Imperial City material slice**

Keep:

- broad readable wall/ground planes;
- enough negative space to inspect the player silhouette;
- sparing props;
- no crowd;
- no information board;
- no text labels baked into the art;
- no visible grid;
- no exaggerated apparatus.

---

# 9. Automatic reference rejection

Reject/refine before modular-source production if any of these appear:

- world art visibly below character quality;
- generic RPG Maker/fantasy-town appearance;
- Japanese-Chinese architectural drift;
- cyberpunk/neon/wet-reflective language;
- steampunk/gear/boiler/clockwork language;
- mannequin/incomplete player;
- fake front-facing body reused as another direction;
- visible grid rhythm;
- smooth painted illustration that cannot become modular game space;
- impossible occlusion;
- excessive purple/teal dominance;
- values too dark to read materials;
- decorative apparatus becoming the hero.

---

# 10. Modular source production

After reference approval, author the contracted assets as **purpose-built clean source masters** at the dimensions in `asset-manifest.json`.

Do not crop modules from the reference and call them final.

Reference-only dressing/occluder cues must be separately contracted before becoming production source assets.

Temporary generations, failed experiments, and QA boards may remain outside the repository. Once a source master becomes the active approved authority for a manifest path, it should live at the registered canonical source path unless the package is explicitly re-contracted to use an external source authority.

---

# 11. Character source work

Using the same visual authority:

1. author eight base-underlayer masters;
2. author eight fully dressed benchmark masters;
3. author modular garment/accessory layers on the same lattice;
4. compare modular composites to the benchmark;
5. run isolation/anchor/hard-alpha QA;
6. approve all source directions;
7. derive `48×64` runtime candidates;
8. manually clean target-resolution pixels;
9. integrate idle/walk/ready into Phaser.

No runtime reduction while source silhouette, direction, routing, or material treatment is unstable.

---

# 12. Integrated Slice 0 acceptance

After world and character sources are approved and runtime candidates are cleaned, assemble Slice 0 in the **actual Phaser runtime**.

Required:

- multiple separate runtime environment textures/layers;
- continuous player movement;
- collision independent from appearance imagery;
- live foreground/background occlusion;
- correct player pivot/contact;
- no visible grid rhythm;
- character/world style homogeneity;
- no placeholder clothing;
- no baked-background dependency;
- integrated preview captured from the running Phaser canvas;
- zero automatic failures;
- all critical minimums passing;
- **42+** before related checklist completion;
- **46+** target before Slice 0 becomes a visual authority for Harbor production.

Until that gate passes, Slice 0 remains active.
