# Astro Fighters — World Package 03 v5 Status

**Branch:** `chatgpt/ground-variants-package-03`  
**Pipeline:** reference target → core-style gate → modular derivation → Phaser integration → integrated rubric review

## Correction history

Package 02 and the first Package 03 attempts are **superseded as visual sources**. Their paving was too procedural/regular and did not reliably meet the locked character-level material-art requirement. They remain useful engineering history only.

A later synthetic v3 field was also rejected because enlarging the material into a repeating field introduced visible macro repetition. The v5 package therefore avoids edge-to-edge repetition entirely at this gate.

## Reference gate — PASS

The active source anchors are dedicated material studies for:

- Worn Imperial stone street — clean
- Worn Imperial stone street — cracked
- Patched stone street
- Damp stone variation

The accepted anchors now show the material behavior required by the locked master direction:

- irregular worn masonry instead of clean tile geometry
- chipped / rounded stone edges
- recessed dark mortar
- localized wear and mineral variation
- fractures that affect stone bodies rather than appearing as line decals
- repair masonry that is materially different from the surrounding street
- dampness expressed through absorbed darkening, moss, and grime rather than neon highlights
- warm analog / Japandi-industrial restraint

These source anchors are preserved unscaled in `docs/assets/reference/world/package03/`.

## Runtime derivation — PASS for a single module

Each material is represented by one **128×160** runtime module derived by centered crop from the accepted reference anchor with **no enlargement**. Runtime colors are quantized to a restrained subset of the locked master-palette world families.

This package deliberately does **not** tile those modules edge-to-edge. Repeating them created visible macro rhythm even when the hidden 32×32 grid itself was not drawn.

The next ground-construction step is therefore not “more tiling”; it is authored street assembly using:

- street-edge / threshold modules
- foundation modules
- localized surface decals
- authored larger street patches where necessary

## Phaser integration — PASS for staging

`docs/play-v4-ground-package03.html` loads the actual Phaser runtime and injects:

- the Package 01 layered paper-doll engineering candidate
- one Package 03 material module in world space

Controls:

- **F6** — cycle clean / cracked / patched / damp
- **F7** — toggle the material module
- **F8** — toggle the Package 01 paper doll

The material module is placed once in world space and does not follow the camera. No grid lines are rendered and no repeated ground tiling is used.

## Checklist state

**No world checklist item is marked complete.** Reference quality and single-module runtime integration are necessary gates, not the completion gate. Completion still requires representative Imperial City gameplay with architecture, dressing, props, occlusion, a finished production character stack, and the mandatory rubric threshold.

## Next autonomous package

1. Street-to-building threshold reference family.
2. Aged stone foundation reference family.
3. Derive threshold/foundation modules from those references.
4. Integrate the first authored street-edge assembly in Phaser without repeating ground tiles.
5. Begin timber structural post + horizontal beam reference family.
6. Continue Kairo anchor-locked source cleanup in parallel; do not promote Package 01 placeholder-derived source layers to production art.
