# Kairo — Package 07 Progress Update

## Direction convention correction

Astro Fighters gameplay uses **`S` as front-facing** and **`N` as back-facing**.

Earlier Package 07 text inherited the reference-sheet slot labels and therefore described `N` as front. That interpretation is superseded. Raw source files may keep their sheet slot labels, but all production/runtime metadata now maps them explicitly to canonical game directions.

Canonical source mapping:

- `N` ← source `S`
- `NE` ← source `SE`
- `E` ← source `E`
- `SE` ← source `NE`
- `S` ← source `N`
- `SW` ← source `NW`
- `W` ← source `W`
- `NW` ← source `SW`

See `KAIRO_PACKAGE_07_DIRECTION_CONVENTION.md`.

## Active source gates

### Shared lattice

The source canvas remains **480×640**, body center `x = 240`, foot-contact `y = 560`.

Character layers use anatomical registration rather than generic object centering/bottom justification.

### Base body

The chest cross-bandage / X-wrap is forbidden on the production body.

The current clean-chest work applies to source slots `N / NE / E / W`, which are canonical **`S / SE / E / W`**.

The clean-chest candidate remains useful for continued source integration but is **not yet production-approved**. Final full-resolution torso review is still required.

Wrist and ankle/lower-leg wraps remain intentional.

### Clothing

Active contamination-free garment isolation: **v13**.

- 40 transparent garment candidates across inner top / haori / trousers / footwear / sash reference;
- no neighboring-item pixels;
- no direction labels / panel borders;
- no source-sheet background;
- no presentation shadow contamination.

The previous two-direction `NW/SW` override is now understood as part of the full canonical source-slot remap rather than a special-case artwork swap.

The open-front haori presentation fill is removed so body / inner layers remain visible.

The active body/garment routing candidate is **v37**. It narrows late body routing to head plus wrist/hand zones so upper forearms do not repaint over haori sleeves.

Rear-facing inner-top suppression now means canonical **`NE / N / NW`**.

v37 is not final. Sleeve/cuff/hand seams and near/far garment routing still require per-facing polish against the approved dressed benchmark.

### Waist modularity

The clothing-sheet sash is not the final swappable waist layer because several facings include presentation-baked pouch / gourd / charm content.

Production keeps these independent:

- belt knot / scabbard cord;
- pouch;
- gourd;
- charm tag;
- utility trinket.

### Hair / hairless body

Standalone eight-direction hair source art is available.

**v39 remains the active hairless-body engineering candidate**. It proves the separation path, but the scalp silhouette and source-level shading still require manual art polish before the hairless body master can be locked.

### Equipment and accessories

Active equipment isolation / shared-lattice registration: **v44**.

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

The equipment sheet lacks source slot `NW`. Under the canonical gameplay convention, the unresolved assets are therefore **canonical `SW`**:

- SW katana;
- SW scabbard;
- SW belt knot / scabbard cord;
- SW shoulder tie.

They are not mirrored automatically because facing-sensitive routing and silhouette matter.

## Anchor / layering rule

> No garment or equipment layer may hide body regions unless that occlusion is directionally intentional and supported by the approved dressed Kairo benchmark.

Open garment regions remain transparent. Pouch, gourd, charm and belt/scabbard-cord content remain independently swappable.

## Current gate

No character checklist item is complete.

Package 07 remains a **source-stage art/engineering candidate** until:

1. the clean-chest body for canonical S / SE / E / W receives final source-art approval;
2. the v39 hairless-body scalp is manually polished and approved;
3. all eight canonical clothing composites receive seam / occlusion polish;
4. waist cloth and accessories are fully separated;
5. v44 equipment anchors are converted into manual per-facing front/back registration;
6. the four missing canonical SW equipment assets are authored from the absent source NW slot;
7. the complete source composite passes review before any 48×64 reduction.

After source approval, runtime derivation must still be manually pixel-cleaned at 48×64 before Phaser promotion.
