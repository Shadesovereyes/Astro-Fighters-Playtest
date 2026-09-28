# Astro Fighters — Current Development Status

**Updated:** 2026-09-28  
**Authoritative branch:** `main`  
**Current milestone:** Imperial City Early Player Experience v0  
**Immediate runtime gate:** Phaser World Refactor v0 + Slice 0 Foundation Courtyard

## Current game architecture

Astro Fighters is an **open-world, real-time action-combat RPG**. The active public implementation is the **Phaser/browser runtime under `/docs`**.

The private `Shadesovereyes/Astro-Fighters` Unity project is a **legacy turn-based tactical Combat Strategy vertical slice**. It is reference material for reusable combat logic and math only. Do not redirect current development into Unity and do not port the old turn loop, action-slot scheduler, hex encounter structure, or prototype UX into the open-world RPG.

When legacy combat logic is reused, preserve design intent and useful math, then adapt it to real-time movement, hit windows, animation commitment, collision, interrupts, recovery/cooldowns, resources, player input, and AI behavior.

## Repository authority

`main` is the current repository authority unless `README.md` or this file explicitly identifies a newer active development branch.

Before development, read in this order:

1. `README.md` — repository orientation and game architecture
2. `AGENTS.md` — repository/runtime/development behavior
3. `ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md` — visual canon
4. `PHASER_WORLD_REFACTOR_V0.md` — temporary world-runtime migration gate
5. `IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md` — current route/scope/order
6. `Astro Fighters — Art Preview Review Rubric.md` — human review rules
7. `docs/data/art-review-rubric.json` — machine scoring authority
8. world and character production checklists — completion inventories
9. `production/asset-manifest.json` — current machine-readable package contract

Git history is the iteration archive. Old development branches and superseded package PRs are historical reference, not current authority.

## Active milestone

The first connected production-quality route is:

> **SOUTHERN HARBOR ARRIVAL → DOCKS / SHIPWRIGHT → MARKET / SHOPPING STREET → RESIDENTIAL / CANAL TRANSITION → ASTRO FIGHTER ACADEMY EXTERIOR → ACADEMY INTERIOR / SENSEI TUTORIAL**

The Academy tutorial retains the established progression intent:

- Sensei teaches the combat foundation;
- General/Trap ability access is introduced;
- the player receives **100 mon**;
- the player chooses **3 distinct trap types, 10 of each**;
- inventory/paper-doll/action-RPG state reflects the result.

Crab-island/cave production remains outside this milestone gate.

## Player-relative scale authority

The **64×64 player frame is the visual world-scale authority**. The approved player sheet is **512×64** (eight contiguous 64×64 directional frames). Every asset is proportioned against that player and tested beside it in Phaser; the hidden 32×32 grid is logic only. Player collision is an authored 20×8 foot box (`canonical.playerScale.collision`), not the sprite bounds.

Contracts reconciled on 2026-09-28: `production/asset-manifest.json` (schema v3, `canonical.playerScale`, `characterDependencies.baseSheets`), `tools/validate-production.mjs`, `tools/validate-source-png.mjs` (sheet / overlay / inspection modes), `tools/validate-world-data.mjs`, the runtime loader, and the authority documents no longer describe the player as 48×64 or use 480×640 source assumptions.

**Character layers integrated (2026-09-28):** `/Paperdolls` supplies male and female base bodies (two skin tones with matching arms), Gi, male Red/Blue Armor with shoulder guards, hair (male: Afro, Fade, Long; female: Afro, Long), and Brown/Purple eyes. All 23 sheets are 512×64, hard alpha, registered in `docs/js/world/characters.js`, and copied byte-identically to `docs/assets/characters/`. Frame order confirmed from the sheets: **S, SE, E, NE, N, NW, W, SW**. Measured stature S=55px. The legacy 48×64 candidate sheets were removed; player and NPCs now use the same layers and scale.

Open gaps: no female armor layers (armor is male-only for now); no idle/walk/ready animation sheets (one frame per direction, held while moving).

## Immediate technical gate

Runtime state (2026-09-28):

- `docs/index.html` is a thin shell; engine, data, natal engine, world data, runtime, and images are separate files under `/docs`;
- exploration is continuous real-time movement (112 px/s, delta-time, normalized diagonals, eight-direction facing), camera follow with deadzone on maps larger than the view;
- no visible grid overlay; collision is authored pixel-space data independent of imagery (F2 debug view);
- actors, architecture, and props are depth-sorted by foot line; authored occluders fade when the player is behind them;
- player and NPCs are composited from the approved paper-doll layers; the creator offers body, skin tone, hair, and eyes, with the Gi as starter outfit;
- Armorer Ren (Civic Ward, temporary location until Market exists) sells Red/Blue Armor for 80 mon, buys back at half, and equips; the wardrobe persists through save/load and death;
- the **scale reference scene** (`?scale`) sizes door/wall/window, stairs, counter, crates, barrel, bench, post, railing, lantern, and two bridge widths from ratios × measured stature; ratios are provisional until reviewed beside the approved player;
- **Slice 0** (`?slice0`) was re-proportioned against the player (22px plinth, 106px eave, 36×68 door opening, lattice window at 35px sill) from separate module textures in the manifest layer order, with a door interactable through the shared interaction framework;
- real-time combat, traps, dialogue, and save/load remain as before; map transitions are tested to preserve mon, inventory, and trap stock.

