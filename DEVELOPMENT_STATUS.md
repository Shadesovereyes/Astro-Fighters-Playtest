# Astro Fighters — Current Development Status

**Updated:** 2026-08-28  
**Authoritative branch:** `main`  
**Current milestone:** Imperial City Early Player Experience v0  
**Immediate runtime gate:** Phaser World Refactor v0 + Slice 0 Foundation Courtyard

## Current game architecture

Astro Fighters is an **open-world, real-time action-combat RPG**. The active public implementation is the **Phaser/browser runtime under `/docs`**.

The private `Shadesovereyes/Astro-Fighters` Unity project is a **legacy turn-based tactical Combat Strategy vertical slice**. It is reference material for reusable combat logic and math only. Do not redirect current development into Unity and do not port the old turn loop, action-slot scheduler, hex encounter structure, or prototype UX into the open-world RPG.

When legacy combat logic is reused, preserve design intent and useful math, then adapt it to real-time movement, hit windows, animation commitment, collision, interrupts, recovery/cooldowns, resources, player input, and AI behavior.

## Repository authority

`main` is the current repository authority unless `README.md` or this file explicitly identifies a newer active development branch.

Before development, read in this order:

1. `README.md` — repository orientation and game architecture
2. `AGENTS.md` — repository/runtime/development behavior
3. `ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md` — visual canon
4. `PHASER_WORLD_REFACTOR_V0.md` — temporary world-runtime migration gate
5. `IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md` — current route/scope/order
6. `Astro Fighters — Art Preview Review Rubric.md` — human review rules
7. `docs/data/art-review-rubric.json` — machine scoring authority
8. world and character production checklists — completion inventories
9. `production/asset-manifest.json` — current machine-readable package contract

Git history is the iteration archive. Old development branches and superseded package PRs are historical reference, not current authority.

## Active milestone

The first connected production-quality route is:

> **SOUTHERN HARBOR ARRIVAL → DOCKS / SHIPWRIGHT → MARKET / SHOPPING STREET → RESIDENTIAL / CANAL TRANSITION → ASTRO FIGHTER ACADEMY EXTERIOR → ACADEMY INTERIOR / SENSEI TUTORIAL**

The Academy tutorial retains the established progression intent:

- Sensei teaches the combat foundation;
- General/Trap ability access is introduced;
- the player receives **100 mon**;
- the player chooses **3 distinct trap types, 10 of each**;
- inventory/paper-doll/action-RPG state reflects the result.

Crab-island/cave production remains outside this milestone gate.

## Immediate technical gate

The current browser prototype genuinely uses Phaser, but its world layer still contains prototype debt:

- baked full-frame district imagery;
- visible 32×32 route/grid presentation;
- fixed integer tile-step exploration;
- collision tied too closely to grid rectangles;
- limited live depth/occlusion behavior.

`PHASER_WORLD_REFACTOR_V0.md` is the active correction plan.

Before Slice 0 can be called integrated, the runtime must prove:

- continuous real-time movement;
- no persistent visible grid;
- multiple separate environment textures/layers loaded by Phaser;
- collision authored independently from appearance imagery;
- live foreground/background occlusion;
- eight-direction player facing/animation;
- crisp pixel rendering;
- an integrated review captured from the actual Phaser canvas.

A collage, presentation board, source assembly, contact sheet, or mock renderer is never an integrated gameplay preview.

## Active production package

`AF-IC-SHARED-FOUNDATION`

The package is currently **contracted** in `production/asset-manifest.json`. Its production source masters and runtime assets remain missing/unapproved in the repository.

Locked package facts include:

- canonical directions `N, NE, E, SE, S, SW, W, NW`;
- `S = front`, `N = back`;
- character source canvas `480×640`;
- source body center `[240,600]`;
- source foot-contact line `y=600`;
- runtime frame `48×64`;
- runtime pivot `[24,60]`;
- world source scale `10×` for the shared-foundation contract;
- source approval before runtime derivation;
- actual Phaser integration before checklist completion.

## Slice 0 — Foundation Courtyard

Slice 0 is the next production proof. It must combine, in the running Phaser scene:

- Imperial stone ground and wear/decal treatment;
- street/building threshold;
- drainage channel/grate;
- aged stone foundation;
- timber/plaster wall;
- timber post and horizontal beam;
- one restrained sign/lantern/noren-style dressing cue;
- one foreground occluder;
- one fully dressed benchmark player.

The purpose is to prove character/world homogeneity, projection, hidden-grid concealment, traversal scale, collision, depth, occlusion, and the source-to-runtime pipeline before Harbor production expands.

Prior collage-derived Slice 0 boards and extracted candidates are **reference/scaffolding only**. They are not production source masters and must not be promoted merely because they were isolated or resized.

## Review gate

The machine rubric in `docs/data/art-review-rubric.json` and the human-readable rubric must stay synchronized.

- **0–29:** rejected
- **30–36:** rework required
- **37–41:** conditional/internal candidate only
- **42–45:** production approved
- **46–50:** lock quality

Approval additionally requires zero automatic failures and all critical minimums passing. Checklist completion begins only at **42+**.

Integrated review is valid only from the running Phaser canvas.

## Completion-state ownership

To avoid duplicate or contradictory progress tracking:

- the **world checklist** owns world-asset completion state;
- the **character checklist** owns character-asset completion state;
- `production/asset-manifest.json` owns the active package/runtime registration state;
- `IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md` owns route scope and production order;
- this file records only the current handoff snapshot.

Do not use this file as a second checklist.

## Next work order

1. complete the Phaser world refactor minimum needed for Slice 0;
2. author/approve the shared-foundation source assets and player source authorities;
3. run source isolation/anchor/assembly QA;
4. derive and manually clean runtime candidates only after source approval;
5. assemble Slice 0 from separate assets in Phaser;
6. capture the actual Phaser gameplay frame and score it;
7. repair until all critical gates pass;
8. at 42+, update only the relevant checklist/manifest completion state;
9. proceed into Harbor Arrival, then Market → Residential/Canal → Academy Exterior → Academy Interior/Sensei.

If an upstream gate fails, repair it before continuing downstream.
