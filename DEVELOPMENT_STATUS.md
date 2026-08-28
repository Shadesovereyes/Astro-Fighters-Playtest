# Astro Fighters — Current Development Status

**Updated:** 2026-08-28  
**Authoritative baseline:** `main`  
**Active development branch:** `development/slice0-shared-foundation-v1`  
**Current milestone:** Imperial City Early Player Experience v0  
**Current gate:** Slice 0 Foundation Courtyard production assets + live Phaser review

## Current game architecture

Astro Fighters is an **open-world, real-time action-combat RPG**. The active public implementation is the **Phaser/browser runtime under `/docs`**.

The private `Shadesovereyes/Astro-Fighters` Unity project is a **legacy turn-based tactical Combat Strategy vertical slice**. It is reference material for reusable combat logic and math only. Do not redirect current development into Unity and do not port the old turn loop, action-slot scheduler, hex encounter structure, or prototype UX into the open-world RPG.

When legacy combat logic is reused, preserve design intent and useful math, then adapt it to real-time movement, hit windows, animation commitment, collision, interrupts, recovery/cooldowns, resources, player input, and AI behavior.

## Repository authority

`main` remains the production baseline. Active Slice 0 work is being developed on `development/slice0-shared-foundation-v1` until reviewed/merged.

Before development, read in this order:

1. `README.md` — repository orientation and game architecture
2. `AGENTS.md` — repository/runtime/development behavior
3. `ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md` — visual canon
4. `PHASER_WORLD_REFACTOR_V0.md` — world-runtime migration gate
5. `IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md` — current route/scope/order
6. `Astro Fighters — Art Preview Review Rubric.md` — human review rules
7. `docs/data/art-review-rubric.json` — machine scoring authority
8. world and character production checklists — completion inventories
9. `production/asset-manifest.json` — current machine-readable package contract

Git history is the iteration archive. Old package branches and superseded package PRs are historical reference, not production authority.

## Active milestone

The first connected production-quality route remains:

> **SOUTHERN HARBOR ARRIVAL → DOCKS / SHIPWRIGHT → MARKET / SHOPPING STREET → RESIDENTIAL / CANAL TRANSITION → ASTRO FIGHTER ACADEMY EXTERIOR → ACADEMY INTERIOR / SENSEI TUTORIAL**

The Academy tutorial retains the established progression intent:

- Sensei teaches the combat foundation;
- General/Trap ability access is introduced;
- the player receives **100 mon**;
- the player chooses **3 distinct trap types, 10 of each**;
- inventory/paper-doll/action-RPG state reflects the result.

Crab-island/cave production remains outside this milestone gate.

## Phaser world refactor — technical milestone implemented

The first runtime refactor milestone is now implemented on `development/slice0-shared-foundation-v1` through `docs/js/world-refactor-v0.js` and wired into `docs/play-v4.html`.

The refactor layer deliberately preserves proven gameplay systems while replacing the legacy exploration/world-presentation path.

Implemented:

- continuous movement at **104 pixels/second**;
- delta-time movement;
- normalized diagonals;
- canonical eight-direction facing derived from the movement vector;
- suppression of the legacy `STEP_MS` tile-step movement while retaining the rest of the established update loop;
- persistent legacy 32×32 grid graphics hidden in refactor mode;
- legacy full-frame district background/shade hidden in refactor mode;
- separate runtime scaffold textures for ground, wall, foundation, threshold, and foreground post;
- explicit runtime layer metadata using the locked 11-layer order;
- collision data represented independently from appearance imagery;
- axis-separated continuous collision resolution against authored rectangles;
- one foreground post/occluder proof object with Y-depth behavior and its own collision footprint;
- a visible `TECHNICAL WORLD-REFACTOR SCAFFOLD · NOT ART REVIEW` label so scaffold imagery cannot be mistaken for production art;
- runtime audit exposure through `AF_WORLD_REFACTOR_V0.audit()` and `AF_TEST.worldRefactor()`;
- static contract validation in `tools/validate-world-refactor.mjs`;
- CI syntax + contract coverage for the refactor.

GitHub Actions run **#53** passed for commit `faf3fd20734e1ea7e6fc5a38baf91563727287e4`.

### Important status distinction

This completes the **technical code/scaffold milestone**, not the art milestone.

The generated scaffold textures are intentionally low-authority technical materials. They are marked `productionArt: false` and `scaffoldOnly: true`. They must never be scored or presented as production-quality Astro Fighters art.

A live/manual Phaser-canvas observation is still required before the refactor document's final visual proof items can be checked off, especially the actual occlusion screenshot/review evidence. CI proves the code contract and wiring, not visual art quality.

## Active production package

`AF-IC-SHARED-FOUNDATION`

The package remains **contracted** in `production/asset-manifest.json`. Production source masters and production runtime assets remain missing/unapproved.

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

## Slice 0 — next art milestone

The next legitimate milestone is now **production replacement of the technical scaffold with a coherent shared-foundation asset family**.

First benchmark family:

1. Imperial stone ground
2. aged stone foundation
3. timber/plaster wall
4. timber post
5. horizontal beam

These assets must establish one coherent studio language before drainage, threshold, decals, signs, props, or foliage expand the set.

The first production family must share:

- one effective pixel density;
- one NW/upper-left lighting model;
- one edge/outline vocabulary;
- one material-shading discipline;
- the locked palette families;
- dry matte surface treatment;
- flat-faced 3/4 cabinet projection;
- no visible 32×32 cadence;
- no generic steampunk/cyberpunk drift.

Only after source/reference approval should 10× source masters be reduced and manually cleaned into runtime assets.

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

- the **world checklist** owns world-asset completion state;
- the **character checklist** owns character-asset completion state;
- `production/asset-manifest.json` owns active package/runtime registration state;
- `IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md` owns route scope and production order;
- this file records only the current handoff snapshot.

Do not use this file as a second checklist.

## Next work order

1. author one coherent shared-foundation visual benchmark family: stone + aged foundation + timber/plaster + post/beam;
2. approve that source/reference language before expanding the asset count;
3. produce clean modular source masters on contracted dimensions;
4. run source isolation/anchor/assembly QA;
5. derive and manually clean runtime candidates;
6. replace `af-scaffold-*` textures with the approved runtime assets while keeping the refactor architecture;
7. capture an actual Phaser gameplay frame demonstrating continuous traversal, hidden grid, collision, and foreground occlusion;
8. score the integrated Slice 0 scene;
9. repair until all critical gates pass;
10. at 42+, update only the relevant checklist/manifest completion state;
11. proceed into Harbor Arrival, then Market → Residential/Canal → Academy Exterior → Academy Interior/Sensei.

If an upstream gate fails, repair it before continuing downstream.
