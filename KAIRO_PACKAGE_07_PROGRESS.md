# Kairo — Package 07 Progress Update

## Active source gates

### Shared lattice

The source canvas remains **480×640**, body center `x = 240`, foot-contact `y = 560`.

Character layers use anatomical registration rather than generic object centering/bottom justification.

### Base body

The chest cross-bandage / X-wrap is forbidden on the production body.

**Active clean-chest candidate: v35.**

v35 removes the wrap from N / NE / E / W while preserving the approved source art outside the torso correction region. It supersedes the earlier broad procedural cleanup attempts.

The clean-chest candidate is now good enough for continued source integration, but it is **not yet marked production-approved**. Final full-resolution torso review is still required.

Wrist and ankle/lower-leg wraps remain intentional.

A true hairless body master is still required before interchangeable hair can be source-complete.

### Clothing

Active contamination-free garment isolation: **v13**.

- 40 transparent garment candidates across inner top / haori / trousers / footwear / sash reference;
- no neighboring-item pixels;
- no direction labels / panel borders;
- no source-sheet background;
- no presentation shadow contamination.

Direction-source correction remains:

- benchmark `NW` ← clothing source `SW`;
- benchmark `SW` ← clothing source `NW`.

The open-front haori presentation fill is removed so body / inner layers remain visible.

Direction-specific manual placement has now been established across all eight facings:
- N / NE / E → v29
- SE / S / SW → v30
- W / NW → v31

The consolidated eight-direction source review is v32.

### Clean-chest integration

**Active integration candidate: v36.**

v36 rebuilds the eight-direction clothing/waist stack on the v35 clean-chest body and retains the direction-specific manual placements rather than reverting to a universal overlay transform.

The body still uses core + late-visible anatomy routing so garments cannot blindly cover the head, hands/forearms or feet.

v36 is not final. Sleeve/cuff/hand seams and near/far garment routing still need per-facing polish against the approved dressed benchmark.

### Waist modularity

The clothing-sheet sash is not the final swappable waist layer because several facings include presentation-baked pouch / gourd / charm content.

Production keeps these independent:

- belt knot / scabbard cord;
- pouch;
- gourd;
- charm tag;
- utility trinket.

v36 continues to use independent belt-knot / pouch / gourd staging.

### Hair

Standalone eight-direction hair isolation remains useful, but runtime hair is blocked by the missing true hairless body master.

### Equipment and accessories

Active extraction QA remains **v24**.

v24 uses tight row/component extraction and corrects the prior gourd-NW clipping and shoulder-tie neighboring fragments.

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

Known source coverage gaps remain:

- NW katana;
- NW scabbard;
- NW belt knot / scabbard cord;
- NW shoulder tie.

They are not mirrored automatically because facing-sensitive routing and silhouette matter.

## Anchor / layering rule

> No garment or equipment layer may hide body regions unless that occlusion is directionally intentional and supported by the approved dressed Kairo benchmark.

Open garment regions remain transparent. Pouch, gourd, charm and belt/scabbard-cord content remain independently swappable.

## Current gate

No character checklist item is complete.

Package 07 remains a **source-stage art/engineering candidate** until:

1. v35 clean-chest body receives final source-art approval;
2. a true hairless body master exists;
3. all eight v36 clothing composites receive seam / occlusion polish;
4. waist cloth and accessories are fully separated;
5. equipment is manually registered per facing;
6. the four missing NW equipment directions are authored;
7. the complete source composite passes review before any 48×64 reduction.

See `KAIRO_PACKAGE_07_V35_V36_QA.md` for the current body/integration gate.
