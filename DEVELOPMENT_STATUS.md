# Astro Fighters — Current Development Status

**Updated:** 2026-10-06  
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

## Immediate technical gate

The current browser prototype genuinely uses Phaser, but its world layer still contains prototype debt:

- baked full-frame district imagery;
- visible 32×32 route/grid presentation;
- fixed integer tile-step exploration;
- collision tied too closely to grid rectangles;
- limited live depth/occlusion behavior.

`PHASER_WORLD_REFACTOR_V0.md` is the active correction plan.

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

Locked base geometry is under **change control** (approved 2026-10-02):

- finalized male and female character sheets are **production geometry, not inspiration**;
- the native **512×64** sheets (eight contiguous **64×64** directional frames, approved existing order) are the locked **reference poses** and frame 0 of each direction's `ready` state;
- new animation base frames (idle, walk, ready, attack) may be authored as deterministic data specs built from the reference pose as a cut-out rig; each becomes locked production geometry after user approval per state per direction;
- approved frames are never regenerated, redrawn, or stylistically reinterpreted; unlocking one requires explicit user instruction, a recorded reason, and overlay re-verification;
- each body has one canonical geometry; skin tones are palette swaps;
- sheet frame order, left to right (frames 0–7): `S, SE, E, NE, N, NW, W, SW` (recorded as `referenceFrameOrder` in the manifest);
- male clothing split: approved by the user (2026-10-02) (`overlays.json` + one part map per Male overlay layer); the armour belt split added afterwards is a candidate. Layer 2 clothing follows torso/pelvis/legs (never arms or head); the Gi sash (band, knot and tail) is its own overlay part `sash`, anchored at the hip, so it can sway independently; Layer 4 pieces follow their majority part (pads → upper arm, bracers → forearm); hair and eyes follow the head. The armour belt (waist band + hanging flap) is identified by position and outline — the outlined armour-colour region between the torso's lower outline and the knee band — and is also part `sash`, anchored at the hip;
- Male Gi S-frame shoes trimmed to the body-foot outline (7 px; toes no longer splay outward); trousers unchanged;
- animation plan approved (2026-10-06), recorded as `characterAnimationPlan` in the manifest: idle 8 (all 8 directions), walk 8, sprint 8, light attack jab/cross 4, heavy kick chain 16 (E/W first for all but idle), max 16 frames, one speed per animation with holds only on approved key poses, per-frame root motion (dx, dy);
- long-hair sway split: approved for male and female (2026-10-06); built for male, female follows once the female rig exists — cap (rows ≤15, follows head), `hair-fall-upper` (rows 16–19, 1-frame lag), `hair-fall-lower` (rows 20+, 2-frame lag); 
- male idle (8 frames, all 8 directions): approved by the user (2026-10-06); rendered by `tools/character-animate.mjs` into `production/source/characters/anim/male/idle/` from the spec `idle.json` — head leads the 1-px exhale and returns last, torso settles, arms lag on the way down (NE/NW arms move with the torso), hair falls settle after the cap; pelvis, legs and sash fixed. QC: no seam gaps, no new skin under any clothing, feet planted, frame 0 = reference. Layer 2 clothing at or below the waistline now always stays with the pelvis/legs;
- male walk (8 frames, E authored, W mirrored): approved by the user (2026-10-06); rendered by `tools/character-posed.mjs` into `production/source/characters/anim/male/walk/` from the spec `walk.json`. The near leg runs 8 authored poses (contact, down, passing, up, contact, toe-off, passing swing, reach); the far leg runs the same poses 4 frames later, one shade darker, behind the body. Legs are row spans with the reference shading; contact/passing/up/reach reuse the reference wrap+foot block, down/toe-off/swing carry the shin slope through the wrap and use authored feet (flat, toe-off, toes dropped). Arms swing from the shoulder (near back 5 px as a pendulum with the wrist wrap rigid, forward 4 px along a line with a slight elbow bend); the far arm mirrors the phase. Body bob 0/+1/0/−1; hair falls lag but never rise above the part above them. Where the reference arm was painted into Body1 the uncovered torso/trunk is filled; generated outline is cleaned (pixels that outline nothing removed, doubled far-side lines merged). The W reference is verified as an exact mirror of E before mirroring. Root motion 3/2 px alternating (planted foot slides with it). QC: no unoutlined edges or holes, every frame touches the ground, palette locked. S and N (approved 2026-10-06) are built from their own reference frames with no new pixels: a raised leg is the leg shortened by dropping listed reference rows (swing lift 1/2/3/1 px, the planted leg stays on row 63), arms swing from the shoulder by dropping or repeating the elbow row, then a forearm row, then a wrist-wrap row (hand 3/2/0 px; forward lengthens in S and shortens in N), bob 0/+1/0/0, same step phase as E/W. Where a moved N arm's outline meets the trunk, the 1-px background hole is closed with outline. Approved as a draft state to revisit (2026-10-06): SE (SW mirrored) blends the S row edits with a sideways swing — legs move at the hip and swing to the foot, arms swing from the shoulder, far side drawn behind, new exposures outlined; all directions share one step phase and one bob (0/+1/0/−1, S/N repeat a leg row on −1 frames) and W/SW play their mirrored source half a cycle later, so the walk can change direction on any frame. NE (NW mirrored) approved 2026-10-07: built like SE from the back (forward arm shortens, legs spread with the right leg forward and cross with the left; near-arm length edits only on the wrap rows below 33). Sheets now hold all 8 directions in reference order S, SE, E, NE, N, NW, W, SW. Male Gi fitted to the walk (candidate 2026-10-07, `male-gi.png` in the walk folder): front/back/diagonal views move each Gi pixel with the body part it covers; the profile (E, W mirrored) authors trouser rows on each posed leg (leg span widened 2 px back / 1 px front, Gi trouser shading, hem above the wrap, knee fold), keeps the reference wrap+shoe on reference-ankle poses, and on line poses stripes the sloped wrap rows and draws toe-down feet as the shoe; the jacket under the swung arm takes the jacket base colour; the far trouser is shaded one step darker; SW/NW Gi come from their own frames (the Gi is not an exact mirror there); leg skin uncovered from under the sash takes trouser mid colour; new cloth edges get the Gi outline. Armours and shoulder pieces are still pending; clothing (Gi, armours) and shoulder accessories are not fitted to the walk yet;
- contact shadow registered as the lowest character layer (`Paperdolls/contact-shadow.png`, fixed ellipse, fully opaque);
- Male Body1 replaced with the user's updated sheet (2026-10-06): S/N legs straighter and narrower, NE/NW feet adjusted; Arms1, hair and eyes unaffected. Refits: Male Gi S/N hem underline and ankle wraps shifted inward with the shins (S 1 px, N 2 px), S/N shoes rebuilt on the new foot shapes, NE/NW changed foot rebuilt the same way; trousers above row 54 unchanged (shifting them would make the inner edges overlap; they still cover the new legs). Both armours: N boots (rows 54–63) shifted 2 px inward. No skin shows under any male clothing layer in the changed frames;
- Male Gi S frame reworked (approved 2026-10-06): trouser outer edges straightened (hip to cuff, inner edges unchanged) so the legs no longer bow; trousers lengthened 2 rows (rows 50–51 repeated, hem now rows 54–56); ankle wraps straightened to a 5-px column and shortened to rows 57–59. Applied to all other directions (approved 2026-10-06): outer edges straightened from row 44 to the hem (profiles: front and back edges; SE and NE keep 1 px of the original knee curve), trousers 2 rows longer, wraps straightened and 2 rows shorter; where the narrow wrap would uncover ankle skin, the row just above the shoe keeps its original shape (SE/SW raised foot, E/W, NE both legs, NW left);
- male part split and anchors: approved by the user (2026-10-02); generated by `tools/character-rig.mjs` into `production/source/characters/rig/male/` (part map + rig.json, every Body1 pixel in exactly one of 11 parts, 13 anchors per frame). Approved choices: profile shoulder cap rows 21–24 stay torso, elbow rows 28 (profiles 30), knees at each leg's narrowest row (profile near knee 46). In E and W the far arm is fully hidden and the far thigh is hidden behind the near thigh; only the far shin-foot is visible;
- clothing, armor, equipment, and accessories are separate transparent overlays: rigid items placed by anchor, deformable items authored per body-part pose, coverage tracked per direction × state × frame;
- AI-generated images are reference only; no production pixel is converted from them;
- enlarged inspection sheets are integer nearest-neighbor derivatives only; 10× = **5120×640**;
- composite previews are mechanical base-plus-overlay composites;
- if fitting an asset requires guessing hidden or unapproved body geometry, stop at the ambiguous frame/area;
- actual Phaser integration is still required before checklist completion.

