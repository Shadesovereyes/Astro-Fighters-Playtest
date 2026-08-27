# Kairo — Package 07 v32 Eight-Direction Manual QA

## Milestone

Package 07 now has a **manual source-stage clothing/waist candidate for all eight facings**.

This is the first pass in the package where every direction is represented by a deliberately tuned candidate instead of relying on one universal transform.

Source provenance by direction:

- `N` — v29
- `NE` — v29
- `E` — v29
- `SE` — v30
- `S` — v30
- `SW` — v30
- `W` — v31
- `NW` — v31

## What v32 proves

- all eight directions can be assembled from the clean clothing isolates on the shared 480×640 lattice;
- the open-haori correction prevents the old opaque body-covering failure;
- rear directions suppress the front inner-top overlay;
- left-side source-direction remapping is functioning (`NW` ← source `SW`, `SW` ← source `NW`);
- the all-in-one clothing-sheet sash is no longer required for staging;
- belt knot / pouch / gourd can remain independent modules;
- the manually tuned facings preserve the intended N / NE / E / SE / S / SW / W / NW silhouettes well enough to continue refinement direction-by-direction.

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

The active clean equipment isolation remains **v24**.

A v27 automatic weapon-anchor experiment was tested and rejected as final registration because facing-specific weapon placement still needs manual alignment. That experiment remains useful only as anchor-metadata exploration.

The genuine missing source views remain:

- NW katana
- NW scabbard
- NW belt knot / scabbard cord
- NW shoulder tie

These are still intentionally not mirrored automatically.

## Next source sequence

1. manually polish N sleeve/cuff/hand seams and waist spacing;
2. lock the same landmark method for NE and E;
3. refine SE / S / SW rear equipment and waist depth;
4. refine W / NW profile/front-left overlaps;
5. author the true clean-chest N / NE / E / W body master;
6. author a true hairless body master;
7. register clean equipment manually per facing;
8. author the four missing NW equipment references;
9. run the complete eight-direction source review;
10. only then derive 48×64 nearest-neighbor runtime layers and integrate them into Phaser.

**No character checklist item is complete yet.**