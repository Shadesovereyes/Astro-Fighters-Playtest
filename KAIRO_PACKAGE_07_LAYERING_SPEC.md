# Kairo — Package 07 Direction-Aware Layering Specification

**Status:** source-stage engineering contract  
**Applies to:** all Kairo body / clothing / hair / equipment layers before 48×64 derivation

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

The chest cross-bandage / X-wrap is **not part of the approved base body**. N / NE / E / W require a clean bare-torso source master. Wrist and lower-leg wraps remain separate intentional visual elements for the current Kairo design and must not be used to reconstruct the removed chest wrap.

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

The current source sheet visually combines waist cloth with accessories. Production separation is:

- `sash_back`
- `sash_front`
- `sash_ties`
- pouch / gourd / charm as independent equipment or accessory layers

Pouch, gourd, charm and scabbard-cord pixels must never be baked permanently into the base sash.

### Pants / footwear

- `pants`
- `footwear`

Both use the body lattice; footwear inherits the character foot anchors rather than generic prop bottom-justification.

## Direction profiles

| Facing | Visual profile | Near side | Notes |
| --- | --- | --- | --- |
| N | front | symmetric | both front panels can be visible; hands remain in front of cuffs |
| NE | front-right 3/4 | right | right/near sleeve and panel route in front of torso |
| E | right profile | right | near sleeve/panel in front; far sleeve/body mass behind |
| SE | back-right 3/4 | right | front panels mostly suppressed; rear haori mass dominates |
| S | back | symmetric | front panel slots generally empty; back mass / rear sash visible |
| SW | back-left 3/4 | left | mirror of SE in depth logic, not a bitmap mirror |
| W | left profile | left | near sleeve/panel in front; far sleeve/body mass behind |
| NW | front-left 3/4 | left | left/near sleeve and panel route in front of torso |

This describes depth logic only. Artwork remains independently authored for all eight facings.

## Equipment routing

Weapon/equipment layers require direction-sensitive front/back overrides when they cross the body.

At minimum, the katana/scabbard kit must be separable into:

- scabbard body / rear portion → `equipment_back`
- hilt / hand-crossing or viewer-side portion → `equipment_front`
- scabbard cord → front or back slot by facing
- charm / tag → `accessory_front` unless the approved facing clearly routes it behind

Missing NW equipment is authored independently; do not mirror another facing as production art.

## Hair / eyes

Hair must support:

- `hair_back`
- `hair_front`
- optional direction-specific side/volume sublayer if a hairstyle needs it

Eyes remain an independent alignment-safe layer. Rear-facing directions may use an intentionally empty eyes frame.

## Source acceptance test

Before runtime derivation, every direction must satisfy all of the following:

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

Only after this source-stage review passes may the stack be reduced to 48×64 with nearest-neighbor scaling and integrated into Phaser.