# Kairo — Package 07 v28 Manual Registration Update

> **Direction-convention correction (2026-08-27):** this historical QA uses reference-sheet/source-slot labels. Canonical gameplay uses `S = front`, `N = back`; map source slots through `KAIRO_PACKAGE_07_DIRECTION_CONVENTION.md`. Thus the v28 source-slot sequence `N → NE → E` corresponds to canonical `S → SE → E`, and the absent source `NW` equipment slot corresponds to canonical `SW`.

## Purpose

v28 begins the required **direction-by-direction manual source registration** against the approved dressed Kairo benchmark.

This pass intentionally stops trying to solve all eight facings with one generic placement transform.

## Active directions

The first manual tuning pass covers source slots:

- `N` → canonical `S`
- `NE` → canonical `SE`
- `E` → canonical `E`

The remaining facings stay pending until these first three establish stable scale/anchor rules.

## Source inputs

- clothing clean isolation: **v13**
- open-haori cleanup / source-slot remap retained from the v19/v20 correction path
- equipment clean isolation: **v24**
- shared character lattice: `480×640`, body center `x=240`, foot contact `y=560`

## Manual garment tuning

v28 uses independent per-family source scales rather than the rejected universal whole-garment transform.

Current source-slot trial scales:

| Source slot | Canonical facing | Inner top | Haori | Trousers | Footwear |
| --- | --- | ---: | ---: | ---: | ---: |
| N | S | 0.72 | 0.96 | 0.94 | 0.82 |
| NE | SE | 0.72 | 0.92 | 0.92 | 0.82 |
| E | E | 0.74 | 0.88 | 0.90 | 0.80 |

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

The canonical continuation sequence is:

1. finish canonical S clothing seams and waist spacing;
2. finish canonical SE using the same explicit landmark method;
3. finish canonical E/profile overlap and equipment depth;
4. continue canonical NE → N → NW → W → SW;
5. resolve the source-quality clean-chest and hairless body masters;
6. author the four missing canonical SW equipment references;
7. review the complete eight-direction source composite before runtime reduction.

**No character checklist item is complete yet.**