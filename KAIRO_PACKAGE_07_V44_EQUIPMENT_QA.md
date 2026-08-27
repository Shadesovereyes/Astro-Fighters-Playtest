# Kairo — Package 07 v44 Equipment QA

> **Direction-convention correction (2026-08-27):** the equipment reference sheet's absent slot is labeled `NW` in the source sheet, but Astro Fighters canonical gameplay uses `S = front` / `N = back`; source slot `NW` maps to canonical `SW`. Therefore the four missing production equipment views are canonical **SW**, not NW.

## Purpose

v44 advances the equipment/accessory blocker without promoting any runtime art. The pass focuses on two separate gates:

1. contamination-free source isolation;
2. first-pass registration to the shared 480×640 Kairo body lattice.

## v41–v43 rejected extraction attempts

A fresh extraction pass was tested against the equipment reference sheet, but v41/v42 still admitted direction-label fragments and neighboring dense-row objects in several families. Those attempts are rejected as active source art.

v43 tightened the extraction substantially, but the charm-tag row still carried detached direction-label components. It is therefore superseded.

## v44 clean equipment isolation

v44 keeps the clean v43 candidates and rebuilds the hanging charm-tag family as main-component-only objects. The active isolated families are:

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

The isolation rule remains strict: a reusable equipment candidate fails if it contains typography, panel rules, neighboring-object pixels, clipped adjacent variants, or source-sheet background.

The equipment sheet lacks source slot `NW`. Those four genuine source gaps correspond to canonical gameplay `SW` and are intentionally not mirrored:

- SW katana;
- SW scabbard;
- SW belt knot / scabbard cord;
- SW shoulder tie.

## Shared-lattice registration scaffold

The v44 candidates are placed on the existing 480×640 body lattice using family-specific anatomical anchors rather than generic centering:

- necklace → neck/chest anchor;
- wrist wraps → wrist/hand anchor;
- shoulder tie → shoulder anchor;
- belt knot → waist-center anchor;
- pouch / gourd / utility → independent left/right waist anchors;
- charm tag → outer-waist accessory anchor;
- scabbard → waist/back equipment anchor;
- katana → hand/weapon anchor.

This registration is intentionally a **staging scaffold**, not final placement. The QA proves that the equipment families are independent and can share the body lattice; it does not claim that the current anchor offsets match the approved dressed benchmark in every canonical facing.

## Direction-aware routing still required

The next equipment pass must convert the scaffold into per-facing manual registration and split body-crossing equipment into canonical depth slots:

- `equipment_back`;
- `equipment_front`;
- `accessory_front`;
- direction-specific scabbard-cord routing.

Katana-in-hand is not part of the current idle dressed benchmark and must be registered against the hand/weapon stance reference rather than forced into the idle composite.

## Gate

v44 supersedes v24 as the current equipment-isolation candidate for continued engineering review, but **no equipment checklist item is complete**.

Before runtime reduction:

1. manually align idle equipment per canonical facing against the approved dressed turnaround;
2. manually align the katana to the hand/weapon anchor per canonical facing;
3. author the four missing canonical SW equipment views from the absent source NW slot;
4. validate front/back routing wherever scabbard, cord, charm or weapon cross the body;
5. include the equipment stack in the complete eight-direction source review.

No 48×64 derivation is approved by this pass.
