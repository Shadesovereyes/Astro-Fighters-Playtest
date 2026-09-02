# Astro Fighters Player Paper-Doll — Production Contract

**Status:** active source-development contract  
**Scope:** generic playable male/female paper-doll base models and modular equipment/clothing families

This contract follows the locked Master Art Direction, Pixel-Art Source Standard, Modular Source Layer Integrity Rules, and Key-Color Isolation & Transparency QA.

## Canonical facing

Runtime directions are `N, NE, E, SE, S, SW, W, NW`, with `S = front` and `N = back`. Legacy sheet slot order may differ and must be remapped in metadata.

## Shared production lattice

- source canvas: **480×640**
- body center: **x = 240**
- foot-contact line: **y = 560**
- established runtime target: **48×64** unless a later locked runtime contract explicitly replaces it
- every body, hair, clothing, equipment, hand, footwear, and accessory source layer shares the same anatomical lattice
- legacy small sprites may be visual/runtime references, but enlarging them does not create source masters

## Base underlayers

**Male:** body/skin + hair/face + base shorts only.

**Female:** body/skin + hair/face + base shorts + sports bra only.

Chest wraps, wrist/leg wraps, footwear, inner/outer clothing, trousers, sash/belts, weapons, scabbards, charms, pouches, and other equipment remain removable layers.

## Current legacy cardinal references

The current male and female `256×64` sheets are **legacy cardinal pixel references**, not complete source packages.

Inspection establishes:

- each sheet contains **eight 32×64 slots**;
- only slots `0`, `2`, `4`, and `6` contain art;
- slots `1`, `3`, `5`, and `7` are empty;
- populated visual mapping is:
  - slot `0` → `N`
  - slot `2` → `S`
  - slot `4` → `E`
  - slot `6` → `W`
- the four diagonal directions are missing and must be independently authored.

This legacy slot order is not canonical. Manifests must remap it explicitly. The 32×64 cardinals are useful pixel-art authorities for proportions, base garments, hair silhouette, and cardinal identity, but they are **not** valid 480×640 source masters.

## Pixel-art requirement

Anything intended for game use must satisfy `ASTRO_FIGHTERS_PIXEL_ART_SOURCE_STANDARD.md`: hard intentional pixels, no anti-aliasing, no mixles, ordinary sprite alpha `0/255`, nearest-neighbor integer previews only, and master-palette discipline. Polished illustration is allowed only as reference material.

## Key-color isolation QA

Every transparent paper-doll layer must follow `ASTRO_FIGHTERS_KEY_COLOR_ISOLATION_QA.md`.

Reserved QA background:

- **`#FF00FF` / RGB 255,0,255**
- QA/staging only
- forbidden from production art

Required review surfaces:

1. transparent PNG;
2. exact production pixels over `#FF00FF`;
3. checkerboard;
4. binary alpha mask;
5. nearest-neighbor pixel zoom;
6. occluder-toggle view for modular overlaps.

The key-color pass must expose accidental holes inside solid body/hair/clothing/equipment, matte contamination, fringe/mixle pixels, bad cutouts, and hidden-underlayer clipping. Final assets contain transparency, never the key color.

## Eight-direction base-development order

Preserve and QA the four existing cardinal references first. Author missing diagonals as distinct poses, one at a time:

`SE → NE → NW → SW`

Each diagonal must genuinely rotate head/face, hair volume, shoulders, torso, hips, arms/hands, legs/feet, base shorts, and the female sports bra. A diagonal is not a cardinal body with shifted facial pixels.

## Base-model approval gate

A direction receives `SOURCE PASS` only when canonical facing, base-underlayer contents, shared lattice, foot anchor, anatomy, hair/face direction, key-color QA, alpha-mask QA, no-hole/no-matte review, no-mixle review, palette/pixel quality, and independent clothing-underlayer usability all pass.

Do not build clothing families on an unstable base direction.

## Generic modular layer families

1. shadow
2. hair_back
3. equipment_back
4. outerwear_back
5. sash_back
6. body_core
7. pants/lower garment
8. inner_top
9. outerwear_far_sleeve
10. body_far_hand
11. outerwear_front_far
12. outerwear_near_sleeve
13. body_near_hand
14. outerwear_front_near
15. footwear
16. sash_front
17. sash_ties
18. eyes/face detail when modularized
19. hair_front
20. equipment_front
21. accessory_front

Whole-garment visibility slices are invalid. Hidden components continue beneath occluders according to `ASTRO_FIGHTERS_MODULAR_SOURCE_LAYER_INTEGRITY_RULES.md`.

## Immediate production state

- male cardinal base references: `N`, `S`, `E`, `W` exist;
- female cardinal base references: `N`, `S`, `E`, `W` exist;
- diagonal base directions are missing;
- 480×640 eight-direction male/female source masters are not yet approved;
- legacy 32×64 art remains reference/runtime evidence only;
- first production task: preserve and QA the cardinals, then author **SE** for male and female under this contract before the other diagonals.

## Locked summary

> **BASE MODELS ARE PIXEL ART GAME ASSETS, NOT PAINTED REFERENCES.**  
> **MALE = BODY/HAIR/FACE + SHORTS. FEMALE = BODY/HAIR/FACE + SHORTS + SPORTS BRA.**  
> **LEGACY CARDINALS GUIDE THE BUILD; THEY ARE NOT 480×640 SOURCE MASTERS.**  
> **USE `#FF00FF` ONLY AS QA STAGING TO EXPOSE HOLES, MATTE, AND BAD ALPHA.**  
> **AUTHOR THE FOUR DIAGONALS AS REAL DIRECTIONS AND APPROVE THEM ONE AT A TIME.**
