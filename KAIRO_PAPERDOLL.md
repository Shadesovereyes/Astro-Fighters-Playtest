# Kairo Paper-Doll — Current Production Contract

**Status:** active male-character source package; not runtime-final  
**Canonical facing:** `S = front`, `N = back`  
**Source lattice:** `480×640`, center `x=240`, foot-contact `y=560`

## Base underlayer

Male base contains only:

- body / skin
- hair / face
- base shorts

Chest cross-bandages, wrist wraps, leg wraps, footwear, clothing, weapons, scabbards, charms, pouches, and other equipment are independent removable layers.

Future female rule is documented only: base body + hair/face + shorts + sports bra. Female production remains deferred while the male package is active.

## Canonical directions

- `N` — back
- `NE` — back-right 3/4
- `E` — right profile
- `SE` — front-right 3/4
- `S` — front
- `SW` — front-left 3/4
- `W` — left profile
- `NW` — back-left 3/4

Legacy reference-sheet source slots are remapped in metadata rather than repainting correct artwork.

## Anatomical sword rule

The mounted sword belongs to the character's anatomical **left hip** in every facing. Screen-left/screen-right is never the authority.

For `S` / front, the hilt and mount root must read inside the gap between the character's left arm and torso. For `SW` the hilt must remain visibly connected to the left-hip mount. For `W` the scabbard must route on the anatomical left side rather than simply occupying the same screen side as another facing.

## Current modular layer contract

Back-to-front logical order:

1. shadow
2. hair_back
3. equipment_back
4. haori_back
5. sash_back
6. body_core
7. trousers
8. inner_top
9. haori_far_sleeve
10. body_far_hand
11. haori_front_far
12. haori_near_sleeve
13. body_near_hand
14. haori_front_near
15. footwear / leg wraps
16. sash_front
17. sash_ties / belt knot
18. eyes
19. hair_front
20. equipment_front
21. accessory_front

Whole-garment overlays are allowed only when they do not violate the dressed benchmark. If a garment crosses anatomy differently by facing, it must be decomposed into near/far/front/back pieces.

## Required swappable families

- inner top
- haori
- trousers
- sash
- wrist wraps
- leg wraps
- footwear
- scabbard
- belt knot / scabbard cord
- charm tag
- necklace
- shoulder tie
- pouch / utility pouch
- gourd
- other utility attachments

Open garment regions must remain transparent. Presentation-sheet fill, panel background, neighboring-item pixels, labels, dividers, and contact-shadow artifacts are invalid source pixels.

## Current source quality state

The current male reference work established several locked corrections:

- canonical `S = front`, `N = back`
- male base is never nude and always includes shorts
- chest cross-wrap is not part of the base
- sword mount follows anatomical left hip
- `S`, `SW`, and `W` require especially careful hilt/scabbard routing
- garments require direction-aware occlusion rather than a universal flat stack
- modular isolates must be clean before registration

Several earlier automatic registration/segmentation experiments were useful diagnostically but are not production authorities. Final source pixels must come from approved source art and deliberate per-facing registration.

## Current gate

Before 48×64 runtime derivation:

1. lock the clean male base source in all eight directions;
2. complete per-facing clothing registration and near/far routing;
3. complete mounted sword/scabbard registration on anatomical left hip;
4. complete all eight source directions for required equipment, including any genuinely missing source views;
5. approve the full eight-direction modular source composite against the dressed benchmark;
6. only then derive 48×64 frames and manually clean target-resolution pixels;
7. integrate accepted runtime layers into Phaser and perform gameplay review.

No automatically reduced or procedurally healed character asset is pixel-final until it receives manual target-resolution cleanup.

## Repository rule

This file is the current human-readable Kairo contract. `docs/assets/metadata/character/kairo-paperdoll.json` is the current machine-readable contract. Git history stores previous iterations; do not create sequential `v##` copies in the repository.
