# Astro Fighters — Paper-Doll Package 01 Status

**Package:** `kairo_package01`  
**Runtime target:** Phaser  
**Status:** reference-derived engineering candidate — **NOT production approved**

## Governing workflow

This package follows the locked sequence:

`reference target → modular derivation → Phaser integration → integrated review`

The locked master direction requires 480×640 source masters, eight distinct facings, shared anchors, and 48×64 runtime derivatives. It also requires actual Phaser integration; a custom Canvas renderer cannot substitute for acceptance.

## Package contents

The staging runtime package contains eight-direction atlases for:

- body
- hair
- wrapped inner top
- street-haori outerwear
- pants
- footwear
- sash / waist treatment
- scabbard
- charm tag
- necklace
- pouch
- gourd flask
- shoulder tie
- contact shadow

`docs/assets/metadata/characters/kairo-package01.json` declares frame size, anchors, direction indexes, per-facing draw order, atlas paths, variants, and final animation requirements.

`docs/js/paperdoll-package01-bridge.js` attaches the layered paper doll to an active Phaser scene and attempts to locate the current player object. `docs/play-v4-paperdoll-package01.html` runs the existing game runtime and injects that Phaser bridge for integration testing.

## Gate result

This package is **not** a character-art completion pass yet.

The current runtime derivatives expose two issues that must be corrected before an art gate:

1. source reference sheets do not yet provide final 480×640 individually authored, perfectly aligned transparent overlays for every module;
2. the 48×64 nearest-neighbor derivatives lose too much of the approved reference detail and require source-stage re-authoring around the shared sample/anchor lattice.

Therefore:

- no character checklist item is struck;
- the current assets are suitable for validating layer replacement, facing routing, frame indexing, Phaser loading, and draw-order behavior only;
- the next autonomous character package must re-author the source overlays at the locked source-frame standard before expanding animation counts.

## Next package

1. Re-author the true hairless base-body + independent eyes source masters at 480×640.
2. Re-author the approved Kairo outfit overlays against those exact anchors rather than free-floating component sheets.
3. Validate all eight idle composites against the approved Kairo turnaround.
4. Derive and inspect 48×64 nearest-neighbor frames.
5. Only after idle alignment/readability passes, expand to idle 4 / walk 6 / ready 2.
6. In parallel, build the first Global Imperial City material reference package beginning with worn Imperial stone street — clean, then derive modular ground/decal assets.
