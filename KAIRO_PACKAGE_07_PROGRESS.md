# Kairo — Package 07 Progress Update

## Active source gates

### Shared lattice

The source canvas remains **480×640**, body center `x = 240`, foot-contact `y = 560`.

Character layers use anatomical registration rather than generic object centering/bottom justification.

### Base body

The production body must not contain the chest cross-bandage / X-wrap.

Procedural chest cleanup experiments are rejected as production source art because they damaged source-quality torso rendering. A true source-quality N / NE / E / W clean-chest master remains required.

Wrist and ankle/lower-leg wraps remain intentional for the current Kairo design.

A true hairless body master is also still required before interchangeable hair can be source-complete.

### Clothing

Active clean isolation: **v13**.

- 40 transparent garment candidates across inner top / haori / trousers / footwear / sash reference;
- no neighboring-item pixels;
- no direction labels / panel borders;
- no source-sheet background;
- no presentation shadow contamination.

Registration review identified two source-direction corrections:

- benchmark `NW` ← clothing source `SW`;
- benchmark `SW` ← clothing source `NW`.

The open-front haori also carried a dark presentation/mannequin fill inside the opening. That fill is removed for paper-doll staging so the body/inner layer remains visible.

Current source-composite staging: **v20**.

v20 uses full cleaned haori sleeve volume around the body, keeps head/hands/late anatomy available as front regions, and suppresses the front inner-top overlay on rear facings (`SE`, `S`, `SW`).

v20 is not final. Scale, cuff/hand seams and near/far routing still require hand correction per direction against the approved dressed benchmark.

### Waist modularity

The clothing-sheet sash is no longer treated as the final swappable waist layer because it contains presentation-baked pouch / gourd / charm content in several facings.

The production waist stack keeps the following independent:

- belt knot / scabbard cord;
- pouch;
- gourd;
- charm tag;
- utility trinket.

A v25 source-stage composite removes the baked sash and demonstrates those items as independent lattice-registered modules.

### Hair

Standalone eight-direction hair isolation remains useful, but runtime hair is blocked by the missing true hairless body master.

### Equipment and accessories

Active extraction QA: **v24**.

v24 replaces overlapping rectangular crops with tight row/component extraction and corrects the last visible gourd-NW clipping and shoulder-tie neighboring fragments from v23.

Clean source candidates now exist for all source-provided directions of:

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

Known source coverage gaps remain intentionally unresolved:

- NW katana;
- NW scabbard;
- NW belt knot / scabbard cord;
- NW shoulder tie.

These are not mirrored automatically because facing-sensitive routing and silhouette matter.

## Anchor / layering rule

> No garment or equipment layer may hide body regions unless that occlusion is directionally intentional and supported by the approved dressed Kairo benchmark.

Open garment regions remain transparent. Pouch, gourd, charm and belt/scabbard-cord content remain independently swappable.

## Current gate

No character checklist item is complete.

Package 07 remains a **source-stage engineering/art candidate** until:

1. a true clean-chest body master exists;
2. a true hairless body master exists;
3. all eight v20 clothing composites receive manual seam / occlusion correction;
4. waist cloth and accessories are fully separated;
5. equipment is registered to the shared anatomical lattice;
6. the four missing NW equipment directions are authored;
7. the complete source composite passes review before any 48×64 reduction.

See `KAIRO_PACKAGE_07_V20_V24_QA.md` for the latest QA history.