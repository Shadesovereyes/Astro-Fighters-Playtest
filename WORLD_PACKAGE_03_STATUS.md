# Astro Fighters — World Package 03 v2 Status

**Branch:** `chatgpt/ground-variants-package-03`  
**Pipeline:** reference target → core-style gate → modular derivation → Phaser integration → integrated rubric review

## Why this v2 exists

The first Package 02/03 stone studies were rejected because their source art read as flat rectangular masonry with surface noise and did not meet the locked character-level craftsmanship requirement. This v2 supersedes those visual sources rather than continuing to build on them.

## Reference gate

Reference targets now cover:

- Worn Imperial stone street — clean
- Worn Imperial stone street — cracked
- Patched stone street
- Damp stone variation

The v2 source studies use authored stone-edge breakup, recessed mortar, localized highlight/shadow clusters, mineral/wear variation, explicit fracture behavior, visibly different replacement masonry, and joint-following damp/moss. The family is palette-locked to colors already present in the current Astro Fighters master-palette families.

**Reference-stage verdict:** PASS for continued runtime derivation. This is not the same as checklist completion.

## Runtime derivation

- 4 materials
- 4 macro variants per material
- 16 total runtime patches
- 192×128 per patch
- 768×512 atlas
- exact master-palette-family colors only
- nearest-neighbor source derivation
- no alpha smoothing
- hidden-grid cadence measured on every candidate window before selection

The selected windows all have lower measured contrast at 32px-equivalent boundaries than ordinary local edge contrast. The 192×128 macro step is deliberately decoupled from the hidden 32×32 gameplay grid.

## Phaser integration

`docs/play-v4-ground-package03.html` loads the existing Phaser game and injects:

- Package 03 v2 stone atlas
- Package 03 Phaser ground bridge

Controls:

- **F6** — cycle clean / cracked / patched / damp / mixed
- **F7** — toggle Package 03 ground

The bridge never renders gameplay-grid lines.

## Checklist state

No world checklist item is marked complete yet. The source-reference gate and runtime-derivation gate are passed, but the checklist requires representative integrated Imperial City gameplay with architecture, dressing, props, occlusion, a finished clothed character, and the mandatory rubric threshold.

## Next autonomous dependencies

1. Street-to-building threshold pieces.
2. Aged stone foundation.
3. Timber structural post + horizontal beam family.
4. First authored facade benchmark using those dependencies.
5. Continue Kairo source-master cleanup/anchor validation in parallel; do not accept artifacted Package 01 source layers as production art.
