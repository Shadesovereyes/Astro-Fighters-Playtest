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

- Version 9 (2026-10-15):
  - Hex step 20 (was 34), drawn at an integer 2x when the panel fits, so adjacent fighters stand close enough for a
    jab (reach +23 px past the pivot) to visibly land.
  - Fighters turn to face their main target (else last target, else nearest foe) after every beat, throw and recap.
  - Appearance section (`web/af-creator-v3.js`): skin tone, hair style, hair colour, eye colour, outfit. All are palette
    swaps or layer picks over the approved sheets; nothing is redrawn. Tones 1 and 2 are approved, tones 3 and 4 are
    candidates awaiting approval. Hair and eye colours share one ramp rule (`colorRamp` in `af-sprites-v3.js`): the
    picked colour is the base, highlights shift lighter and warmer, the iris shadow darker and cooler. The look is kept
    in the browser's localStorage (`af.look.v1`).
  - "Record the fight (video + GIF)" on the result screen replays the recap and offers a WebM (or MP4) at 2x and a
    10 fps GIF at 1x for download.

- Environment props (2026-10-15, `web/af-props-v3.js`, candidate art awaiting approval): every engine terrain kind is
  drawn as pixel art instead of a glyph, with 2 or 3 variants picked per cell (pine, oak and autumn trees about 2 to 2.4 fighters tall, with headroom above the top row; boulder,
  standing stone and sandstone rocks; shrub, berry and flowering bushes; stone and plank rubble; pond; Earth Wall;
  felled log and stump; animated smoke; spike pit; caltrops), plus grass, pebbles, flowers and mushrooms on open cells.
  Each prop is a deterministic pixel spec rendered at the rig's density; nothing is generated or resampled. Standing
  props are depth sorted with the fighters and turn see-through while a fighter is behind one. The recap video and GIF
  include them. Gameplay is unchanged: the hex outlines still mark what blocks movement and sight.

- Downed state (2026-10-15, candidate awaiting approval): a defeated fighter no longer fades out. It lies in the new
  `downed` state (the approved prone pose with the eyes closed, `production/source/characters/anim/male/downed.json`)
  where it fell, for the rest of the fight and in the recap. Beasts and summons drawn as glyphs still fade.

- Pinned battle layout (2026-10-15): on screens wider than 1100 px the health bars and the arena map stay on screen
  while the controls column on the right scrolls; the arena is fitted to the height left under the health bars.

- Seamless arena ground (2026-10-15): one painted plateau (grass, worn dirt, an earth cliff on the south edge) under
  the SVG hex grid. While planning, the grid shows faintly over it with the move, target and area highlights; while a
  round or the recap plays the grid fades out. The recap video and GIF draw the ground with no grid.

- Water (2026-10-15): lakes of at least 7 connected tiles (a centre and its ring, grown a little; 2 lakes on large
  maps), painted into the ground so the water fills whole tiles and runs between them. Characters can walk on water
  but pay 10 chakra each round they end on it (`BAL.waterChakraPerRound`); with too little chakra they drown for 12% of
  max HP a round (`BAL.waterDrownPercent`) and show the drowning loop (the approved guard-break arms-up frames, sunk to
  the waist and cut at the waterline, with a foam ring). Animals (bear, tiger, crab, bat), summons and the caravan
  cannot enter water. Charge Chakra cannot be used while standing in water.

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
