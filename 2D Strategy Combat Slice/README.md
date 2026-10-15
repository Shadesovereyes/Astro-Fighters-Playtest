# 2D Strategy Combat Slice

Everything needed to run the hex turn-based combat testbed (engine V3.5) that is published as the Artifact
https://claude.ai/artifact/UpATMo9mKyEJtQ5tJuYp7N.

This is the legacy turn-based strategy testbed, kept for combat design and math. It is a canvas-over-SVG replay in a
plain browser page, **not** the Phaser runtime and not Phaser-integrated gameplay (see the repository `AGENTS.md`).

## Run it

- Single file, no server: open `web/astro-fighters-artifact.html` or `web/astro-fighters-standalone.html` in a browser.
  Both inline every module and the male character rig.
- Split modules, for debugging: serve the folder (`cd web && python3 -m http.server`) and open `index.html`.

## What this version adds over the previous Artifact

- The engine resolves each round first and records events (move, act, hit, evade, parry, knock, grapple, release).
  `af-sprites-v3.js` replays those events with the approved male sprite states.
- Clinch pairs the two fighters side by side; clinch strikes (Uppercut, Knee Strikes, Elbow Strike, Body Shot) play the
  paired clips.
- Hip Toss follows the sheet ("Prone 1rd; breaks the hold") and Christopher's tile ruling: the victim lands 1 tile
  behind the holder, stays down 1.5 s, kips up, then turns to face the opponent. Power and stamina stay at the engine's
  15/22.
- Rolling Throw follows the sheet ("Throw target 3 tiles away from user; Ends Grapple"): the victim lands 3 tiles away on
  the holder's far side.

To see the moves: train Judo or Muay Thai, Clinch an adjacent foe, then queue Hip Toss, Rolling Throw, Knee Strikes,
Elbow Strike, Uppercut or Body Shot.

## Layout

- `web/` runtime modules, entry pages, smoke tests, `build-standalone.js`, and `characters/` (the imported rig: 42 male
  states, byte copies of the approved sheets from this repository's `docs/assets/characters/male`).
- `tools/import-playtest-rig.mjs` re-imports the rig from a git ref of this repository, e.g.
  `node tools/import-playtest-rig.mjs male origin/claude/busy-dirac-ejzeh7`.
- `tools/report-ability-animations.mjs` regenerates `docs/ABILITY_ANIMATION_COVERAGE.md` (which abilities have sprite
  clips and which still need art).

## Rebuild and test

```bash
cd web
node af-core.smoke.js
node af-v3.4.smoke.js
node af-sprites.smoke.js
node build-standalone.js --rig --artifact   # rewrites both single-file pages
```

Ability data comes from the AstroFighters_Abilities sheet, which stays the source of truth.
