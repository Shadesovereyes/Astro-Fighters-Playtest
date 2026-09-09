# Kairo — Package 07 Runtime Benchmark

## Purpose

This file records the first deliberately narrow runtime-art benchmark for Package 07.

The benchmark is **not** a paper-doll completion claim. It exists to provide a pixel-accurate 48×64 visual target that the modular body / clothing / hair / equipment stack must reproduce.

## Source authority

The eight directional frames are derived from the approved fully dressed Kairo turnaround.

Production rules applied:

- 48×64 runtime frame
- eight directions: N / NE / E / SE / S / SW / W / NW
- nearest-neighbor reduction
- hard alpha only
- locked Astro Fighters material palette
- material-specific palette ramps for skin, hair, haori, cream cloth, trousers, sash / wood accents, and metal
- detached-pixel cleanup after reduction
- shared anchor `[24, 60]`
- shared foot-contact position `[24, 60]`
- direction-sensitive contact shadow remains a separate layer

## Narrow-scope output policy

Package 07 art review no longer uses large dashboard / infographic images as the primary production output.

Production images should be limited to:

- isolated source assets
- isolated runtime assets
- compact direction strips when comparison is necessary
- actual Phaser gameplay screenshots for integrated review

Progress text, scores, explanations, and checklist state belong in Markdown / JSON, not baked into generated artwork.

## Phaser staging

`docs/play-v4-kairo-benchmark-package07.html` loads the real Phaser runtime and the Package 03–06 world staging, then replaces the detected player with the Kairo benchmark when available.

Controls:

- **F11** — toggle Kairo benchmark
- **numpad 8/9/6/3/2/1/4/7** — N / NE / E / SE / S / SW / W / NW
- earlier Package 03–06 world controls remain available

## Gate

The benchmark itself is a valid runtime comparison target, but Package 07 remains incomplete.

The modular paper-doll stack still requires:

1. source-quality clean-chest / hairless body masters;
2. final direction-aware clothing seam correction;
3. final equipment front/back registration;
4. four missing NW equipment views;
5. modular 48×64 derivation and per-pixel cleanup;
6. source-to-runtime comparison against this benchmark;
7. integrated Phaser rubric review.

No character checklist item is marked complete by this benchmark.
