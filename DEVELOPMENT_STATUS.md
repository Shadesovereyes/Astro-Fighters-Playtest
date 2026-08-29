# Astro Fighters — Current Development Status

**Updated:** 2026-08-29  
**Authoritative branch:** `main`  
**Active development branch:** `development/slice0-shared-foundation-v1`  
**Draft PR:** #12 — Slice 0 continuous modular Phaser world refactor  
**Current milestone:** Imperial City Early Player Experience v0  
**Current gate:** complete the five-asset shared-foundation source family, then promote passing assets into guarded Phaser runtime activation

## Architecture snapshot

Astro Fighters is an **open-world, real-time action-combat RPG**. The active public runtime is Phaser/browser under `/docs`. The private Unity project is legacy turn-based Combat Strategy reference material only.

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

`main` remains production authority until the active branch is reviewed and merged.

## Technical runtime milestone — implemented

The active branch has the Phaser refactor seam for continuous 104 px/sec movement, delta-time updates, normalized diagonals, canonical 8-direction facing, hidden legacy grid, hidden baked district background in refactor mode, modular world-layer scaffolding, collision independent from appearance, foreground Y-depth/occlusion proof, and runtime audit hooks.

`docs/data/shared-foundation-runtime.json` + `docs/js/shared-foundation-assets-v0.js` enforce guarded activation: source-QA files may exist in the repository, but only `runtime-candidate`, `integrated`, or `approved` assets can be enabled to replace scaffold textures.

## Persistent user corrections

`production/NEGATIVE_PROMPT_REGISTER.md` is mandatory. Current locked corrections include:

- `NP-CHAR-001`: no chibi / SD / mascot / oversized-head character proportions;
- `NP-PRES-001`: no generated status dashboards as production evidence and no invented completion, approval, path, commit, date, or Phaser claims.

## Legacy-reference salvage

Useful Package 03–05 material studies are preserved under `production/reference/world/shared-foundation/legacy-salvage/` and interpreted by `REFERENCE_SALVAGE_REVIEW.md`. They remain reference-only and may not be cropped or promoted as production assets.

## Shared-foundation benchmark progress

The meaningful production counter is now separated by stage.

### Five-asset benchmark family

1. `stone-clean` — **AUTHORED / SOURCE-QA**
   - source: `production/source/world/shared-foundation/stone-clean.png` — 1920×1280
   - exact runtime derivative: `docs/assets/world/shared-foundation/stone-clean.png` — 192×128
   - QA: `production/qa/world/shared-foundation/stone-clean-candidate-v1.md`
   - runtime registry: disabled

2. `aged-stone-foundation` — **AUTHORED / SOURCE-QA**
   - source: `production/source/world/shared-foundation/aged-stone-foundation.png` — 1920×640
   - exact runtime derivative: `docs/assets/world/shared-foundation/aged-stone-foundation.png` — 192×64
   - QA: `production/qa/world/shared-foundation/aged-stone-foundation-candidate-v1.md`
   - runtime registry: disabled

3. `timber-plaster-wall` — **MISSING**
4. `timber-post` — **MISSING**
5. `horizontal-beam` — **MISSING**

### Accurate counters

- benchmark source assets authored: **2 / 5**
- benchmark assets in source QA: **2 / 5**
- source-approved benchmark assets: **0 / 5**
- exact runtime derivatives physically present: **2 / 5**
- runtime-activated production assets: **0 / 5**
- Phaser-integrated production assets: **0 / 5**
- production-approved assets: **0 / 5**

The manifest now includes `source-qa` in the asset status vocabulary so authored candidates are no longer mislabeled `missing` merely because they have not reached source approval.

## Current material-family intent

`stone-clean` establishes the base civic-stone grammar: dry matte pale/warm stone, irregular authored courses, broken NW highlights, localized chips/grime/repair, cross-block wear, and no visible 32×32 gameplay-grid cadence.

`aged-stone-foundation` intentionally shares that pixel density and lighting while reading older/heavier through larger masonry blocks, deeper joints, darker contact edges, restrained moss, and more concentrated age/grime. It must read as Imperial city fabric rather than dungeon masonry.

Neither asset is source-approved yet. Their current purpose is to establish a coherent two-material family before timber/plaster production.

## Immediate work order

1. review the `stone-clean` + `aged-stone-foundation` pair as one material family;
2. author `timber-plaster-wall` at 1920×1600 → 192×160 using the same effective pixel density and NW lighting;
3. author `timber-post` at 480×1280 → 48×128;
4. author `horizontal-beam` at 1280×480 → 128×48;
5. perform a five-asset source assembly/homogeneity review;
6. repair any style/pixel-density mismatch before source approval;
7. promote only passing assets to `source-approved`, then derive/confirm target-pixel runtime candidates;
8. change manifest + guarded registry to `runtime-candidate` and enable only passing assets;
9. capture the **actual running Phaser canvas** showing traversal, hidden grid, collision, and foreground occlusion;
10. score the integrated Slice 0 scene and repair until 42+ with zero automatic failures and all critical minimums passing.

Do not expand into Harbor/Market prop quantity until this five-asset family is coherent.
