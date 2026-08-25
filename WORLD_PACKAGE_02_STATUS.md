# Astro Fighters — Reference Package 02 Status

**Package:** `world_package02_stone_clean`  
**Branch:** `chatgpt/reference-package-02`  
**Primary checklist dependency:** `Worn Imperial stone street — clean`  
**Status:** reference-derived Phaser integration candidate — **NOT checklist-complete**

## Reference-first source target

A dedicated clean Imperial street material reference was authored before runtime derivation.

- source target: 384×256 native pixel art
- review preview: 768×512 nearest-neighbor scale
- palette: exact locked Astro Fighters production colors only
- visual construction: irregular coursed Imperial slabs, staggered joints, restrained pitting/chips, sparse mineral flecks, broad low-frequency wear
- hidden-grid requirement: no authored 32×32 seams or checkerboard cadence

The reference is governed by the approved Imperial City image, locked Master Palette, master art direction, and Global Imperial City ground checklist. It intentionally avoids district-specific dirt, moss, puddles, drainage, cart wear, and cracks because those are separate checklist variants/decal families.

## Modular runtime derivation

Four 192×128 macro variants were derived from the approved source target by nearest-neighbor reduction and non-32-aligned source offsets. They are packed into a 384×256 runtime atlas.

Measured edge-contrast ratios at hidden-grid multiples are below the overall edge average for all four variants:

| Variant | vertical 32 ratio | horizontal 32 ratio |
|---|---:|---:|
| A | 0.466 | 0.250 |
| B | 0.483 | 0.306 |
| C | 0.538 | 0.309 |
| D | 0.599 | 0.350 |

A ratio under 1.0 means the 32-pixel boundaries are less visually pronounced than ordinary internal edges in that axis; this is a diagnostic, not an art-approval score.

## Phaser integration

`docs/play-v4-reference-package02.html` runs the established game and injects both the Package 01 paper doll and Package 02 world bridge.

`docs/js/world-package02-stone-bridge.js`:

- loads the reference-derived stone atlas into the active Phaser scene
- registers four macro frames with nearest filtering
- populates a moving 7×7 macro field around the player/camera
- selects variants deterministically from macro world coordinates
- places the material below the detected player rather than drawing gameplay-grid lines
- exposes F7 as a diagnostic visibility toggle

The macro placement step is 192×128, deliberately unrelated to the hidden 32×32 gameplay grid.

## Gate result

Do **not** strike `Worn Imperial stone street — clean` yet.

The package establishes the required reference → derivative → Phaser path, but completion still requires a representative Imperial City gameplay slice with transitions, architecture, props, occlusion, a fully finished character, and rubric review at the checklist threshold with no automatic failures.

## Next autonomous dependencies

1. Refine the clean stone family in integrated play if macro-edge repetition is visible.
2. Build `Worn Imperial stone street — cracked` as a separate reference/decal package rather than baking cracks into the clean base.
3. Build `Patched stone street` and `Damp stone variation` from the established material language.
4. Begin shared street-to-building threshold / aged stone foundation dependencies so the ground can be judged in representative architecture.
5. Continue Kairo source-master re-authoring in parallel; current Package 01 paper-doll remains engineering-only until true anchor-locked 480×640 source overlays and full animation coverage exist.