Remaining debt:

- Slice 0 modules are **procedural scaffold textures**, not modular source art or runtime candidates; authored runtime PNGs register through `authoredModules` in `docs/js/world/maps.js`;
- Docks, Civic Ward, Academy, and Fringe still use **baked full-frame district backdrops** (temporary, non-reviewable);
- no Phaser-canvas integrated art review has been scored; Slice 0 has not passed, so Harbor has not started.

Before Slice 0 can be called integrated, the runtime must prove:

- continuous real-time movement;
- no persistent visible grid;
- multiple separate environment textures/layers loaded by Phaser;
- collision authored independently from appearance imagery;
- live foreground/background occlusion;
- eight-direction player facing/animation;
- crisp pixel rendering;
- an integrated review captured from the actual Phaser canvas.

A collage, presentation board, source assembly, contact sheet, or mock renderer is never an integrated gameplay preview.

## Active production package

`AF-IC-SHARED-FOUNDATION`

The package is currently **contracted** in `production/asset-manifest.json`. Its production source masters and runtime assets remain missing/unapproved in the repository.

Locked character-sheet facts now include:

- finalized male and female character sheets are **production geometry, not inspiration**;
- native character-sheet canvas is **512×64**;
- the sheet contains **eight contiguous 64×64 directional frames** in the approved existing order;
- every approved base pixel remains unchanged unless the user explicitly authorizes a base-character edit;
- base characters are never regenerated or stylistically reinterpreted for clothing/equipment work;
- clothing, armor, equipment, and accessories are separate transparent pixel overlays aligned to the locked sheet;
- enlarged inspection sheets are nearest-neighbor derivatives only; 10× = **5120×640**;
- composite previews are mechanical base-plus-overlay composites, never AI-redrawn dressed characters;
- no extra shading/detail may be added beyond the established sprite vocabulary;
- if fitting an asset requires guessing hidden body geometry, stop at the ambiguous frame/area rather than inventing anatomy or pose changes;
- actual Phaser integration is still required before checklist completion.

The machine-readable manifest now carries the 512×64 / 64×64 contract; the superseded 480×640 / 48×64 character keys were removed and the validator blocks their return.

## Slice 0 — Foundation Courtyard

Slice 0 is the next production proof. It must combine, in the running Phaser scene:

- Imperial stone ground and wear/decal treatment;
- street/building threshold;
- drainage channel/grate;
- aged stone foundation;
- timber/plaster wall;
- timber post and horizontal beam;
- one restrained sign/lantern/noren-style dressing cue;
- one foreground occluder;
- one fully dressed benchmark player.

The purpose is to prove character/world homogeneity, projection, hidden-grid concealment, traversal scale, collision, depth, occlusion, and the source-to-runtime pipeline before Harbor production expands.

Prior collage-derived Slice 0 boards and extracted candidates are **reference/scaffolding only**. They are not production source masters and must not be promoted merely because they were isolated or resized.

## Review gate

The machine rubric in `docs/data/art-review-rubric.json` and the human-readable rubric must stay synchronized.

- **0–29:** rejected
- **30–36:** rework required
- **37–41:** conditional/internal candidate only
- **42–45:** production approved
- **46–50:** lock quality

Approval additionally requires zero automatic failures and all critical minimums passing. Checklist completion begins only at **42+**.

Integrated review is valid only from the running Phaser canvas.

## Completion-state ownership

To avoid duplicate or contradictory progress tracking:

- the **world checklist** owns world-asset completion state;
- the **character checklist** owns character-asset completion state;
- `production/asset-manifest.json` owns the active package/runtime registration state;
- `IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md` owns route scope and production order;
- this file records only the current handoff snapshot.

Do not use this file as a second checklist.

## Next work order

1. review the scale reference scene beside the approved player and lock or adjust `docs/js/world/scale-guide.js` ratios;
2. author/approve the shared-foundation modules against those ratios without altering the locked base sheets;
3. run module and overlay QA (`validate-source-png.mjs`, `validate-world-data.mjs`), then register runtime modules in `authoredModules`;
4. capture Slice 0 from the running Phaser canvas and score it;
5. repair until all critical gates pass; at 42+, update only the relevant checklist/manifest completion state;
6. only then begin Harbor Arrival, then Market → Residential/Canal → Academy Exterior → Academy Interior/Sensei.

If an upstream gate fails, repair it before continuing downstream.
