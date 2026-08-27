# Kairo Male Paper-Doll Layer Contract v46

## Canonical facing
S = front. N = back.

## Shared player canvas
- source canvas: 480×640
- character center: x=240
- foot contact: y=560
- all layer positions in `docs/assets/metadata/character/package07-male-layer-positions-v45.csv` are absolute pixels relative to this canvas

## Base underlayer
The male base is never nude. It contains only:
- body / skin
- hair / face
- **base shorts**

Chest cross-bandages, wrist wraps, lower-leg wraps, footwear, weapons, charms, and other clothing/equipment are **not** baked into the production male base. They remain independent removable layers.

Future female base rule is documented only: **base shorts + sports bra**. No female production is included in this package.

## Non-base modular layers
- inner top
- haori
- trousers
- footwear / leg wraps
- sash
- wrist wraps
- scabbard / mounted weapon support
- belt knot / scabbard cord
- charm tag
- necklace
- pouch
- gourd
- shoulder tie
- utility attachment

Every layer is exported on the same 480×640 transparent canvas. This means swapping a layer does not require guessing its offset; its pixel position is already encoded.

## Sword mount
The mounted sword belongs to the character's anatomical **left hip** in every facing. Screen-left/screen-right is not the rule.

For canonical **S / front**, the mount root and hilt must read inside the gap between the character's left arm and torso.

## Current gate
This is a source-layer registration candidate, not final runtime art. The v46 base removes non-underwear wrap content as an engineering/source cleanup candidate, but the bare-skin chest/wrist/foot pixels still require a hand-authored pixel cleanup pass before production approval. Final 48×64 assets still require nearest-neighbor derivation followed by manual target-resolution pixel cleanup. Missing canonical SW mounted-weapon support remains a source-stage blocker.