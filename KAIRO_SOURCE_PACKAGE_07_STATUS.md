# Kairo — Source Package 07 Status

## Goal

Create contamination-free, direction-specific paper-doll source layers from the approved Kairo reference sheets before any runtime reduction or Phaser promotion.

## Current pass

The five clothing families from `astro_fighters_kairo_clothing_components.png` were isolated as independent source assets for all eight directions:

- wrapped inner top
- short street-haori
- baggy trousers
- wrapped footwear / leg wraps
- layered sash / belt / waist treatment

This produces 40 direction-specific source candidates.

## Isolation rule

A modular source layer automatically fails if it contains:
- pixels from a neighboring item
- row labels / panel borders / call-out art
- detached presentation shadows
- unrelated decoration from another direction

Object bounds are family- and direction-specific; the extractor does not assume every row shares identical rectangular cells.

## Important remaining gate

These are **clean source isolates**, not yet anchor-locked paper-doll layers.

Before runtime derivation, every direction must be registered against the same 480×640 Kairo body anchor lattice and compared against the fully dressed eight-direction Kairo benchmark. Hair, eyes/face treatment, equipment and accessory layers must then use that same lattice.

No character checklist item is complete.


## Shared body lattice — registration scaffold v1

The 40 clean clothing isolates have now been placed onto a common **480×640** source canvas.

Current deterministic registration rules:
- shared horizontal body center: `x = 240`
- shared foot-contact line: `y = 560`
- base-body reference figures are centered horizontally and registered to the same foot line
- footwear is foot-contact anchored
- trousers and sash use the shared waist region
- inner top and haori use shared shoulder/chest regions

This is a **registration scaffold**, not final production approval. The current approved base-body reference still includes hair and presentation underlayers, and the clothing pieces have not yet been re-authored where necessary for exact overlap with the fully dressed Kairo turnaround.

Next character gate:
1. compare every direction against the fully dressed Kairo benchmark;
2. adjust each layer on the lattice until seams/overlaps are correct;
3. isolate hair and equipment/accessories using the same contamination rule;
4. only then derive runtime paper-doll layers.


## Paper-doll anchor rule

Character layers are exempt from generic floor-prop anchoring. Every Kairo clothing, hair, face, equipment and accessory layer must occupy the same **480×640 body canvas** and inherit the approved body master’s anatomical anchor lattice.

Required shared anchors:
- head / crown
- shoulders
- torso center
- waist
- left/right hand attachment
- left/right foot placement / ground contact

Layers must not be independently centered or bottom-justified if doing so changes their relationship to the body. Registration against the body master takes priority.

## Shared body lattice — v2 cleanup

The body and fully dressed Kairo benchmarks have been re-extracted without presentation labels or floor-shadow strokes and placed on the same 480×640 canvas with:

- horizontal body center `x = 240`
- shared foot-contact line `y = 560`

The five clothing families are registered onto that same body canvas for all eight directions. This v2 scaffold also carries a direction-specific horizontal offset derived from the dressed-vs-body silhouette so side/three-quarter clothing is not blindly re-centered.

This remains a registration scaffold, not final overlap approval. The QA sheet compares:
1. clean body lattice,
2. fully dressed Kairo benchmark,
3. current modular clothing registration.

The next pass must correct individual layer seams against the fully dressed benchmark before runtime reduction.

## Shared body lattice — v3 cleanup

The body and dressed benchmark segmentation was rebuilt against the sheet's known warm-grey background instead of estimating background from each crop. This removes the remaining rectangular paper contamination seen in the v2 QA.

The v3 QA is now the active registration review. It remains a scaffold: individual clothing seams still require hand correction against the dressed benchmark before runtime reduction.

## Shared body lattice — v4 active QA

The v3 body/dressed extraction still showed residual sheet-background blocks in several directions. It has been replaced.

The active v4 extraction uses the known sheet background color with a stronger distance threshold and removes detached presentation labels/contact-shadow strokes before alignment. The v4 QA is the current reference for body/clothing registration.

This does **not** make the clothing production-ready. The next gate is direction-by-direction seam correction against the dressed Kairo benchmark.
