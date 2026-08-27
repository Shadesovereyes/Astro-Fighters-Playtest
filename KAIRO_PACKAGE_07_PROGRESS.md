# Kairo — Package 07 Progress Update

## Active source gates

### Shared lattice

The source canvas remains **480×640**, body center `x = 240`, foot-contact `y = 560`.

Character layers use anatomical registration rather than generic object centering/bottom justification.

### Base body

The chest cross-bandage / X-wrap is forbidden on the production body.

**Active clean-chest candidate: v35.**

v35 removes the wrap from N / NE / E / W while preserving the approved source art outside the torso correction region. It supersedes the earlier broad procedural cleanup attempts.

The clean-chest candidate is good enough for continued source integration, but it is **not yet marked production-approved**. Final full-resolution torso review is still required.

Wrist and ankle/lower-leg wraps remain intentional.

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

Direction-specific manual placement has been established across all eight facings:
- N / NE / E → v29
- SE / S / SW → v30
- W / NW → v31

The consolidated eight-direction source review is v32.

### Clean-chest integration and body/garment routing

v36 rebuilt the eight-direction clothing/waist stack on the v35 clean-chest body.

**Active body/garment routing candidate: v37.**

The earlier late-body mask was still too broad and exposed too much forearm over the haori sleeve. v37 narrows late body routing to:

- head / hair;
- wrist / hand zones only.

Upper forearms remain behind the haori sleeve unless a facing-specific benchmark requires otherwise. This directly addresses the incorrect "clothes on top / body on top" behavior found in earlier registration passes.

v37 is not final. Sleeve/cuff/hand seams and near/far garment routing still require per-facing polish against the approved dressed benchmark.

### Waist modularity

The clothing-sheet sash is not the final swappable waist layer because several facings include presentation-baked pouch / gourd / charm content.

Production keeps these independent:

- belt knot / scabbard cord;
- pouch;
- gourd;
- charm tag;
- utility trinket.

Current source staging continues to use independent belt-knot / pouch / gourd pieces.

### Hair / hairless body

Standalone eight-direction hair source art is available.

**v39 is the active hairless-body source candidate for continued engineering review.** It removes the existing hair and reconstructs a direction-specific scalp on the same 480×640 body lattice.

**v40 validates hair re-layering** by registering the approved directional hair source back over the v39 candidate. The eight directions recompose successfully enough to prove the paper-doll separation path.

Neither v39 nor v40 is production approval. The scalp silhouette and source-level shading still require manual art polish before the hairless body master can be locked.

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
2. the v39 hairless-body scalp is manually polished and approved;
3. all eight v37 clothing composites receive seam / occlusion polish;
4. waist cloth and accessories are fully separated;
5. equipment is manually registered per facing;
6. the four missing NW equipment directions are authored;
7. the complete source composite passes review before any 48×64 reduction.

See `KAIRO_PACKAGE_07_V35_V36_QA.md` and `KAIRO_PACKAGE_07_V37_V40_QA.md` for the current source QA gates.
