# Kairo — Package 07 Progress Update

## Active source gates

### Base body

- Shared source lattice remains **480×640**, body center `x = 240`, foot-contact `y = 560`.
- Active clean-body pass: **v5**.
- The chest cross-bandages have been removed from N / NE / E / W source views.
- Wrist and ankle wraps remain because they are separate intended anchors/equipment surfaces.
- Runtime reduction is still blocked.

### Clothing

The previous flat-overlay registration was rejected after review because the clothing reference sheet had been cropped but still contained two different kinds of non-runtime content:

1. opaque warm-grey presentation-sheet background; and
2. opaque interior mannequin/presentation fill inside open garments.

Current active clothing stages:

- **v7 paper-doll isolation** — 40 direction-specific transparent garment candidates across inner top / haori / trousers / footwear / sash;
- wrapped inner tops now expose neck/arm/body openings instead of carrying the mannequin fill;
- front/three-quarter haori candidates receive explicit front-opening cutouts;
- sash sources are re-cropped below direction labels;
- **v8 scaled registration** — source garments are nearest-neighbor normalized to the common body lattice before placement.

Active source-scale normalization:

- inner top `0.80×`
- haori `0.83×`
- trousers `0.86×`
- footwear `0.80×`
- sash `0.82×`

The next gate is direction-by-direction manual seam / occlusion correction against the dressed Kairo benchmark. No 48×64 derivation is allowed yet.

### Hair

- Active hair isolation QA: **v3**.
- Earlier passes were rejected for detached label/border fragments.
- Hair is registered to the same crown/body lattice in all eight directions.
- A true hairless body master is still required before interchangeable hair can be promoted.

### Equipment and accessories

Active equipment isolation QA: **v3** for katana, scabbard, scabbard cord, charm tag, necklace, pouch, gourd, shoulder tie, wrist wraps and utility trinkets.

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
