# Astro Fighters — Integrated Art Review Pass 01

**Date:** 2026-08-25  
**Branch:** `chatgpt/art-integration-pass-1`  
**Review surface:** `docs/art-integration-pass-1.html`  
**Result:** **REJECTED — automatic-failure conditions present**

This pass was previously scored 38/50. That assessment was too generous and did not correctly apply the repository's mandatory automatic-failure rules. The numeric acceptance score is therefore withdrawn; automatic failure takes precedence over category totals.

## Automatic-failure findings

The integrated image fails the locked rubric in multiple ways:

- **World art is visibly below the approved character-reference quality.** The scenery uses much simpler clustering, shading, texture density, and material rendering than the approved 256×64 character sheets.
- **Environment relies too heavily on flat geometric construction.** The storefront, props, tree and street read as decorated primitives rather than production-level authored pixel art.
- **Architecture is too box-like and generic.** The facade lacks the structural silhouette, eaves, hardware, conduits, layered construction, retaining infrastructure and district-specific detail required by the Imperial City direction.
- **Character art is below the approved reference standard.** Although dressed and direction-aware, the test fighter is substantially cruder than the approved character sheets in anatomy, silhouette, hair, clothing folds, value grouping and pixel craftsmanship.
- **Character/world homogeneity is not achieved at the locked quality bar.** Matching palette families is not enough; craftsmanship, cluster language, shading and density must also match.
- **Astro Fighters world identity is underdeveloped.** The scene does not yet communicate the monumental ancient-industrial Imperial City, Edo daily life, analog infrastructure and lived-in density seen in the locked reference direction.

Because any one automatic failure rejects a preview, this pass is **not an internal test candidate and must not be presented as a benchmark for production art**.

## What remains useful

The pass is retained only as a technical integration spike for:

- hidden 32×32 logical movement with no visible grid;
- eight-direction routing;
- layered runtime assets rather than a baked background;
- collision/depth-order experiments;
- foreground occlusion/fade behavior.

These mechanics must be moved back into the established **Phaser runtime**. The custom Canvas test is not the target architecture.

## Rebuild requirements

1. Re-establish the approved male/female character sheets and Imperial City reference as the visual bar before authoring new runtime assets.
2. Replace the current fighter with a production-quality 48×64 side-on pixel-art stack whose anatomy, hair, clothing, equipment and pixel language match the approved references.
3. Replace the current box-like storefront with authored Imperial City architecture: layered timber/stone construction, eaves, roof massing, hardware, conduits, signage, weathering and meaningful silhouette.
4. Raise material rendering for stone, timber, plaster, cloth, rope, metal, foliage and grime to character-art craftsmanship.
5. Increase lived-in density and monumental/industrial context without exposing the hidden grid.
6. Integrate the rebuilt assets directly into Phaser.
7. Re-run the mandatory rubric only after the representative gameplay image no longer triggers any automatic failure.

## Checklist state

**No world or character checklist entry is complete or struck by this pass.**
