# Astro Fighters — World Package 04 Status

**Branch:** `chatgpt/threshold-foundation-package-04`  
**Pipeline:** reference target → core-style gate → modular derivation → Phaser integration → integrated rubric review

## Package targets

This package advances the next shared Imperial City structural dependencies after the corrected stone material family:

- Street-to-building threshold pieces
- Aged stone foundation
- Timber structural post + horizontal beam corner dependency

## Reference gate — PASS for continuation

The active Package 04 reference family was developed before runtime extraction and is judged against the locked Master Art Direction Prompt, approved Kairo reference, Imperial City benchmark, and master palette.

The accepted references show:

- worn, irregular stone rather than clean tile geometry
- chipped/rounded stone edges and recessed mortar
- distinct plaster, timber, stone, metal, foliage, and lantern behavior
- age/wear concentrated at believable structural contact points
- Edo daily-life building construction with warm analog-industrial detailing
- foundations that visibly carry timber/plaster structures instead of reading as decoration pasted over boxes
- threshold steps that create believable street/building elevation transitions
- no visible 32×32 gameplay-grid treatment

The full reference anchors remain project art-production artifacts and were palette-locked without resizing before runtime extraction. The public playtest branch carries a nearest-neighbor review preview rather than duplicating the full source masters. This is a source/reference gate only, not a checklist completion claim.

## Runtime derivation

The initial Phaser staging set contains five transparent modular assets:

- threshold
- foundation — low
- foundation — mid
- foundation — high
- timber post + beam corner

All runtime assets use hard alpha and exact locked world-palette colors. They are isolated from the approved Package 04 reference family and are not enlarged runtime reconstructions masquerading as source art.

## Phaser integration

`docs/play-v4-threshold-foundation-package04.html` loads the actual Phaser runtime and stages Package 01 + Package 03 + Package 04 together.

Controls:

- **F4** — toggle Package 04 structural staging
- **F5** — cycle low / mid / high foundation
- **F6** — cycle Package 03 clean / cracked / patched / damp ground material
- **F7** — toggle Package 03 ground module
- **F8** — toggle Package 01 paper doll

The Package 04 post/beam uses a simple north/south depth test relative to the controlled character so the player can render behind or in front of the vertical structural element. This is an occlusion staging check, not final authored collision/cutaway behavior.

## Checklist state

**No checklist item is marked complete yet.** The source and isolated-module gates are passed, but completion still requires a representative Imperial City facade/street assembly, collision and interaction authoring, dressing/props, finished production character presentation, and the mandatory integrated rubric threshold.

## Next autonomous dependencies

1. Timber structural post family expansion.
2. Horizontal beam family expansion.
3. Timber-and-plaster wall benchmark and modular wall set.
4. First authored facade benchmark assembled from Package 04 + wall/roof dependencies.
5. Common architectural dressing: lantern mount, hanging lantern, sign mount, vertical signboard.
6. Continue Kairo anchor-locked source cleanup in parallel before promoting the paper-doll art beyond engineering-candidate status.
