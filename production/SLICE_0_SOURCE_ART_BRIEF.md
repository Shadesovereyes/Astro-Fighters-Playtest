# Astro Fighters — Slice 0 Source Art Brief

**Status:** Active reference-production brief  
**Package:** `AF-IC-SHARED-FOUNDATION`  
**Milestone:** Imperial City Early Player Experience v0  
**Target:** Slice 0 — Foundation Courtyard Test  
**Runtime:** Phaser/browser under `/docs`

---

# 1. Purpose

Slice 0 is the first visual proof that the Imperial City world, playable character, projection, lighting, layering, and hidden-grid rules can coexist at production quality.

The first deliverable is a **reference target**, not a baked gameplay background and not a substitute for modular source files. It establishes the look that the separately authored world modules and character sources must match.

The reference must answer one question:

> Can a finished Astro Fighters street-fighter character stand inside a small Imperial City architectural slice and make the entire image read as one premium game rather than a premium character pasted onto weaker scenery?

Only after that answer is yes should modular source production continue.

---

# 2. Required Reference Composition

Create one compact gameplay-oriented courtyard/street-edge composition using the locked flat-faced 3/4 cabinet projection.

The composition must visibly contain:

- irregular worn Imperial stone street;
- one street-to-building threshold;
- one drainage channel and restrained grate treatment;
- aged stone foundation;
- timber-and-plaster wall;
- timber structural post;
- horizontal timber beam;
- a restrained roof/eave implication or architectural upper edge sufficient to establish vertical construction;
- one analog dressing cue: hanging lantern, restrained sign mount, or noren-style cloth;
- one foreground occluder such as a low railing, planter, or foliage edge;
- one fully dressed benchmark player character at believable gameplay scale.

Do not make a grand plaza, palace, monumental vista, decorative key illustration, or dense market scene. This is a narrow material/character benchmark.

---

# 3. Character Reference

Use the shared-foundation benchmark identity:

- brown-skinned male fighter;
- short Afro;
- sleeveless fighter wrap;
- short utility jacket;
- loose fighter trousers;
- sneaker-hybrid martial shoes;
- cloth sash;
- wrist wraps;
- neck cord / charm;
- no weapon required;
- restrained contact shadow.

The fighter should look like an early-game Academy/street-fighter trainee rather than a generic fantasy adventurer.

Character language:

- Edo/martial garment logic;
- hip-hop/streetwear attitude;
- practical layered silhouette;
- premium 90s-anime-inspired pixel craftsmanship;
- clear face/hair/garment material separation;
- no mannequin/base-body exposure;
- no cyberpunk techwear;
- no European medieval fantasy silhouette.

The reference character is a **visual benchmark only**. Final production character art still requires eight separately authored canonical direction masters on the shared 480×640 lattice plus modular layer sources.

---

# 4. World Material Language

## Imperial stone

- pale-to-warm civic stone family;
- irregular authored blocks and repair seams;
- small cracks, grime, and cart wear;
- dry matte surface;
- no mirrored reflections;
- no regular square tiling that exposes the hidden 32×32 grid;
- wear patterns should cross implied movement-cell boundaries.

## Timber

- warm aged structural timber;
- visible grain only where it survives gameplay scale;
- darkened contact edges and joinery;
- restrained iron/clean-metal brackets when needed;
- no steampunk gear/rivet clutter.

## Plaster

- warm off-white/earthy plaster;
- broad calm wall planes;
- localized age, staining, or repairs;
- enough negative space to preserve Japandi restraint.

## Aged stone foundation

- heavier, older masonry than street paving;
- moss/grime only in restrained local pockets;
- must read as load-bearing city fabric rather than dungeon stone.

## Metal / analog dressing

- clean metal, rusted metal, patina used as small accents;
- practical brackets, grate, lantern housing, or junction detail;
- no chrome, glowing panels, sci-fi consoles, or ornate clockwork.

---

# 5. Projection, Scale, and Layering

The reference must obey the runtime's visual logic:

