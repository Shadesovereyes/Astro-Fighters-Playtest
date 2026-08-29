# Astro Fighters — Current Development Status

**Updated:** 2026-08-28  
**Authoritative branch:** `main`  
**Active development branch:** `development/slice0-shared-foundation-v1`  
**Current milestone:** Imperial City Early Player Experience v0  
**Current gate:** Slice 0 Foundation Courtyard production assets + live Phaser review

## Current game architecture

Astro Fighters is an **open-world, real-time action-combat RPG**. The active public implementation is the **Phaser/browser runtime under `/docs`**.

The private `Shadesovereyes/Astro-Fighters` Unity project is a **legacy turn-based tactical Combat Strategy vertical slice**. It is reference material for reusable combat logic and math only. Do not redirect current development into Unity and do not port the old turn loop, action-slot scheduler, hex encounter structure, or prototype UX into the open-world RPG.

When legacy combat logic is reused, preserve design intent and useful math, then adapt it to real-time movement, hit windows, animation commitment, collision, interrupts, recovery/cooldowns, resources, player input, and AI behavior.

## Repository authority

`main` remains the authoritative production state. Active Slice 0 changes are being developed on `development/slice0-shared-foundation-v1` until reviewed and merged; that working branch does not supersede `main` as production authority.

Before development, read in this order:

1. `README.md` — repository orientation and game architecture
2. `AGENTS.md` — repository/runtime/development behavior
3. `ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md` — visual canon
4. `production/NEGATIVE_PROMPT_REGISTER.md` — persistent corrections learned from user review
5. `PHASER_WORLD_REFACTOR_V0.md` — world-runtime migration gate
6. `IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md` — current route/scope/order
7. `Astro Fighters — Art Preview Review Rubric.md` — human review rules
8. `docs/data/art-review-rubric.json` — machine scoring authority
9. world and character production checklists — completion inventories
10. `production/asset-manifest.json` — current machine-readable package contract
11. `docs/data/shared-foundation-runtime.json` — guarded runtime activation state for the first Slice 0 family
12. `production/reference/world/shared-foundation/REFERENCE_SALVAGE_REVIEW.md` — vetted historical visual evidence only

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

The first runtime refactor milestone is implemented on `development/slice0-shared-foundation-v1` through `docs/js/world-refactor-v0.js` and wired into `docs/play-v4.html`.

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

A live/manual Phaser-canvas observation is still required before the refactor document's final visual proof items can be checked off. CI proves the code contract and wiring, not visual art quality.

## Guarded runtime asset activation — implemented

`docs/data/shared-foundation-runtime.json` and `docs/js/shared-foundation-assets-v0.js` form the production-asset activation seam for the first five shared-foundation assets.

Rules enforced by `tools/validate-shared-foundation-runtime.mjs`:

- an asset is not loaded merely because a PNG exists;
- it must be explicitly enabled in the runtime registry;
- enabled status must be `runtime-candidate`, `integrated`, or `approved`;
- registry status must exactly match `production/asset-manifest.json`;
- runtime path and dimensions must match the manifest contract;
- enabled PNGs must physically exist in `/docs/assets/world/shared-foundation/` and pass PNG signature/dimension validation;
- partially replaced scaffold scenes remain labeled **NOT ART REVIEW**;
- Phaser audit state is exposed through `AF_TEST.sharedFoundation()`.

All five benchmark assets remain disabled and `missing`; therefore the scene remains scaffold-only and no production-art completion is claimed.

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
- grounded non-chibi character proportions per `production/NEGATIVE_PROMPT_REGISTER.md`;
- world source scale `10×` for the shared-foundation contract;
- source approval before runtime derivation;
- actual Phaser integration before checklist completion.

## Slice 0 reference salvage — consolidated

Useful visual evidence from superseded Package 03–05 work has been consolidated under:

`production/reference/world/shared-foundation/legacy-salvage/`

The carried-forward references are:

- `package03-clean-data.js` — historical clean-stone embedded runtime study;
- `package04-reference-preview.png` — threshold/foundation/post-beam visual reference;
- `package05-reference-anchor-montage.png` — facade/timber/plaster visual reference.

Their exact usage limits are documented in:

`production/reference/world/shared-foundation/REFERENCE_SALVAGE_REVIEW.md`

They are **reference-only**. They are not production masters, source-approved assets, runtime candidates, or integrated gameplay. No old package status or architecture was imported.

The salvage review preserves the strongest useful material lessons: irregular civic-stone rhythm, localized wear, older/heavier foundations, warm aged timber, broad restrained plaster planes, and functional metal accents.

## Rejected development outputs

The first local schematic/procedural five-asset trial was rejected because it was dimensionally correct but visually too flat and generic to establish the production style. It was not committed or promoted.

Generated status/handoff dashboards are also rejected as production evidence. `NP-PRES-001` now prohibits generated dashboards from inventing completion percentages, approvals, runtime integration, dates, commits, dimensions, file paths, or Phaser proof. Repository data and actual Phaser captures are the only authorities for those claims.

## Slice 0 — next art milestone

The next legitimate milestone is **author and approve the first current-contract `stone-clean` source master**, then use it as the material/pixel-density authority for the remaining benchmark family.

Benchmark family order:

1. `stone-clean` — source 1920×1280 → runtime 192×128
2. `aged-stone-foundation` — source 1920×640 → runtime 192×64
3. `timber-plaster-wall` — source 1920×1600 → runtime 192×160
4. `timber-post` — source 480×1280 → runtime 48×128
5. `horizontal-beam` — source 1280×480 → runtime 128×48

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

The old Package 03 clean-stone study may inform value grouping and joint rhythm, but it uses an obsolete shape and must not be blindly resized into the current 192×128 runtime contract.

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

## Handoff — exact next actions

1. Use the consolidated salvage references only as visual evidence; do not resurrect Package 03–05 runtime architecture.
2. Author a new `stone-clean` source master at **1920×1280** to the current canon.
3. Source-QA it for irregular authored courses, hidden-grid suppression, NW lighting, matte stone, localized wear, palette discipline, and homogeneity.
4. If source QA passes, change only `stone-clean` to `source-approved` in the manifest.
5. Derive the **192×128** runtime candidate with nearest-neighbor reduction plus manual target-pixel cleanup.
6. Change `stone-clean` to `runtime-candidate` in both manifest and guarded runtime registry only after the runtime PNG exists and passes CI.
7. Let Phaser replace only the ground scaffold; keep every other scaffold active and keep the scene marked **NOT ART REVIEW**.
8. Repeat the same source → QA → runtime chain for `aged-stone-foundation`, `timber-plaster-wall`, `timber-post`, and `horizontal-beam`.
9. Once all five are real runtime candidates, capture the first actual Phaser Foundation Courtyard proof showing continuous movement, hidden grid, collision, and walk-behind occlusion.
10. Score the integrated scene and repair until all critical gates pass; checklist completion begins only at 42+.
11. Proceed into Harbor Arrival, then Market → Residential/Canal → Academy Exterior → Academy Interior/Sensei.

If an upstream gate fails, repair it before continuing downstream.
