# Kairo — Package 07 v20 / v24 QA Update

## Scope

This update records the latest source-stage corrections after the earlier flat-overlay and contaminated-equipment passes were rejected.

No 48×64 runtime derivative is approved by this document.

## Clothing source isolation

The active clean garment source family remains the 40-candidate v13 isolation:

- inner top × 8 directions
- haori × 8 directions
- trousers × 8 directions
- footwear × 8 directions
- sash reference × 8 directions

The v13 isolates are retained because they remove neighboring source-sheet pixels, labels, panel/background contamination and presentation shadows.

## Direction remap found during registration

The clothing source sheet's left-side diagonal labels do not line up with the approved dressed turnaround. Registration now treats:

- benchmark `NW` ← clothing source `SW`
- benchmark `SW` ← clothing source `NW`

The other six directions remain same-name mappings.

## Open-haori correction

The standalone front/three-quarter haori reference contains a dark presentation/mannequin fill inside the garment opening. That fill is not valid as a reusable paper-doll layer because it hides the inner top/body.

The active source correction clears only the central low-chroma dark presentation fill in open-front source directions while retaining the colored garment borders, trim and sleeve art.

## v20 direction-aware clothing candidate

The current v20 source-composite experiment uses the clean/open haori and a direction-aware body routing pass.

Current staging order:

`body_core → trousers → inner_top (front/side facings only) → open haori → footwear → head/hands/late body regions → waist layer`

Rear facings (`SE`, `S`, `SW`) suppress the inner-top overlay because the approved dressed benchmark does not expose the front torso there.

v20 materially improves the earlier failure where a whole opaque garment covered Kairo's body. It is still not production-complete: scale, cuff/hand seams and final near/far sleeve decomposition still require direction-by-direction hand correction against the dressed benchmark.

## Sash source decision

The clothing-sheet sash reference is no longer accepted as a final swappable production layer because it contains presentation-baked accessory content (pouch, gourd, charm/chain elements depending on direction).

Production modularity requires those items to remain independent.

The sash reference therefore remains a **visual/placement reference**, while the production waist stack is being rebuilt from independent modules:

- belt knot / scabbard cord
- pouch
- gourd
- charm tag
- utility trinket

## Equipment isolation — v24 active

The active equipment extraction is v24.

The dense lower rows are extracted by row-wide connected components and object-center assignment instead of overlapping rectangles. The remaining gourd-NW clipping and shoulder-tie neighboring fragments from v23 were specifically corrected in v24.

Clean source families now exist for all source-provided directions of:

- katana
- scabbard
- belt knot / scabbard cord
- hanging charm tag
- necklace
- pouch
- gourd
- shoulder tie
- wrist wraps
- utility trinket

The four genuine source gaps remain:

- NW katana
- NW scabbard
- NW belt knot / scabbard cord
- NW shoulder tie

These are intentionally not mirrored automatically.

## v25 modular waist staging

A source-stage v25 composite test removes the baked clothing-sheet sash entirely and stages independent belt-knot / pouch / gourd / utility components on the shared 480×640 body lattice.

This is an anchor/occlusion test only, but it proves the waist accessories can be kept swappable instead of permanently fused into one sash image.

## Blocking source gates

Package 07 remains blocked from 48×64 derivation until:

1. a true source-quality clean-chest N / NE / E / W body master exists;
2. a true hairless body master exists;
3. v20 clothing scale and sleeve/cuff/hand seams are manually corrected in all eight directions;
4. the waist treatment is fully decomposed into cloth + independent accessories;
5. equipment is registered to the shared anatomical lattice;
6. the four missing NW equipment directions are authored;
7. the complete dressed source composite passes visual review against the approved Kairo benchmark.

**No character checklist item is complete yet.**