- flat-faced 3/4 cabinet projection;
- character feet establish the gameplay ground plane;
- vertical wall faces remain legible without isometric diamond distortion;
- foreground occluder demonstrates that the player can pass behind it in the eventual runtime;
- architecture should clearly support separate `ground`, `architecture`, `architecture-dressing`, `actors`, and `props-front-occluders` layers;
- do not compose impossible overlaps that only work in a flattened illustration.

The hidden 32×32 movement grid is structural only. No pavement seam, timber spacing, drainage rhythm, decal spacing, or prop placement may reveal a regular 32-pixel cadence.

---

# 6. Lighting

Default source lighting:

- upper-left / northwest key direction;
- daylight or neutral warm daytime for the first benchmark;
- restrained contact/local shadows;
- material-specific value separation;
- no dramatic cinematic backlight that hides the asset construction.

Night variants are downstream. Do not use neon, wet reflective pavement, magenta/cyan lighting, or cyberpunk glow to make the reference attractive.

---

# 7. Composition Restraint

Use the Master Prompt's restraint requirement:

- one hero relationship: **finished player + finished Imperial City material slice**;
- broad readable wall/ground planes;
- enough negative space to inspect the character silhouette;
- props used sparingly;
- no crowd;
- no decorative information board;
- no text labels baked into the art;
- no UI frame;
- no fake palette chart;
- no visible grid;
- no exaggerated machinery.

The scene should feel inhabited and plausible without becoming cluttered.

---

# 8. Automatic Reference Rejection Conditions

Reject/refine the reference before modular-source production if any of these appear:

- world art visibly lower quality than the character;
- generic RPG Maker / generic fantasy town appearance;
- Japanese-Chinese architectural drift;
- cyberpunk/neon/wet-reflective visual language;
- steampunk boiler/gear/clockwork language;
- character reads as mannequin or unfinished paper doll;
- front-facing body disguised as a different facing;
- regular paving/wall rhythm reveals the hidden grid;
- environment is a smooth painted illustration rather than believable modular pixel-art construction;
- foreground occlusion is impossible to reproduce as separate runtime layers;
- excessive purple/teal palette dominance;
- overly dark values that destroy material readability;
- large decorative machinery becomes the hero instead of city/character homogeneity.

---

# 9. Modular Source Assets That Follow Reference Approval

Once the reference target is visually approved, author these separately at their contracted source dimensions from `production/asset-manifest.json`:

1. `stone-clean` — 1920×1280 source
2. `building-threshold` — 1280×640 source
3. `drainage-channel` — 1600×480 source
4. `drainage-grate` — 480×320 source
5. `timber-post` — 480×1280 source
6. `horizontal-beam` — 1280×480 source
7. `timber-plaster-wall` — 1920×1600 source
8. `aged-stone-foundation` — 1920×640 source

Reference-only lantern/sign/noren and foreground-occluder cues must be separately contracted before they become production source assets.

Do **not** crop these modules out of the reference image and call them production assets. The reference establishes the target; the modular sources must be purpose-built clean assets.

---

# 10. Character Source Work After Reference Approval

Using the same visual authority:

1. author eight base-underlayer masters on 480×640 canvases;
2. author eight fully dressed benchmark masters on the same lattice;
3. author modular garment/accessory layers on that same lattice;
4. compare modular composites against the dressed benchmark;
5. run isolation/anchor/hard-alpha QA;
6. approve all source directions;
7. derive 48×64 runtime candidates;
8. manually clean target-resolution pixels;
9. integrate idle/walk/ready into Phaser.

No runtime reduction should begin while the source silhouette, direction, garment routing, or material treatment is still unstable.

---

# 11. Slice 0 Integrated Acceptance

After modular world and character sources are built and reduced, assemble the actual Phaser Slice 0 scene and evaluate it with the mandatory rubric.

Required:

- zero automatic failures;
- all critical category minimums pass;
- character and world feel authored by the same studio;
- no visible grid rhythm;
- correct depth/occlusion behavior;
- correct player pivot/foot contact;
- no placeholder clothing;
- no baked-background dependency;
- 42+ before related checklist completion;
- 46+ target for the visual authority used by Harbor production.

Until that integrated gate passes, Slice 0 remains active.