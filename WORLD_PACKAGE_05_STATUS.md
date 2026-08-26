# Astro Fighters — World Package 05 Status

**Branch:** `chatgpt/facade-package-05`  
**Pipeline:** reference target → core-style gate → modular derivation → Phaser integration → integrated rubric review

## Package targets

Package 05 moves from isolated material/threshold tests into the first complete Imperial City facade family.

Reference targets:
- timber-and-plaster wall
- shop-front facade
- two-story residence
- alley/corner building
- common street dressing and props

## Reference gate

The source anchors were created before runtime extraction and are judged against the locked Master Art Direction Prompt, approved Kairo benchmark, Imperial City reference, and master palette.

The reference family is accepted **for continued derivation** because it establishes:
- irregular aged timber construction with visible joinery
- plaster infill with wear/staining rather than flat blank panels
- substantial stone foundations
- layered eaves and roof silhouette
- window/door depth, trim, signage, lanterns and daily-life dressing
- warm analog/Japandi-industrial material language
- architecture that reads as authored Imperial City construction rather than generic boxes
- density and prop storytelling closer to the approved character-art craftsmanship level

This is not a checklist completion claim.

## Runtime derivation

Five modular families are staged at 128×160 with transparent hard-alpha canvases:
- wall bays
- door/window bays
- roof/eave pieces
- awning/sign pieces
- street props

Runtime candidates are palette-quantized to the locked world palette and use nearest-neighbor-only scaling. They are deliberately separate from the source anchors.

## Phaser integration

`docs/play-v4-facade-package05.html` loads the actual Phaser runtime and stacks Packages 01, 03, 04 and 05.

Controls:
- **F2** — toggle Package 05 facade
- **F3** — cycle facade variant
- **F4/F5** — Package 04 threshold/foundation controls
- **F6/F7** — Package 03 stone controls
- **F8** — Package 01 paper-doll staging toggle

Package 05 assembles wall + door/window + roof/eave + awning/sign + props as independent sprites. This is a staging composition check; final collision, cutaway, facade occlusion and interaction authoring remain pending.

## Checklist state

**No checklist item is marked complete.**

The package still requires:
1. in-engine visual review at representative gameplay scale;
2. collision and doorway/threshold interaction authoring;
3. stronger direction-aware occlusion/cutaway behavior;
4. final lantern/sign dressing and lived-in prop density;
5. production character art rather than the Package 01 engineering candidate;
6. full integrated rubric review with no automatic failures and the required completion score.

## Next autonomous dependencies

1. Validate Package 05 facade assembly in Phaser.
2. Re-author any module family that falls below the source reference at runtime scale.
3. Add lantern mount + hanging lantern + sign mount + vertical signboard as independent dressing modules.
4. Add roof edge/end-cap and wall corner/transition pieces.
5. Build the first representative Imperial City street slice from Packages 03–05.
6. Continue Kairo anchor-locked source-layer cleanup in parallel.
