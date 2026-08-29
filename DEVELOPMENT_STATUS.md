# Astro Fighters — Current Development Status

**Updated:** 2026-08-28  
**Authoritative production branch:** `main`  
**Active development branch:** `development/slice0-shared-foundation-v1`  
**Draft PR:** #12 — Slice 0 continuous modular Phaser world refactor  
**Current milestone:** Imperial City Early Player Experience v0  
**Current gate:** establish the first coherent shared-foundation source family, then activate approved runtime candidates in Phaser

## Architecture snapshot

Astro Fighters is an **open-world, real-time action-combat RPG**. The active public runtime is Phaser/browser under `/docs`.

The private Unity project is legacy turn-based Combat Strategy reference material only. Reuse useful combat intent/math, but do not restore its turn loop, action-slot queue, hex exploration, IMGUI flow, or Unity roadmap assumptions.

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

## Technical milestone — implemented on active branch

The Phaser refactor seam now provides:

- continuous movement at 104 px/sec;
- delta-time movement;
- normalized diagonals;
- canonical 8-direction facing;
- legacy fixed-step exploration suppressed in refactor mode;
- persistent 32×32 grid graphics hidden;
- legacy baked district background hidden in refactor mode;
- separate world-layer scaffold objects;
- collision independent of appearance imagery;
- foreground Y-depth/occlusion proof;
- explicit scaffold/not-art-review labeling;
- runtime audit through `AF_TEST.worldRefactor()`.

`docs/data/shared-foundation-runtime.json` + `docs/js/shared-foundation-assets-v0.js` add a guarded asset-activation seam. Production PNGs do not replace scaffolds unless their manifest/registry state explicitly allows it and CI confirms the exact runtime path/dimensions.

## Persistent user corrections

`production/NEGATIVE_PROMPT_REGISTER.md` is mandatory.

Current locked corrections include:

- `NP-CHAR-001`: no chibi / super-deformed / mascot / oversized-head player or NPC proportions;
- `NP-PRES-001`: no generated status dashboards as production evidence; no invented completion, approval, runtime, commit, date, path or Phaser claims.

Every future explicit visual correction from the user must be written into that register before related generation continues.

## Legacy-reference salvage — consolidated

The strongest useful Package 03–05 material studies were copied into:

`production/reference/world/shared-foundation/legacy-salvage/`

with interpretation rules in:

`production/reference/world/shared-foundation/REFERENCE_SALVAGE_REVIEW.md`

These files are **reference-only**. They are not source masters, runtime candidates, approvals, or integrated gameplay. Their purpose is to retain good stone/foundation/timber/plaster decisions without importing superseded package architecture.

## First real asset candidate — committed, not promoted

`stone-clean` now has an actual candidate pair:

- source: `production/source/world/shared-foundation/stone-clean.png` — **1920×1280**
- derivative: `docs/assets/world/shared-foundation/stone-clean.png` — **192×128**
- QA: `production/qa/world/shared-foundation/stone-clean-candidate-v1.md`

The source is a 10× pixel-lattice master and its nearest-neighbor 10:1 reduction matches the committed runtime derivative pixel-for-pixel.

This is meaningful asset progress, but it is deliberately **not source-approved and not runtime-activated yet**. The manifest and runtime registry still leave `stone-clean` disabled/missing so the source/reference gate is not bypassed merely because PNG files exist.

Art intent of this candidate:

- dry matte pale/warm Imperial civic stone;
- irregular courses and joint rhythm rather than visible 32×32 cadence;
- NW edge lighting;
- localized chips, grime, cracks, repair and restrained moss;
- cross-block wear;
- no wet-reflective, cyberpunk, steampunk or generic-fantasy drift.

The first earlier five-asset schematic/procedural trial remains rejected for being too flat, generic and low-detail.

## Current machine state

`AF-IC-SHARED-FOUNDATION` remains below runtime-candidate package status.

- `stone-clean`: candidate files exist; machine state intentionally still disabled pending source/reference review
- `aged-stone-foundation`: missing
- `timber-plaster-wall`: missing
- `timber-post`: missing
- `horizontal-beam`: missing
- remaining shared-foundation dependencies: missing
- playable-character benchmark: missing
- approved packages: none

No world or character checklist completion is earned by this candidate alone.

## Immediate work order

1. review/refine `stone-clean` against the salvage reference set and hidden-grid/material rules;
2. author `aged-stone-foundation` to the same effective pixel density and NW lighting;
3. create a two-material source comparison/assembly proving street stone and older foundation belong to one studio while remaining materially distinct;
4. if that comparison passes, continue with `timber-plaster-wall`, `timber-post`, and `horizontal-beam` using the same established pixel grammar;
5. only after source/reference approval, promote passing assets in both `production/asset-manifest.json` and `docs/data/shared-foundation-runtime.json`;
6. let Phaser replace only eligible scaffold textures;
7. capture the **actual running Phaser canvas** with continuous traversal, hidden grid, collision and foreground occlusion;
8. score the integrated Slice 0 scene; repair until 42+ with zero automatic failures and all critical minimums passing.

Do not expand into Harbor/Market prop quantity until this first material/architecture family proves coherent.
