# Kairo — Package 07 v32 Eight-Direction Manual QA

> **Direction-convention correction (2026-08-27):** this historical QA uses reference-sheet/source-slot labels. Canonical gameplay uses `S = front` and `N = back`. Translate all direction names through `KAIRO_PACKAGE_07_DIRECTION_CONVENTION.md`. Source slot `NW` corresponds to canonical `SW`; source slot `SW` corresponds to canonical `NW`.

## Milestone

Package 07 now has a **manual source-stage clothing/waist candidate for all eight source facings**.

This is the first pass in the package where every direction is represented by a deliberately tuned candidate instead of relying on one universal transform.

Source provenance by source slot:

- `N` — v29 → canonical `S`
- `NE` — v29 → canonical `SE`
- `E` — v29 → canonical `E`
- `SE` — v30 → canonical `NE`
- `S` — v30 → canonical `N`
- `SW` — v30 → canonical `NW`
- `W` — v31 → canonical `W`
- `NW` — v31 → canonical `SW`

## What v32 proves

- all eight source directions can be assembled from the clean clothing isolates on the shared 480×640 lattice;
- the open-haori correction prevents the old opaque body-covering failure;
- rear source slots suppress the front inner-top overlay;
- the left-side source-slot relationship is understood within the full canonical mapping;
- the all-in-one clothing-sheet sash is no longer required for staging;
- belt knot / pouch / gourd can remain independent modules;
- the manually tuned source facings preserve the intended silhouettes well enough to continue refinement direction-by-direction.

## What v32 does **not** prove

v32 is **not production-approved source art** and is not a 48×64 runtime candidate.

Visible differences against the approved dressed benchmark still include some combination of:

- exact haori sleeve and cuff contour;
- hand/cuff overlap;
- inner-top collar/opening proportion;
- trousers hem and lower-leg relationship;
- waist accessory spacing/depth;
- missing weapon/scabbard routing in the manual clothing composites;
- the unresolved true clean-chest source body;
- the unresolved hairless source body.

## Equipment

The active equipment work has since advanced beyond v24, but this historical pass recorded the genuine missing source slot as `NW`. Under the locked canonical convention that means the missing production facing is **canonical `SW`**.

Missing canonical SW assets:

- SW katana
- SW scabbard
- SW belt knot / scabbard cord
- SW shoulder tie

These are still intentionally not mirrored automatically.

## Next source sequence

Using canonical facings, the continuation sequence becomes:

1. manually polish S sleeve/cuff/hand seams and waist spacing;
2. lock the same landmark method for SE and E;
3. refine NE / N / NW rear equipment and waist depth;
4. refine W / SW profile/front-left overlaps;
5. author the true clean-chest S / SE / E / W body master;
6. author a true hairless body master;
7. register clean equipment manually per facing;
8. author the four missing SW equipment references;
9. run the complete eight-direction source review;
10. only then derive 48×64 nearest-neighbor runtime layers, manually pixel-clean them, and integrate them into Phaser.

**No character checklist item is complete yet.**