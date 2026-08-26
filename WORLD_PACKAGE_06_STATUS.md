# Astro Fighters — World Package 06 Status

**Branch:** `chatgpt/dressing-street-slice-package-06`  
**Pipeline:** reference target → core-style gate → modular derivation → Phaser integration → integrated rubric review

## Purpose

Package 06 adds the architectural dressing and lived-in street layer needed before the first representative Imperial City slice can be judged.

## Reference gate — PASS for continued derivation

Accepted art-source regions cover:
- hanging lantern construction and material response
- vertical/horizontal signage and noren
- market-stall / daily-life cargo language
- barrels, baskets, jars and utility storage
- plants, bonsai, bamboo, stone lanterns and shrine markers
- a dense street/facade benchmark

The generated board's own dashboard scores, checkmarks and completion labels are **explicitly ignored**. They are not review evidence. Only the cropped art regions are treated as source references.

The references advance the locked style because they show material-specific paper, wood, cloth, ceramic, foliage and stone behavior; warm analog lighting; Edo daily-life construction; irregular lived-in density; and authored silhouettes at a craftsmanship level much closer to the Kairo quality anchor.

Full-resolution source anchors and isolated component studies remain production-source artifacts. The public playtest branch carries compact review previews plus the derived runtime atlas. The wide street benchmark is a composition/quality anchor only and must never be baked into gameplay as a background.

## Modular derivation

Four transparent modular families were derived from the isolated component studies:
- 8 lantern variants
- 8 sign / noren variants
- 9 utility prop variants
- 9 plant / decorative variants

All derivatives:
- use 128×160 hard-alpha cells
- use nearest-neighbor-only scaling
- are never enlarged from the source crop
- are quantized to the locked world palette
- are packed into `package06-dressing-atlas-1152x640.png`

Palette validation:
- off-palette opaque colors: **0**
- non-hard alpha values: **0**

## Phaser integration

`docs/play-v4-street-slice-package06.html` stacks Packages 01, 03, 04, 05 and 06 in the actual Phaser runtime.

Package 06 controls:
- **F9** — toggle architectural dressing
- **F10** — cycle three authored dressing layouts

Earlier package controls remain active:
- F2/F3 facade
- F4/F5 threshold/foundation
- F6/F7 stone material
- F8 paper-doll staging

No gameplay grid lines are rendered.

## Checklist state

**No checklist item is complete yet.**

This package reaches the point where a representative street slice can finally be evaluated, but completion still requires:
1. live Phaser visual review of the combined Packages 03–06 scene;
2. final doorway/collision/interaction authoring;
3. occlusion/cutaway refinement for tall facade and dressing assets;
4. production-quality character paper-doll art rather than the Package 01 engineering candidate;
5. rubric review of the integrated gameplay screenshot with no automatic fails and the locked completion threshold.

## Next autonomous package

1. Validate the combined street slice and replace any low-quality runtime derivative.
2. Add roof end-caps, wall corners and facade-transition modules where the street exposes hard seams.
3. Add interaction/collision metadata for doorways, market stalls and tall props.
4. Begin the first production character paper-doll source package from true anchor-locked Kairo layers.
5. Only after the representative gameplay scene clears the rubric may related checklist items be struck.
