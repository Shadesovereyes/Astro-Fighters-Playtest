# Astro Fighters Repository Instructions

For all work in this repository, treat root `AGENTS.md` as mandatory repository-wide instructions.

The current game is an **open-world, real-time action-combat RPG** using the **Phaser/browser runtime under `/docs`**.

Before changing runtime, art, manifests, checklists, or review status, read:

- `AGENTS.md`
- `README.md`
- `ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md`
- `PHASER_WORLD_REFACTOR_V0.md`
- `IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md`
- `Astro Fighters — Art Preview Review Rubric.md`

## Non-negotiable runtime/art rules

- Production gameplay scenes must be assembled by Phaser from separate runtime assets/layers; do not use a single baked full-screen district illustration as the playable world.
- A photo collage, PIL/Python composite, generated montage, source assembly, or presentation board is reference/QA material only and must never be presented as an in-engine gameplay preview.
- Integrated art review is valid only from the running Phaser canvas.
- The 32×32 grid is hidden structural logic. Do not draw it persistently or expose it through repeated world-art rhythm.
- Ordinary exploration uses continuous real-time movement, not fixed integer tile stepping.
- Collision must be authored independently of appearance imagery.
- Maintain true depth sorting/occlusion so actors pass in front of and behind appropriate world objects.
- Retain crisp pixel rendering (`pixelArt: true`, `antialias: false`, `roundPixels: true`) unless the user explicitly changes the standard.
- Mixed-resolution collage appearance, baked-background substitution, visible grid rhythm, broken depth/occlusion, non-Phaser review imagery, and fixed grid-step exploration are production blockers.
- Do not mark checklist items production-complete until representative Phaser-integrated gameplay passes the locked rubric at 42+ with no automatic failure.

If existing code conflicts with these rules, treat the conflicting implementation as legacy prototype debt and follow `PHASER_WORLD_REFACTOR_V0.md` rather than copying the shortcut forward.
