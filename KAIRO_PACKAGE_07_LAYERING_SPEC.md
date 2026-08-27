# Kairo — Package 07 Direction-Aware Layering Specification

**Status:** source-stage engineering contract  
**Applies to:** all Kairo body / clothing / hair / equipment layers before 48×64 derivation

## Canonical direction convention

Astro Fighters gameplay uses **`S` as front-facing / toward camera** and **`N` as back-facing / away from camera**.

The current Kairo reference sheets use source-slot labels that were previously interpreted with `N` as front. Do not rotate or repaint valid source art simply to rename it. Resolve source art through the explicit mapping in `KAIRO_PACKAGE_07_DIRECTION_CONVENTION.md` and `docs/assets/metadata/character/package07-direction-convention.json`.

Canonical-to-source mapping:

- `N` ← source `S`
- `NE` ← source `SE`
- `E` ← source `E`
- `SE` ← source `NE`
- `S` ← source `N`
- `SW` ← source `NW`
- `W` ← source `W`
- `NW` ← source `SW`

All future Phaser-facing state, animation names, runtime manifests and 48×64 assets use canonical gameplay directions.

## Governing rule

The paper doll may not be assembled as a stack of whole-garment stickers. Any garment or equipment item that crosses the body must be decomposed into front/back/near/far pieces as required by the facing.

A layer is invalid if it hides anatomy or another garment merely because it is drawn later. Occlusion must be intentional and must match the approved dressed Kairo turnaround for that direction.

Open garment areas must remain transparent. Presentation-sheet background, mannequin fill, and neighboring-item pixels are automatic failures.

## Shared source lattice

- source canvas: `480×640`
- body center: `x = 240`
- shared foot-contact line: `y = 560`
- all layers use the same origin and anatomical anchors
- character layers are **not** independently centered or bottom-justified

## Active source-stage inputs

- clothing clean isolation: **v13**
- body/garment routing candidate: **v37**
- hairless body candidate: **v39**
- equipment isolation / shared-lattice registration: **v44**

The raw garment and equipment files may retain their reference-sheet source-slot labels. Every production manifest must also expose the canonical gameplay facing explicitly.

The open-front haori source is cleaned of dark presentation/mannequin fill so the inner top/body remains visible through the garment opening.

## Required canonical slots

Back-to-front engine order:

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

Empty slots remain present in metadata when a facing does not show that component.

## Body decomposition

The base body must not be used as a late full-body overlay to repair bad garment stacking. It must be decomposable into at least:

- `body_core` — torso / legs / covered anatomy beneath clothing
- `body_far_hand`
- `body_near_hand`
- head / face area carrying the eye anchor

Hands render after the corresponding sleeve so exposed fingers/wraps do not disappear under outerwear.

The chest cross-bandage / X-wrap is **not part of the approved base body**. Canonical `S / SE / E / W` require a clean bare-torso source master; those correspond to source slots `N / NE / E / W`. Wrist and lower-leg wraps remain separate intentional visual elements and must not be used to reconstruct the removed chest wrap.

## Garment decomposition

### Inner top

Minimum source pieces:

- `inner_top` torso/collar piece

Neck, arm and torso openings must be transparent.

### Haori

A whole haori layer is insufficient for side and 3/4 views. Minimum logical pieces:

- `haori_back`
- `haori_far_sleeve`
- `haori_front_far`
- `haori_near_sleeve`
- `haori_front_near`

Rear-facing directions may collapse front-panel slots to empty layers, but the back mass remains separate.

### Sash / waist

The clothing-sheet sash is treated as a **visual reference only** because several facings contain presentation-baked pouch / gourd / charm content.

Production separation is:

- `sash_back`
- `sash_front`
- `sash_ties`
- `belt_knot` / scabbard cord
- independent pouch
- independent gourd
- independent charm tag
- independent utility trinket

Pouch, gourd, charm and scabbard-cord pixels must never be baked permanently into the base sash.

### Pants / footwear

- `pants`
- `footwear`

Both use the body lattice; footwear inherits the character foot anchors rather than generic prop bottom-justification.

## Canonical direction profiles

| Facing | Visual profile | Near side | Notes |
| --- | --- | --- | --- |
| `N` | back | symmetric | front inner-top/panel slots generally empty; back mass / rear sash visible |
| `NE` | back-right 3/4 | right | front inner-top/panels mostly suppressed; rear haori mass dominates |
| `E` | right profile | right | near sleeve/panel in front; far sleeve/body mass behind |
| `SE` | front-right 3/4 | right | right/near sleeve and panel route in front of torso |
| `S` | front | symmetric | both front panels can be visible; hands remain in front of cuffs |
| `SW` | front-left 3/4 | left | left/near sleeve and panel route in front of torso |
| `W` | left profile | left | near sleeve/panel in front; far sleeve/body mass behind |
| `NW` | back-left 3/4 | left | rear haori mass dominates; front panels mostly suppressed |

This describes depth logic only. Artwork remains independently authored for all eight canonical facings.

## Equipment routing

The active equipment isolation / registration candidate is **v44**. It uses tight source rows plus component-based object assignment; neighboring fragments are rejected instead of being accepted as clipped candidates.

Clean source candidates exist for all source-provided directions of:

- katana
- scabbard
- belt knot / scabbard cord
- charm tag
- necklace
- pouch
- gourd
- shoulder tie
- wrist wraps
- utility trinket

Weapon/equipment layers require direction-sensitive front/back overrides when they cross the body.

At minimum, the katana/scabbard kit must be separable into:

- scabbard body / rear portion → `equipment_back`
- hilt / hand-crossing or viewer-side portion → `equipment_front`
- scabbard cord → front or back slot by facing
- charm / tag → `accessory_front` unless the approved facing clearly routes it behind

The equipment reference sheet lacks source slot `NW`. Under the canonical convention, those missing assets are **canonical `SW`**, not canonical `NW`:

- canonical `SW` katana — missing source slot `NW`
- canonical `SW` scabbard — missing source slot `NW`
- canonical `SW` belt knot / scabbard cord — missing source slot `NW`
- canonical `SW` shoulder tie — missing source slot `NW`

They must be authored independently rather than mirrored automatically.

## Hair / eyes

Hair must support:

- `hair_back`
- `hair_front`
- optional direction-specific side/volume sublayer if a hairstyle needs it

Eyes remain an independent alignment-safe layer. Rear-facing canonical `N` may use an intentionally empty eyes frame; `NE/NW` may also suppress eyes when the approved view does not expose them.

A true hairless source body remains a blocking dependency before interchangeable hair can be approved.

## Source acceptance test

Before runtime derivation, every canonical direction must satisfy all of the following:

- direction identity follows `S = front`, `N = back`
- base body contains no chest cross-bandage
- garment openings are transparent
- no neighboring-source contamination
- no layer floats or sinks relative to the 480×640 body lattice
- hands are not accidentally covered by sleeves
- torso is not covered by opaque presentation fill
- haori near/far relationships match the dressed benchmark
- sash/accessories are independently swappable
- equipment crosses the body with the correct front/back routing
- complete dressed source composite matches the approved Kairo silhouette and facing

Only after this source-stage review passes may the stack be reduced to 48×64 with nearest-neighbor scaling, manually pixel-cleaned at runtime resolution, and integrated into Phaser.
