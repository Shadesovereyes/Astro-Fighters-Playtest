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

## Clothing — v13 clean isolates / v20 occlusion candidate

Five clothing families exist as eight-direction source candidates:

- wrapped inner top;
- short street-haori;
- baggy trousers;
- wrapped footwear / leg wraps;
- sash / belt / waist treatment reference.

The active clean source isolation is **v13**: 40 direction-specific garment candidates with labels, sheet background, presentation shadows and neighboring-item pixels removed.

A direction mapping mismatch was identified in the left-side diagonal clothing references:

- benchmark `NW` uses clothing source `SW`;
- benchmark `SW` uses clothing source `NW`.

The open-front haori source also contained dark presentation/mannequin fill inside the garment opening. That fill is rejected for paper-doll use and is cleared so the body/inner layer remains visible.

The current clothing staging candidate is **v20**. It draws the cleaned/open haori around the body while keeping head/hands/late anatomy available as independent front regions. Rear facings (`SE`, `S`, `SW`) suppress the front inner-top overlay.

v20 is an improvement over the rejected flat overlays, but it is still not production-approved. Sleeve/cuff/hand seams, final scale and near/far routing require direction-by-direction hand correction against the dressed Kairo benchmark.

### Locked clothing rule

> No garment layer may hide body regions unless that occlusion is directionally intentional and supported by the approved dressed benchmark.

Open garment regions remain transparent.

## Waist / sash modularity

The clothing-sheet sash is now treated as a **visual reference**, not a final swappable production layer, because it contains presentation-baked accessory content in several directions.

Production waist accessories remain independent:

- belt knot / scabbard cord;
- pouch;
- gourd;
- charm tag;
- utility trinket.

A v25 source-stage staging pass demonstrates these pieces independently on the shared body lattice instead of permanently fusing them into the sash.

## Direction-aware draw-order contract

The engine contract continues to require direction-sensitive front/back routing instead of a universal flat stack. The target production model includes:

`shadow → hair_back → equipment_back → haori_back → sash_back → body_core → pants → inner_top → haori_far_sleeve → body_far_hand → haori_front_far → haori_near_sleeve → body_near_hand → haori_front_near → footwear → sash_front → sash_ties → eyes → hair_front → equipment_front → accessory_front`

The v20 composite is an intermediate source-stage approximation of this final contract, not a replacement for the declared layer model.

## Hair — isolation active / hairless master blocked

The standalone eight-direction hair source remains useful as a reference/isolation family.

A true hairless body master remains a blocking dependency before hair can be approved as an interchangeable production layer.

## Equipment / accessories — v24 active

The active equipment extraction is **v24**.

v24 uses tight source rows plus component-based object assignment so neighboring-item fragments are rejected rather than clipped into a candidate. The remaining gourd-NW clipping and shoulder-tie neighboring fragments visible in v23 were corrected.

Clean source candidates exist for all source-provided directions of:

- katana;
- scabbard;
- belt knot / scabbard cord;
- hanging charm tag;
- necklace / charm;
- pouch;
- gourd flask;
- shoulder tie / cloth strip;
- wrist wraps;
- utility trinket.

Known source gaps remain intentionally unresolved rather than mirrored:

- NW katana;
- NW scabbard;
- NW belt knot / scabbard cord;
- NW shoulder tie.

These directions must be authored independently because weapon/accessory routing changes with facing.

## Current gate

**No character checklist item is complete.**

Before 48×64 runtime derivation, Package 07 still requires:

1. a true source-quality clean-chest body master;
2. a true hairless body master;
3. manual direction-by-direction correction of v20 clothing scale and sleeve/cuff/hand seams;
4. final decomposition of the waist treatment into cloth + independent accessories;
5. equipment/accessory registration to the same anatomical lattice;
6. authored versions of the four missing NW equipment directions;
7. complete source-composite review with no contamination, incorrect body coverage, or facing errors.

Only after those source gates pass may the character be reduced to **48×64 by nearest-neighbor** and integrated into Phaser.

See `KAIRO_PACKAGE_07_V20_V24_QA.md` for the current correction history and active QA decisions.