# Astro Fighters Repository Instructions

Treat root `AGENTS.md` as the mandatory repository-wide instruction authority.

Before changing runtime, art, manifests, checklists, or review state, read:

- `README.md`
- `AGENTS.md`
- `ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md`
- `PHASER_WORLD_REFACTOR_V0.md`
- `IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md`
- `Astro Fighters — Art Preview Review Rubric.md`
- `docs/data/art-review-rubric.json`
- `production/asset-manifest.json`

Stable invariants:

- Astro Fighters is an **open-world, real-time action-combat RPG** using Phaser/browser under `/docs`.
- The private Unity project is legacy turn-based combat-reference material, not the current runtime/roadmap.
- Production world scenes are assembled in Phaser from separate runtime assets/layers; no baked full-screen district image may substitute for playable world construction.
- Ordinary exploration uses continuous real-time movement; the 32×32 grid is hidden structural logic, not a permanent visual overlay.
- Integrated art review is valid only from the running Phaser canvas.
- Collages, presentation boards, source assemblies, PIL/Python composites, and mock renderers are reference/QA only.
- Collision is independent from appearance imagery and actors must pass in front of/behind appropriate world objects.
- Keep crisp pixel rendering (`pixelArt: true`, `antialias: false`, `roundPixels: true`) unless explicitly changed.
- Follow the generation-vocabulary restrictions in `AGENTS.md` and the Master Art Direction; do not reintroduce generic cyberpunk/steampunk/wet-reflective drift.
- Checklist completion requires 42+, zero automatic failures, and all critical minimums passing.
- Do not duplicate completion state across planning/status documents; Git history is the iteration archive.
