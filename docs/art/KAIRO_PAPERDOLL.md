# Kairo Male Paper-Doll — Current Production Contract

**Status:** source-stage; runtime promotion blocked  
**Scope:** male player character only

This file is the current Kairo paper-doll authority. Git history stores superseded package iterations; do not create new `v##` status/spec files.

## Canonical facing

Astro Fighters uses:

- `N` = back
- `NE` = back-right 3/4
- `E` = right profile
- `SE` = front-right 3/4
- `S` = front / toward camera
- `SW` = front-left 3/4
- `W` = left profile
- `NW` = back-left 3/4

Legacy Kairo sheet labels are remapped in `docs/assets/characters/kairo/kairo-manifest.json`. Runtime/Phaser names always use canonical directions.

## Shared source lattice

- source canvas: **480×640**
- body center: **x = 240**
- foot-contact line: **y = 560**
- runtime target: **48×64**
- every paper-doll layer shares the same anatomical lattice
- character layers are not independently centered or bottom-justified

## Base underlayer

The male base is never nude. It contains only:

- body / skin
- hair / face
- **base shorts**

The following are modular and must not be baked into the male base:

- chest wraps
- wrist wraps
- leg wraps
- footwear
- inner top
- outerwear
- trousers
- sash
- weapons / scabbards
- charms / pouches / other equipment

Future female rule is documented but not in active production: **body / skin + hair / face + base shorts + sports bra**.

## Anatomical equipment rule

Equipment placement follows the character's anatomy, not screen-left / screen-right.

Kairo's mounted sword belongs to his **anatomical left hip** in every facing. In canonical `S`, the hilt/mount must read inside the left-arm / torso relationship. `SW` and `W` must preserve the same anatomical mount as the body rotates.

## Modular layer inventory

Current logical slots, back to front:

1. `shadow`
2. `hair_back`
3. `equipment_back`
4. `haori_back`
5. `sash_back`
6. `body_core`
7. `pants`
8. `inner_top`
9. `haori_far_sleeve`
10. `body_far_hand`
11. `haori_front_far`
12. `haori_near_sleeve`
13. `body_near_hand`
14. `haori_front_near`
15. `footwear`
16. `sash_front`
17. `sash_ties`
18. `eyes`
19. `hair_front`
20. `equipment_front`
21. `accessory_front`

Whole-garment overlays are invalid whenever they cover anatomy that should remain visible. Open garment areas remain transparent.

Waist accessories remain independently swappable: belt knot / scabbard cord, pouch, gourd, charm tag, and utility attachment are not permanently baked into the sash.

## Direction-sensitive routing

- `N`: back; front panels empty/minimal
- `NE`: back-right 3/4; right is near side; rear mass dominates
- `E`: right profile; right/near sleeve and panel route in front
- `SE`: front-right 3/4; right/near sleeve and panel route in front
- `S`: front; both front panels may be visible; hands remain in front of cuffs
- `SW`: front-left 3/4; left/near sleeve and panel route in front
- `W`: left profile; left/near sleeve and panel route in front
- `NW`: back-left 3/4; rear mass dominates

## Current source state

Accepted development facts:

- clean eight-direction male base-underlayer visual direction is established
- chest cross-bandage is not part of the production base
- clothing/equipment must be isolated without neighboring pixels, labels, panel rules, checkerboard/paper background, or presentation shadows
- source components are reviewed before runtime reduction
- source registration is performed direction-by-direction against the approved dressed benchmark
- automatic segmentation/template matching may diagnose problems but is not final-pixel authority

Known unresolved source blocker:

The equipment reference lacks legacy source slot `NW`, which maps to canonical **`SW`**. The following canonical `SW` assets must be independently authored rather than mirrored automatically:

- katana
- scabbard
- belt knot / scabbard cord
- shoulder tie

## Source approval gate

Do not derive/promote final 48×64 paper-doll art until all eight source directions pass:

- correct canonical direction
- base body/shorts integrity
- clean garment openings
- clean isolation
- shared-lattice registration
- hand / cuff / sleeve seam correctness
- haori near/far routing
- sash/accessory modularity
- anatomical left-hip weapon routing
- complete eight-direction dressed source composite comparison

After source approval, derive 48×64 once, manually clean target pixels, validate palette/alpha/anchors, then integrate into Phaser.

## Repository rule

Keep only the current production contract, current manifest, accepted source/runtime assets, and concise current status. Failed experiments and QA generations remain outside Git. Stable paths replace versioned package filenames.
