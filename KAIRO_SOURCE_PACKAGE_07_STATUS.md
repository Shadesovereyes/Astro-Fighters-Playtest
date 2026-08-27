# Kairo — Source Package 07 Status

## Goal

Create contamination-free, direction-specific paper-doll source layers from the approved Kairo reference sheets before any runtime reduction or Phaser promotion.

The locked character workflow remains:

`480×640 directional master → source review → modular clothing/equipment against shared anchors → direction-aware occlusion review → 48×64 nearest-neighbor runtime derivation → manual pixel cleanup → Phaser integration`

## Canonical direction convention

Astro Fighters gameplay uses **`S` as front-facing / toward camera** and **`N` as back-facing / away from camera**.

The current reference sheets use source-slot labels that were previously interpreted with `N` as front. Those raw slots are preserved only as source identifiers. Production/runtime metadata uses the canonical mapping:

- canonical `N` ← source `S`
- canonical `NE` ← source `SE`
- canonical `E` ← source `E`
- canonical `SE` ← source `NE`
- canonical `S` ← source `N`
- canonical `SW` ← source `NW`
- canonical `W` ← source `W`
- canonical `NW` ← source `SW`

See `KAIRO_PACKAGE_07_DIRECTION_CONVENTION.md` and `docs/assets/metadata/character/package07-direction-convention.json`.

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

The reference-sheet source slots `N / NE / E / W` that contain the unwanted chest-wrap treatment correspond to canonical gameplay **`S / SE / E / W`**.

Current rule:

- canonical `S / SE / E / W` require a true clean bare-torso source edit;
- wrist wraps remain intentionally present for the current Kairo design;
- lower-leg / ankle wraps remain intentionally present;
- the cleaned body must preserve the approved anatomy, skin rendering, silhouette, feet, hair/face anchors and canonical direction identity;
- no 48×64 body derivative may be promoted until this source master is accepted.

A true hairless body master is also still required before interchangeable hair can be source-complete.

## Clothing — v13 clean isolates / v37 routing candidate

Five clothing families exist as eight-direction source candidates:

- wrapped inner top;
- short street-haori;
- baggy trousers;
- wrapped footwear / leg wraps;
- sash / belt / waist treatment reference.

The active clean source isolation is **v13**: 40 direction-specific garment candidates with labels, sheet background, presentation shadows and neighboring-item pixels removed.

The earlier left-diagonal `NW/SW` mismatch is now resolved by the full canonical source-slot mapping rather than a special-case gameplay direction override.

The open-front haori source contained dark presentation/mannequin fill inside the garment opening. That fill is rejected for paper-doll use and is cleared so the body/inner layer remains visible.

The active body/garment routing candidate is **v37**. It keeps head plus wrist/hand regions available as late body layers while upper forearms remain behind the haori sleeve unless the approved benchmark requires otherwise.

Rear-facing inner-top suppression now applies to canonical `NE / N / NW`.

v37 is still not production-approved. Sleeve/cuff/hand seams, final scale and near/far routing require direction-by-direction hand correction against the dressed Kairo benchmark.

### Locked clothing rule

> No garment layer may hide body regions unless that occlusion is directionally intentional and supported by the approved dressed benchmark.

Open garment regions remain transparent.

## Waist / sash modularity

The clothing-sheet sash is treated as a **visual reference**, not a final swappable production layer, because it contains presentation-baked accessory content in several directions.

Production waist accessories remain independent:

- belt knot / scabbard cord;
- pouch;
- gourd;
- charm tag;
- utility trinket.

## Direction-aware draw-order contract

The engine contract requires direction-sensitive front/back routing instead of a universal flat stack:

`shadow → hair_back → equipment_back → haori_back → sash_back → body_core → pants → inner_top → haori_far_sleeve → body_far_hand → haori_front_far → haori_near_sleeve → body_near_hand → haori_front_near → footwear → sash_front → sash_ties → eyes → hair_front → equipment_front → accessory_front`

All slots are resolved using canonical gameplay facings, not implicit reference-sheet labels.

## Hair — isolation active / hairless master blocked

The standalone eight-direction hair source remains useful as a reference/isolation family.

The current hairless-body engineering candidate proves the separation path, but a source-quality scalp/hairline cleanup remains a blocking dependency before interchangeable hair can be approved.

## Equipment / accessories — v44 active

The active equipment isolation / shared-lattice registration candidate is **v44**.

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

The equipment sheet lacks source slot `NW`. Under the canonical gameplay convention, the missing production direction is therefore **canonical `SW`**:

- SW katana;
- SW scabbard;
- SW belt knot / scabbard cord;
- SW shoulder tie.

These must be authored independently rather than mirrored because weapon/accessory routing changes with facing.

## Current gate

**No character checklist item is complete.**

Before 48×64 runtime derivation, Package 07 still requires:

1. a true source-quality clean-chest body for canonical S / SE / E / W;
2. a true hairless body master;
3. manual direction-by-direction correction of clothing scale and sleeve/cuff/hand seams using canonical facings;
4. final decomposition of the waist treatment into cloth + independent accessories;
5. manual per-facing equipment/accessory front/back registration;
6. authored versions of the four missing canonical SW equipment assets from the absent source NW slot;
7. complete source-composite review with no contamination, incorrect body coverage, or facing errors.

Only after those source gates pass may the character be reduced to **48×64 by nearest-neighbor**, manually pixel-cleaned at runtime resolution, and integrated into Phaser.