The `480×640` source / `48×64` runtime character contract is retired. `production/asset-manifest.json` now records the 512×64 sheet, 64×64 frame, and pivot `[32,63]` (measured: lowest opaque row of every reference frame is y=63, frame center x=32).

Open character-geometry items:

- body geometry: Body1 is the only base geometry for both bodies; Female Body1 is the user's corrected sheet. Body2 sheets are skin-tone references only, kept as originally authored. Body1/Arms1 (male and female) now share one locked 5-step skin ramp (`#f6a35b` / `#c87845` / `#9e4a31` / `#70241d` / `#3f0505`); tone 2 ramp approved (`#e0764b` / `#b24b36` / `#96392b` / `#7b2b21` / `#4a1510`);
- reference-pose feet touch the frame bottom (y=63), leaving no headroom below the contact line;
- the `/docs` prototype still loads `48×64` paper-doll sheets; that is prototype debt, not the production contract.

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

1. complete the Phaser world refactor minimum needed for Slice 0;
2. author/approve the shared-foundation source assets and player source authorities without altering the locked finalized base sheets;
3. run source isolation/anchor/assembly QA;
4. derive and manually clean runtime candidates only after source approval;
5. assemble Slice 0 from separate assets in Phaser;
6. capture the actual Phaser gameplay frame and score it;
7. repair until all critical gates pass;
8. at 42+, update only the relevant checklist/manifest completion state;
9. proceed into Harbor Arrival, then Market → Residential/Canal → Academy Exterior → Academy Interior/Sensei.

If an upstream gate fails, repair it before continuing downstream.
