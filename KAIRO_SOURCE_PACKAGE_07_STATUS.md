# Kairo — Source Package 07 Status

## Goal

Create contamination-free, direction-specific paper-doll source layers from the approved Kairo reference sheets before any runtime reduction or Phaser promotion.

The locked character workflow remains:

`480×640 directional master → source review → modular clothing/equipment against shared anchors → direction-aware occlusion review → 48×64 nearest-neighbor runtime derivation → Phaser integration`

## Isolation rule

A modular source layer automatically fails if it contains:

- pixels from a neighboring item;
- row labels / panel borders / call-out art;
- detached presentation shadows;
- unrelated decoration from another direction;
- opaque presentation-sheet background;
- opaque mannequin/interior fill where an open garment should expose the body or an inner layer.

## Shared body lattice

All character layers use the same **480×640** source canvas with:

- body center `x = 240`;
- foot-contact line `y = 560`;
- direction-specific anatomical registration.

Character layers are not independently centered or bottom-justified like world props. Body registration takes priority.

## Base body — clean-chest correction REQUIRED

The desired Kairo base body does **not** contain the chest cross-bandage / X-wrap.

The earlier Package 07 text said the N / NE / E / W chest wraps were already removed. That was too strong. The procedural cleanup attempts do not meet the approved source-art quality bar and are rejected as production evidence.

Current rule:

- N / NE / E / W require a true clean bare-torso source edit;
- wrist wraps remain intentionally present for the current Kairo design;
- lower-leg / ankle wraps remain intentionally present;
- the cleaned body must preserve the approved anatomy, skin rendering, silhouette, feet, hair/face anchors and direction identity;
- no 48×64 body derivative may be produced until this source master is accepted.

A true hairless body master is also still required before interchangeable hair can be source-complete.

## Clothing — clean isolates retained; flat whole-garment stacking REJECTED

Five clothing families exist as eight-direction source candidates:

- wrapped inner top;
- short street-haori;
- baggy trousers;
- wrapped footwear / leg wraps;
- sash / belt / waist treatment.

The useful result from the earlier passes is the **source isolation work**: open garment areas must be transparent and neighboring/background contamination is rejected.

The whole-garment registration experiments are **not** accepted as the production layer model. Review showed that a flat `body → inner top → whole haori → sash` stack can cover anatomy incorrectly in side and 3/4 views.

### Active layering contract

Package 07 now has an explicit direction-aware contract in:

- `KAIRO_PACKAGE_07_LAYERING_SPEC.md`
- `docs/assets/metadata/character/package07-kairo-layer-order-v1.json`

The production paper doll must support front/back/near/far decomposition where required.

Minimum outerwear/waist decomposition now includes:

- `haori_back`
- `haori_far_sleeve`
- `haori_front_far`
- `haori_near_sleeve`
- `haori_front_near`
- `sash_back`
- `sash_front`
- `sash_ties`

The body must expose separate hand regions so hands can render after sleeve cuffs without using a late full-body overlay to hide bad garment registration.

### Locked clothing rule

> No garment layer may hide body regions unless that occlusion is directionally intentional and supported by the approved dressed benchmark.

Open garment regions remain transparent. Pouch, gourd, charm and scabbard-cord pixels are independent equipment/accessory modules, not permanently baked into the sash.

## Direction-aware draw order

The engine contract now declares a canonical source stack with direction-specific empty/near/far overrides:

`shadow → hair_back → equipment_back → haori_back → sash_back → body_core → pants → inner_top → haori_far_sleeve → body_far_hand → haori_front_far → haori_near_sleeve → body_near_hand → haori_front_near → footwear → sash_front → sash_ties → eyes → hair_front → equipment_front → accessory_front`

This follows the locked requirement that direction-sensitive clothing overlap and equipment crossing be handled explicitly rather than by a universal flat stack.

## Hair — isolation active / hairless master blocked

The standalone eight-direction hair source remains useful as a reference/isolation family.

A true hairless body master remains a blocking dependency before hair can be approved as an interchangeable production layer.

## Equipment / accessories — isolation candidate

Direction-specific source candidates exist for:

- katana in hand;
- scabbard at waist;
- scabbard cord / belt knot;
- hanging charm tag;
- necklace / charm;
- pouch;
- gourd flask;
- shoulder tie / cloth strip;
- wrist wraps;
- utility belt trinket.

Known source gaps remain intentionally unresolved rather than mirrored:

- NW katana;
- NW scabbard;
- NW scabbard cord;
- NW shoulder tie.

These directions must be authored independently because weapon/accessory routing changes with facing.

## Current gate

**No character checklist item is complete.**

Before 48×64 runtime derivation, Package 07 still requires:

1. a true source-quality clean-chest body master;
2. a true hairless body master;
3. re-authoring the haori/sash as direction-aware front/back/near/far paper-doll sublayers;
4. direction-by-direction seam and occlusion correction against the approved dressed Kairo benchmark;
5. equipment/accessory registration to the same anatomical lattice;
6. authored versions of the four missing NW equipment directions;
7. complete source-composite review with no contamination, incorrect body coverage, or facing errors.

Only after those source gates pass may the character be reduced to **48×64 by nearest-neighbor** and integrated into Phaser.