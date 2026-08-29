# Astro Fighters — Current Development Status

**Updated:** 2026-08-29  
**Authoritative branch:** `main`  
**Active development branch:** `development/slice0-shared-foundation-v1`  
**Draft PR:** #12 — Slice 0 continuous modular Phaser world refactor  
**Current milestone:** Imperial City Early Player Experience v0  
**Current gate:** five-asset shared-foundation source assembly / homogeneity review before source approval and Phaser runtime activation

## Architecture snapshot

Astro Fighters is an **open-world, real-time action-combat RPG**. The active public runtime is Phaser/browser under `/docs`. The private Unity project remains legacy turn-based Combat Strategy reference material only.

`main` remains production authority until the active branch is reviewed and merged.

## Required authority order

1. `README.md`
2. `AGENTS.md`
3. `ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md`
4. `production/NEGATIVE_PROMPT_REGISTER.md`
5. `PHASER_WORLD_REFACTOR_V0.md`
6. `IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md`
7. art-review rubric Markdown + `docs/data/art-review-rubric.json`
8. world/character production checklists
9. `production/asset-manifest.json`
10. `docs/data/shared-foundation-runtime.json`
11. this handoff

## Technical runtime milestone — implemented

The active branch provides continuous 104 px/sec movement, delta-time updates, normalized diagonals, canonical 8-direction facing, hidden legacy grid, hidden baked district background in refactor mode, modular world-layer scaffolding, collision independent from imagery, foreground Y-depth/occlusion proof, and runtime audit hooks.

The guarded asset loader only enables assets with `runtime-candidate`, `integrated`, or `approved` status. Source-QA files may exist without appearing in gameplay.

## Persistent user corrections

`production/NEGATIVE_PROMPT_REGISTER.md` is mandatory.

- `NP-CHAR-001`: no chibi / SD / mascot / oversized-head character proportions.
- `NP-PRES-001`: no generated status dashboards as production evidence and no invented completion, approval, file, commit, date, or Phaser claims.

## Shared-foundation benchmark family — 5/5 authored

All five benchmark assets now physically exist as source masters plus exact runtime-scale derivatives and are tracked as **`source-qa`**. None are source-approved or runtime-enabled yet.

1. `stone-clean` — **AUTHORED / SOURCE-QA**
   - source 1920×1280
   - runtime derivative 192×128
   - QA: `production/qa/world/shared-foundation/stone-clean-candidate-v1.md`

2. `aged-stone-foundation` — **AUTHORED / SOURCE-QA**
   - source 1920×640
   - runtime derivative 192×64
   - QA: `production/qa/world/shared-foundation/aged-stone-foundation-candidate-v1.md`

3. `timber-plaster-wall` — **AUTHORED / SOURCE-QA**
   - source 1920×1600
   - runtime derivative 192×160

4. `timber-post` — **AUTHORED / SOURCE-QA**
   - source 480×1280
   - runtime derivative 48×128

5. `horizontal-beam` — **AUTHORED / SOURCE-QA**
   - source 1280×480
   - runtime derivative 128×48

The final three share QA evidence in `production/qa/world/shared-foundation/timber-family-candidate-v1.md`.

### Accurate counters

- benchmark source assets authored: **5 / 5**
- benchmark assets in source QA: **5 / 5**
- exact runtime derivatives physically present: **5 / 5**
- source-approved benchmark assets: **0 / 5**
- runtime-activated production assets: **0 / 5**
- Phaser-integrated production assets: **0 / 5**
- production-approved assets: **0 / 5**

The distinction is intentional: **created ≠ approved ≠ runtime-activated ≠ integrated**.

## Current family intent

The five files are intended to share one effective pixel density, NW/upper-left lighting, restrained edge vocabulary, dry matte surfaces, and Imperial City material logic.

- civic street stone uses irregular authored courses and localized wear;
- aged foundation uses larger/heavier masonry, deeper joints, darker contact edges and restrained moss;
- wall uses broad calm plaster planes framed by aged timber;
- post and beam share the wall's timber ramp and restrained functional metal joinery;
- no visible 32×32 cadence, wet-reflective treatment, cyberpunk, steampunk, clockwork or generic-fantasy material language.

## Immediate work order

1. build a five-asset source assembly using the actual committed files;
2. review homogeneity, scale, material separation, projection, NW lighting and hidden-grid behavior;
3. repair any asset that reads as a different pixel style or lower-quality material treatment;
4. when the full assembly passes, advance passing assets from `source-qa` to `source-approved`;
5. confirm/manual-clean the runtime derivatives at target pixel scale;
6. advance passing assets to `runtime-candidate` and enable them in `docs/data/shared-foundation-runtime.json`;
7. let the actual Phaser refactor scene replace the corresponding scaffold textures;
8. capture a real running Phaser canvas showing continuous movement, hidden grid, collision and foreground occlusion;
9. score the integrated Slice 0 scene and repair until 42+ with zero automatic failures and all critical minimums passing.

Do not expand into Harbor/Market prop quantity until this family passes the assembly/homogeneity gate.
