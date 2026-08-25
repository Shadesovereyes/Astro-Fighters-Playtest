# Astro Fighters — Art Development Status

**Branch pass:** `chatgpt/art-integration-pass-1`  
**Date:** 2026-08-25  
**Workflow source:** repository `README.md` → locked master art direction → both asset checklists → integrated runtime → rubric.

## Current state

This branch now advances beyond isolated component staging into a **playable integrated art test**:

- `docs/art-integration-pass-1.html`
- `docs/assets/world/imperial_stone_clean_patch_192x128.png`
- `docs/assets/world/market_facade_320x192.png`
- `docs/assets/world/crate_cluster_96x64.png`
- `docs/assets/world/lantern_pole_48x96.png`
- `docs/assets/world/cedar_occluder_96x128.png`
- `docs/assets/world/drain_channel_128x48.png`
- `docs/assets/characters/fighter_urban_haori_8dir_walk3_384x192.png`
- `ART_REVIEW_PASS_01.md`

The integrated page uses the hidden **32×32 square movement grid** structurally but never renders it. Movement is smooth and supports all eight directions. Architecture, cargo, drainage, actor and foreground vegetation are separate runtime layers; the cedar uses a local fade when the player is underneath its canopy.

## World checklist target

The first shared dependency remains:

- **Worn Imperial stone street — clean**

A 192×128 irregular macro patch is now used inside the playable test scene rather than only on a review card. It deliberately avoids 32px paving cadence.

Status: **active / not struck**. Integrated review is 38/50, below the 42+ production threshold.

## Character checklist target

The pass now replaces the bare-body staging condition with a fully visible dressed fighter proof:

- short freeform-loc silhouette;
- wrapped martial inner top;
- short street-haori outer layer;
- loose fighter trousers;
- wrapped boots;
- waist sash;
- scabbard;
- pouch;
- charm tag;
- shoulder tie;
- contact shadow;
- distinct N / NE / E / SE / S / SW / W / NW bodies;
- three movement poses per direction for the test slice.

This is sufficient to remove the mannequin automatic-fail condition for this integrated scene, but it does **not** complete the full character checklist because final idle/walk/ready frame counts and full equipment/accessory validation remain unfinished.

## Rubric gate

See `ART_REVIEW_PASS_01.md`.

**Integrated score: 38 / 50 — internal test candidate.**

Critical minimums pass in this small slice, but the result is not production approved. Therefore **no checklist entries are struck in this pass**.

Primary weaknesses are material variety, lived-in density, monumental/industrial city scale, animation coverage, and macro-ground repetition.

## Verification performed

- JavaScript extracted from `docs/art-integration-pass-1.html` passes `node --check`.
- All referenced local PNG assets exist and decode with expected dimensions.
- The movement table contains all eight direction vectors.
- Collision checks operate on hidden logical cell centers rather than rendered grid lines.
- No permanent grid drawing routine is present in the integrated page.

A Chromium binary is present in the development container, but its headless process does not terminate correctly in this environment, so browser-screenshot automation was not treated as a passing test. A deterministic preview composite was generated locally for art review instead.

## Next automatic continuation

1. Add cracked / patched / damp stone surface variants and irregular macro mixing.
2. Increase architecture hardware, weathering, material micro-variation and street clutter.
3. Add a second Imperial City architecture/infrastructure silhouette.
4. Expand fighter animation coverage and add a fully dressed NPC/profession variant.
5. Re-run integrated rubric review.
6. At 42+, strike only the checklist entries directly demonstrated by the representative runtime scene.
