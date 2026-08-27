# Kairo — Package 07 v28 Manual Registration Update

## Purpose

v28 begins the required **direction-by-direction manual source registration** against the approved dressed Kairo benchmark.

This pass intentionally stops trying to solve all eight facings with one generic placement transform.

## Active directions

The first manual tuning pass covers:

- `N`
- `NE`
- `E`

The remaining facings stay pending until these first three establish stable scale/anchor rules.

## Source inputs

- clothing clean isolation: **v13**
- open-haori cleanup / direction remap: retained from the v19/v20 correction path
- equipment clean isolation: **v24**
- shared character lattice: `480×640`, body center `x=240`, foot contact `y=560`

## Manual garment tuning

v28 uses independent per-family source scales rather than the rejected universal whole-garment transform.

Current front/side trial scales:

| Direction | Inner top | Haori | Trousers | Footwear |
| --- | ---: | ---: | ---: | ---: |
| N | 0.72 | 0.96 | 0.94 | 0.82 |
| NE | 0.72 | 0.92 | 0.92 | 0.82 |
| E | 0.74 | 0.88 | 0.90 | 0.80 |

These are source-stage registration values only. They are not runtime scales.

## Waist modularity

The all-in-one clothing-sheet sash is **not used** in the v28 candidate.

Instead, the waist is staged from independent v24 equipment modules:

- belt knot / scabbard cord
- pouch
- gourd

This keeps the waist customization path modular and avoids reintroducing the baked pouch/gourd/charm problem from the clothing reference sheet.

## Current visual result

v28 materially improves scale/placement relative to the earlier generic registration passes, but it is still below final source approval.

Remaining differences against the approved benchmark include:

- exact haori sleeve/cuff contour;
- inner-top collar/opening proportion;
- hand/cuff overlap;
- final trousers hem / lower-leg relationship;
- waist accessory spacing and depth;
- equipment routing and weapon placement;
- the unresolved production clean-chest base body.

## Weapon routing experiment

A separate v27 automatic weapon-anchor test was attempted for katana/scabbard/shoulder-tie placement.

It is **not accepted as production registration**. Automatic hilt/hip anchoring is useful for metadata experiments, but the resulting weapon placement does not match the facing-specific benchmark closely enough. Weapon registration therefore returns to the same manual per-direction process as clothing.

## Gate

No 48×64 derivation is allowed from v28.

The immediate source sequence is:

1. finish N clothing seams and waist spacing;
2. finish NE using the same explicit landmark method;
3. finish E/profile overlap and equipment depth;
4. continue SE → S → SW → W → NW;
5. resolve the source-quality clean-chest and hairless body masters;
6. author the four missing NW equipment references;
7. review the complete eight-direction source composite before runtime reduction.

**No character checklist item is complete yet.**