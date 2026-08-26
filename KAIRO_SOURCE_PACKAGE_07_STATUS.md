# Kairo — Source Package 07 Status

## Goal

Create contamination-free, direction-specific paper-doll source layers from the approved Kairo reference sheets before any runtime reduction or Phaser promotion.

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

## Base body — v5 active

The chest cross-bandages have been removed from the N / NE / E / W base-body source views. Wrist and ankle wraps remain.

This is still a source cleanup candidate, not runtime approval.

## Clothing — v7 isolation / v8 registration active

Five clothing families exist in all eight directions:
- wrapped inner top;
- short street-haori;
- baggy trousers;
- wrapped footwear / leg wraps;
- layered sash / belt / waist treatment.

The earlier flat-overlay registrations are rejected. Review confirmed that cropped clothing art still carried warm-grey sheet background and, in some open garments, opaque interior mannequin/presentation fill. That caused clothing to look pasted over or to cover body regions incorrectly.

### v7 paper-doll cutouts

- all 40 clothing candidates are re-isolated as transparent sources;
- wrapped inner tops expose neck / arm / torso openings;
- front and three-quarter haori candidates receive explicit front-opening cutouts;
- sash sources are re-cropped below the direction-label band;
- trousers and footwear preserve only intended garment pixels.

### v8 source-scale registration

The standalone clothing references are authored larger than the shared body lattice, so v8 applies nearest-neighbor source-scale normalization before placement:

- inner top `0.80×`;
- haori `0.83×`;
- trousers `0.86×`;
- footwear `0.80×`;
- sash `0.82×`.

The v8 registration is visibly closer to the approved dressed Kairo benchmark, but direction-specific seam and occlusion corrections are still required before runtime reduction.

## Hair — v3 active

The eight-direction hair sheet is isolated and registered to the same crown/body lattice. Earlier passes were rejected for detached label/border fragments.

A true hairless body master is still required before interchangeable hair can be considered source-complete.

## Equipment / accessories — v3 active

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

## Current gate

**No character checklist item is complete.**

Before 48×64 runtime derivation, Package 07 still requires:
1. direction-by-direction v8 clothing seam / occlusion correction against the dressed benchmark;
2. a true hairless body master;
3. equipment/accessory registration to the same anatomical lattice;
4. authored versions of the four missing NW equipment directions;
5. a complete source-composite review with no contamination or layering failures.
