# Kairo — Package 07 Progress Update

## Active source gates

### Base body

- Shared source lattice remains **480×640**, body center `x = 240`, foot-contact `y = 560`.
- The chest cross-bandage / X-wrap is **not allowed** in the production base body.
- The earlier procedural clean-chest attempts are rejected as source-quality art; the previous statement that the N / NE / E / W cleanup was complete has been retracted.
- Wrist and lower-leg wraps remain intentional for the current Kairo visual target.
- A true clean-chest body master and a true hairless body master are still blocking dependencies.
- Runtime reduction remains blocked.

### Clothing

The contamination lesson from the earlier passes is retained: open garments must expose the body/inner layer and may not carry opaque presentation-sheet background or mannequin fill.

The current 40 eight-direction clothing source candidates remain useful for isolation/reference work, but the whole-garment registration model is rejected as the final paper-doll structure.

Review showed that side and 3/4 facings require garments to be split by depth rather than drawn as broad overlays.

A new source-stage engineering contract is now committed:

- `KAIRO_PACKAGE_07_LAYERING_SPEC.md`
- `docs/assets/metadata/character/package07-kairo-layer-order-v1.json`

The production stack now requires direction-aware pieces including:

- haori back mass;
- far sleeve / far front panel;
- near sleeve / near front panel;
- sash back;
- sash front;
- sash ties;
- separate body far/near hands so hands remain visible after sleeve cuffs;
- equipment back/front overrides when gear crosses the body.

Locked rule:

> No garment layer may hide body regions unless that occlusion is directionally intentional and supported by the approved dressed benchmark.

### Hair

- Standalone eight-direction hair isolation remains a useful source/reference family.
- A true hairless body master is still required before interchangeable hair is source-complete.

### Equipment and accessories

The isolated equipment family still covers katana, scabbard, cord, charm tag, necklace, pouch, gourd, shoulder tie, wrist wraps and utility trinkets.

Known source coverage gaps remain intentionally unresolved:

- katana in hand — NW missing
- scabbard at waist — NW missing
- scabbard cord / belt knot — NW missing
- shoulder tie / cloth strip — NW missing

These directions will be authored rather than mirrored automatically because equipment routing is facing-dependent.

## Anchor policy

World props use host-specific placement anchors. Character paper-doll layers do not.

Every Kairo body, clothing, hair, eyes, equipment and accessory layer inherits the same anatomical `480×640` body lattice. Feet, hands, shoulders and head anchors must remain stable across all directions and future animation frames.

## Current gate

No character checklist item is complete.

Package 07 remains a **source-stage engineering/art candidate** until:

1. the clean-chest and hairless body masters are source-quality;
2. the haori/sash are re-authored into the new direction-aware sublayers;
3. all eight dressed source composites match the approved benchmark without incorrect coverage;
4. equipment is registered to the same lattice;
5. the four missing NW equipment directions are authored;
6. the complete source stack passes review.

Only then may the first **48×64 nearest-neighbor runtime paper-doll set** be derived and integrated into Phaser.