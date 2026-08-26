# Kairo — Package 07 Progress Update

## Active source gates

### Base body

- Shared source lattice remains **480×640**, body center `x = 240`, foot-contact `y = 560`.
- Active clean-body pass: **v5**.
- The chest cross-bandages have been removed from N / NE / E / W source views.
- Wrist and ankle wraps remain because they are separate intended anchors/equipment surfaces.
- Runtime reduction is still blocked.

### Clothing

The previous flat-overlay registration was rejected because the clothing reference sheet had been cropped but still contained opaque warm-grey presentation-sheet background and opaque mannequin/interior fill inside open garments.

Current active clothing stages:

- **v7 paper-doll isolation** — 40 direction-specific transparent garment candidates across inner top / haori / trousers / footwear / sash;
- wrapped inner tops expose neck/arm/body openings;
- front/three-quarter haori candidates receive explicit front-opening cutouts;
- sash sources are re-cropped below direction labels;
- **v8 scaled registration** — source garments are nearest-neighbor normalized to the common body lattice before placement.

Active source-scale normalization:

- inner top `0.80×`
- haori `0.83×`
- trousers `0.86×`
- footwear `0.80×`
- sash `0.82×`

The next clothing gate is direction-by-direction manual seam / occlusion correction against the dressed Kairo benchmark. No 48×64 derivation is allowed yet.

### Hair

- Active standalone hair isolation QA remains **v3**.
- Two experimental hairless-body reconstructions were attempted and rejected; neither is accepted as the body master because the reconstructed scalp/head geometry was not clean enough.
- A true hairless body master therefore remains a blocking source dependency.

### Equipment and accessories

Active equipment isolation QA is now **v8**.

The upper weapon/charm rows retain the clean v3 isolates. The dense pouch / gourd / shoulder-tie / wrist-wrap / utility rows were rebuilt with row-wide connected-component extraction so each candidate consists only of the detected object pixels rather than a manually centered rectangle.

This specifically eliminates the clipped-neighbor problem that remained in the earlier dense-row passes.

Known source coverage gaps remain intentionally unresolved:

- katana in hand — NW missing
- scabbard at waist — NW missing
- scabbard cord / belt knot — NW missing
- shoulder tie / cloth strip — NW missing

These directions will be authored rather than mirrored automatically because weapon/accessory routing is facing-dependent.

## Anchor policy

World props may use host-specific center/bottom/top mount justification. Character paper-doll layers do not. Every Kairo body, clothing, hair, face, equipment and accessory layer must inherit the same anatomical body lattice.

## Current gate

No character checklist item is complete. Package 07 remains a **source-registration candidate** until all eight v8 clothing composites are manually corrected, a true hairless body master exists, equipment is registered to the same lattice, the four missing NW equipment directions are authored, and the complete source composite passes review before any 48×64 runtime derivation.
