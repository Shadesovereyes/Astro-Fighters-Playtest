# Astro Fighters — Current Development Status

**Updated:** 2026-10-12  
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
- eight-direction movement with four-direction player facing/animation (S, E, N, W);
- crisp pixel rendering;
- an integrated review captured from the actual Phaser canvas.

A collage, presentation board, source assembly, contact sheet, or mock renderer is never an integrated gameplay preview.

## Active production package

`AF-IC-SHARED-FOUNDATION`

The package is currently **contracted** in `production/asset-manifest.json`. Its production source masters and runtime assets remain missing/unapproved in the repository.

Four-direction facing adopted by the user (2026-10-12), replacing eight-direction facing:

- the player moves in eight directions and faces S, E, N or W: any horizontal component faces E or W (NE/SE use E, NW/SW use W), pure vertical faces N or S, no input keeps the last facing; attacks play and resolve in the current facing, and an attack press with a selected target first turns the character to face it (user 2026-10-12) (`characterFacing` in the manifest);
- runtime animation sheets (idle, walk, sprint, lightAttack, heavyAttack) have the rows S, E, N, W; W mirrors E; regenerated S, E, N, W rows are pixel-identical to the previously approved rows;
- the locked 512×64 reference sheets keep all eight frames; rig, anchors and overlay registration stay valid for all eight; diagonal animation views (walk, sprint, jab/cross, idle) are retired from runtime and remain in git history;
- AGENTS.md, Master Art Direction §11, EPE, Phaser World Refactor v0, README, the character checklist and the rubric (Markdown and JSON) updated; the validator enforces S, E, N, W rows;

Locked base geometry is under **change control** (approved 2026-10-02):

- finalized male and female character sheets are **production geometry, not inspiration**;
- the native **512×64** sheets (eight contiguous **64×64** directional frames, approved existing order) are the locked **reference poses** and frame 0 of each direction's `ready` state;
- new animation base frames (idle, walk, ready, attack) may be authored as deterministic data specs built from the reference pose as a cut-out rig; each becomes locked production geometry after user approval per state per direction;
- approved frames are never regenerated, redrawn, or stylistically reinterpreted; unlocking one requires explicit user instruction, a recorded reason, and overlay re-verification;
- each body has one canonical geometry; skin tones are palette swaps;
- sheet frame order, left to right (frames 0–7): `S, SE, E, NE, N, NW, W, SW` (recorded as `referenceFrameOrder` in the manifest);
- male clothing split: approved by the user (2026-10-02) (`overlays.json` + one part map per Male overlay layer); the armour belt split added afterwards is a candidate. Layer 2 clothing follows torso/pelvis/legs (never arms or head); the Gi sash (band, knot and tail) is its own overlay part `sash`, anchored at the hip, so it can sway independently; Layer 4 pieces follow their majority part (pads → upper arm, bracers → forearm); hair and eyes follow the head. The armour belt (waist band + hanging flap) is identified by position and outline — the outlined armour-colour region between the torso's lower outline and the knee band — and is also part `sash`, anchored at the hip;
- Male Gi S-frame shoes trimmed to the body-foot outline (7 px; toes no longer splay outward); trousers unchanged;
- animation plan approved (2026-10-06), recorded as `characterAnimationPlan` in the manifest: idle 8, walk 8, sprint 8, light attack jab/cross 8 (two 4-frame clips), heavy kick chain 16; four facings S, E, N, W (E/W first), max 16 frames, one speed per animation with holds only on approved key poses, per-frame root motion (dx, dy);
- long-hair sway split: approved for male and female (2026-10-06); built for male, female follows once the female rig exists — cap (rows ≤15, follows head), `hair-fall-upper` (rows 16–19, 1-frame lag), `hair-fall-lower` (rows 20+, 2-frame lag); 
- male idle (8 frames, S, E, N, W): approved by the user (2026-10-06); rendered by `tools/character-animate.mjs` into `production/source/characters/anim/male/idle/` from the spec `idle.json` — head leads the 1-px exhale and returns last, torso settles, arms lag on the way down (NE/NW arms move with the torso), hair falls settle after the cap; pelvis, legs and sash fixed. QC: no seam gaps, no new skin under any clothing, feet planted, frame 0 = reference. Layer 2 clothing at or below the waistline now always stays with the pelvis/legs;
- male walk (8 frames, S, E, N, W; E authored, W mirrored; diagonal views retired 2026-10-12): approved by the user (2026-10-06); rendered by `tools/character-posed.mjs` into `production/source/characters/anim/male/walk/` from the spec `walk.json`. The near leg runs 8 authored poses (contact, down, passing, up, contact, toe-off, passing swing, reach); the far leg runs the same poses 4 frames later, one shade darker, behind the body. Legs are row spans with the reference shading; contact/passing/up/reach reuse the reference wrap+foot block, down/toe-off/swing carry the shin slope through the wrap and use authored feet (flat, toe-off, toes dropped). Arms swing from the shoulder (near back 5 px as a pendulum with the wrist wrap rigid, forward 4 px along a line with a slight elbow bend); the far arm mirrors the phase. Body bob 0/+1/0/−1; hair falls lag but never rise above the part above them. Where the reference arm was painted into Body1 the uncovered torso/trunk is filled; generated outline is cleaned (pixels that outline nothing removed, doubled far-side lines merged). The W reference is verified as an exact mirror of E before mirroring. Root motion 3/2 px alternating (planted foot slides with it). QC: no unoutlined edges or holes, every frame touches the ground, palette locked. S and N (approved 2026-10-06) are built from their own reference frames with no new pixels: a raised leg is the leg shortened by dropping listed reference rows (swing lift 1/2/3/1 px, the planted leg stays on row 63), arms swing from the shoulder by dropping or repeating the elbow row, then a forearm row, then a wrist-wrap row (hand 3/2/0 px; forward lengthens in S and shortens in N), bob 0/+1/0/0, same step phase as E/W. Where a moved N arm's outline meets the trunk, the 1-px background hole is closed with outline. Approved as a draft state to revisit (2026-10-06): SE (SW mirrored) blends the S row edits with a sideways swing — legs move at the hip and swing to the foot, arms swing from the shoulder, far side drawn behind, new exposures outlined; all directions share one step phase and one bob (0/+1/0/−1, S/N repeat a leg row on −1 frames) and W/SW play their mirrored source half a cycle later, so the walk can change direction on any frame. NE (NW mirrored) approved 2026-10-07: built like SE from the back (forward arm shortens, legs spread with the right leg forward and cross with the left; near-arm length edits only on the wrap rows below 33). Sheets now hold all 8 directions in reference order S, SE, E, NE, N, NW, W, SW. Male Gi fitted to the walk (approved 2026-10-07, `male-gi.png` in the walk folder): front/back/diagonal views move each Gi pixel with the body part it covers; the profile (E, W mirrored) authors trouser rows on each posed leg (leg span widened 2 px back / 1 px front, Gi trouser shading, hem above the wrap, knee fold), keeps the reference wrap+shoe on reference-ankle poses, and on line poses stripes the sloped wrap rows and draws toe-down feet as the shoe; the jacket under the swung arm takes the jacket base colour; the far trouser is shaded one step darker; SW/NW Gi come from their own frames (the Gi is not an exact mirror there); leg skin uncovered from under the sash takes trouser mid colour; new cloth edges get the Gi outline. The sash flaps swing from the knot (row 34) as a pendulum phased with the step and lag the bob by a frame; body uncovered under them takes trouser mid colour. Male Gi E/W ankle wraps corrected (2026-10-07): the inner black stripe (column 29 E / 34 W, rows 56–59) is now wrap grey, so the wrap has a single outline; the idle Gi and rig overlay split were regenerated. The E/W wraps were then narrowed to the near ankle's 3-px wrap (rows 56–59, columns 30–34 E / mirrored W) to match the other directions; the far ankle shows the body's own wrap behind it. The sash band and knot now move exactly with the waist (bandFollowsBody); only the flaps lag and swing. Blue and red armour plus their shoulder pieces fitted to the walk (approved 2026-10-07) with the same rules: armour leg rows authored on each posed leg (2 px back / 1 px front, grey with white front), boots rigid from row 55 on reference-ankle poses and rebuilt as seamed shafts and boot-coloured feet on line poses, belt flap swinging below row 35; Layer 4 pads and bracers follow the arm part they sit on, and in E/W the hidden far arm gets the near pieces, shaded darker, wherever the far arm shows. Both armours' E/W boots were trimmed to the near boot (2026-10-07: far-boot sliver and its inner black line removed on rows 54–60, W mirrored), so the ankle has one outline like the Gi; the walk's sloped boot shafts use the same width. NW/NE seat fix (2026-10-07): NE hips do not shift sideways (spreading the joined thighs opened doubled seams at the seat, and a one-frame hip shift read as a jerk); each leg swings from the hip row (39) so the upper thigh angles with the stride (2026-10-07). Armour crotch fix (2026-10-07): the outline row closing the bottom of a hanging flap now swings with the flap (in SE/SW it belonged to the leg and left a box shape under the flap); cloth backing sits behind swinging flaps where they swing off the body; in front/back/diagonal views leg skin the garment moved off is covered with the gap colour; gaps between two leg outlines are left as drawn instead of being filled with a grey strip. A smooth 1 px hip sway toward the stance leg (pelvis, shorts/belt and both thigh tops: 0,1,1,1,0,−1,−1,−1) was tried for the male NE/NW and rejected by the user (2026-10-07) — keep it as a candidate idea for the female walk; clothing cleanup removes 1–2 px cloth specks and orphaned outline left between the legs (never uncovering the body), and closes body pinholes still showing inside cloth. Armours and shoulder pieces are still pending; clothing (Gi, armours) and shoulder accessories are not fitted to the walk yet;
- male sprint (8 frames, 14 fps, S, E, N, W): E/W and S/N approved by the user (2026-10-08); rendered by `tools/character-posed.mjs` from `sprint.json`. E: forward lean by torso shear (pelvis +1 to head +8, 3 torso rows dropped, head 2 px lower), authored constant-thickness band arms swept back with an authored fist, constant-thickness band legs (contact, load, drive, push-off, kick-back, recovery, knee drive, reach; pointBack/flex feet), flight frames 3 and 7. S/N: named running leg poses by row edits with a 2-row crouch, head level with E/W. To revisit: S arm sizing (upper arm widened, wrist and fist narrowed with a gap; the fist is 2 px wide) approved tentatively 2026-10-08. SE/SW and NE/NW retired 2026-10-12 (four-direction facing);
- male guard (combat idle, 4 frames, 6 fps, S, E, N, W; approved by the user 2026-10-12): the jab/cross guard with hands up and a slight 1 px bob (bob 1, 1, 2, 2; E legs bend 1 row on the low frames, S/N legs drop bob rows); the head bobs at the neck (1 px further down on the low frames, bob.head) and the arms bob at the shoulders a frame behind the body (bob.arms); every light and heavy attack clip returns to it (next: guard) and it holds while in combat, returning to the idle after a few seconds without an attack. Rendered by `tools/character-posed.mjs` from `guard.json`;
- male lightAttack jab/cross (8 frames, 12 fps, S, E, N, W, two clips: jab 0-3, cross 4-7, chain windows jab 2-3 and cross 6-7): E/W approved by the user (2026-10-09); S/N approved (2026-10-12). Rendered by `tools/character-posed.mjs` from `lightAttack.json`; band arms with elbow, boxing guard, outlined body parts (`characterAnimationPlan.outlineRule`); S/N hip and shoulder twist. Band-arm depth is per segment (z, zFore/foreAt) routed per pixel to the body or arms layer; arm accessories drawn only where the band arm shows. Previews must composite in the locked draw order (body, clothing, arms, shoulder/arm accessories, hair, eyes). SE/SW and NE/NW (approved temporarily 2026-10-09) retired 2026-10-12. Hitboxes per facing (W mirrors E); S/N added 2026-10-12 with the kick chain's convention (S top = E top + 14, N top = E top − 16, 16 px deep, centred on the punching fist): jab S [26, 32, 12, 16], N [28, 2, 12, 16]; cross S [25, 32, 14, 16], N [25, 2, 14, 16];
- male heavyAttack kick chain (16 frames, 12 fps, S, E, N, W; redesigned by the user 2026-10-12; approved by the user 2026-10-12 in S, E, N, W with its S/N part variants): lowKick 0-4 (rear-leg lift, low kick with the shin at knee height, recoil, return), snapKick 5-9 (rear knee lift, chamber, snap at stomach height, rechamber, return), spinRoundhouse 10-15 (spin through the spinPivot bodies, rear-leg roundhouse at head height, fold, recovery; finisher). Every clip starts and ends in the orthodox guard. E: kick legs to an explicit ankle point with authored feet. S/N: kicking legs authored in each view's coordinates with front/back cross-sections; the knee turns in toward the centre line and the low and snap kick feet sit on the centre line, sole toward the viewer (level three-row kick foot where the shin is level); height reads by leg shape (low kick knee at knee height, snap kick knee raised above the hip, roundhouse beside the head). Named part variants per frame (frontal.partVariants): bend (standing leg drops bob rows, knee out 1 px, body lower), plant (standing leg shifts toward the centre line), hike (kicking hip raised), tilt (torso leans away), rotate (torso and hips turned into the kick: far-side columns dropped, near side, head and shoulders toward the centre). Layering: S kicking leg in front of the standing leg and cut out of the arms layer and arm accessories; N kicking leg behind the standing leg (z 1.5 under 2). Spin frames from the spinPivot helper (guard arms, at most 2 px shift). Hitboxes per facing at each kick's height band. To revisit: spin bodies still change silhouette; N snap mostly hidden behind the body; standing-knee bend 1 px; three-quarter-body kicks were tried and undone at the user's request;
- combos (`production/source/characters/anim/male/combo.json`, user 2026-10-12): light attack and heavy attack are separate keys/buttons; one press per clip in rhythm (chain window = the clip's last two frames, earlier presses buffered); the only combos are light, light (jab, cross), light, light, heavy (jab, cross, spin roundhouse), light, heavy (jab, spin roundhouse) and heavy, heavy, heavy (low kick, snap kick, spin roundhouse); kicks never lead into punches; the spin roundhouse is the finisher. Hit area and targeting (user 2026-10-12, `combo.json` hitArea/targeting): every attack hits in an arc on the ground plane in front of the facing, furthest point 25 px from the foot pivot, half-angle 60° (arc approved by the user 2026-10-12) (120° arc, so targets not exactly aligned still connect), with the move's height band taken from its E hitbox; each active frame damages one target: the selected target if it is inside the arc, otherwise (no target selected, or the selected one out of the arc) the closest target inside; the choice is made again on every active frame, so a combo keeps hitting the same target while it is the selected target or still the closest; every attack press (including each chained step) with a selected target first turns the character to face it along the dominant axis, so the target sits in the arc's centre half. The authored hitbox rectangles now give only the height band (E) and the on-screen debug box (S/N). Implemented in the Phaser character lab (below);
- Phaser character lab (2026-10-12; runtime candidate integration, not world art and not rubric-scored): `tools/export-character-runtime.mjs male` copies the approved non-helper sheets byte-for-byte to `docs/assets/characters/male/<state>/` and writes `docs/data/characters/male.json` (states, S/E/N/W rows, fps, clips, events, root motion, layer slots in draw order, outfits, combo transitions); CI fails if the export is stale. `docs/character-lab.html` (Phaser 4.2.1 vendored at `docs/vendor/`, pixelArt, no antialias, roundPixels, integer zoom 3) assembles the paper doll from one sprite per layer (contact shadow, body, clothing, arms, arm accessories, hair, eyes) and drives it with continuous movement (walk 25 px/s and sprint 84 px/s from the sheets' root motion, normalised diagonals, delta time), the four-direction facing rule, idle → walk/sprint, J light / K heavy through the combo transitions (presses from the active frame buffered to the chain window, early presses dropped), per-frame attack root motion, the 25 px hit arc and target priority against three training posts (T selects a target, H shows the arc, debug boxes and collision), attack → guard → idle after 3 s (placeholder), outfits 1–4, hair 5, eyes 6. Verified in headless Chromium from the running canvas: no console errors; jab, cross, spin roundhouse, low kick and snap kick land; all four combos chain at rhythm. The ground arc replaces the earlier screen-space test, whose S/N reach was uneven (N 0–60 px, S 0–38 px). Not yet: world collision and props (Slice 0), guard timeout value, controller input;
- male oneHandDualGuard (dual-wield dagger combat stance, 4 frames, 6 fps, S, E, N, W): approved by the user 2026-10-13, with `items/tanto.json`; registered in the manifest and CI (`tools/character-weapon.mjs male oneHandDualGuard --check`); the runtime export now carries weapon layers (per hand and item, one sheet per depth slot) in `docs/data/characters/male.json` (`states.oneHandDualGuard.weapons`); the Phaser lab does not draw weapons yet. `twoHandGuard` (katana, `items/katana.json`) and `oneHandGuard` (wakizashi default, tanto option, `items/wakizashi.json`) approved by the user 2026-10-13 in S, E, N, W and registered the same way;
- male katanaLight (katana light chain, candidate 2026-10-13, E/W first): 8 frames, 12 fps; the user's spec: two vertical slashes, each one continuous swing — downCut, 12 to 6 (wind-up with the blade straight up; one smear frame with the blade arriving at 6 and a single crescent over the whole arc 12-3-6, active; hold at 6; return to the two-handed stance) and upCut, 6 to 12 (wind-up with the blade straight down; one smear frame arriving at 12 with a single crescent over 6-3-12, active; hold at 12; return). Chained from the hold at 6 the upCut enters at its smear frame (clip `entry`), so 12-6-12 plays as one continuous pair. Chain windows on each clip's last two frames, next: twoHandGuard. Hand positions are authored key poses (`keyPoses`) solved onto the band arms by two-link IK; katana grips measured from the rendered near fist; overhead frames split the katana at the grip (hilt in front, blade behind the head). The swing smear is a hard-edged pixel crescent around the swing's pivot in front of the shoulders (trail center/radius), widest at the blade and tapering to nothing, banded white / #e3e3e3 / #adadad from the tip inward (`items/katana.json` trail), drawn as its own FX sheet `main-katana-trail.png` over every character layer. Renderer fixes found on the way: the 64×64 bounds check rejects NaN coordinates; a sash sway table must have one entry per frame;
- weapon stances (candidates 2026-10-12, now S, E, N, W; S/N added 2026-10-12: S two-handed hands together at the navel with the katana drawn up the centre line foreshortened (scale 0.55); S one-handed weapon hand low at the right hip with a short foreshortened blade angled up and out, off hand up in the guard (dual: dagger blade up beside the face); N hands hidden in front of the body and the weapons drawn behind it — the katana angled up and right so its tip clears the head beside the right shoulder (user: the katana tip must show in N; daggers may be hidden); the weapon tool gained per-pose scale (foreshortening), layer and hidden (no fist to register to); S matched to E/W by projection lines (user 2026-10-13): every fist and weapon point in S sits on its E row (two-handed grip row 33, katana guard 31.4, tip 17.6; one-handed weapon fist row 35, guard fist row 26, dagger tip 14); the hands stay at their own sides with the forearms foreshortened toward the viewer (band-arm scale) instead of swung across the body; the S guard hand rises straight up from the left shoulder line (fist x 36–39, rows 24–27) so the fist and the off-hand dagger, gripped at the fist centre, sit beside the face (user 2026-10-13: fist and dagger were misaligned); a blade at E angle a is drawn vertical in S foreshortened by sin(a) (katana 0.64, wakizashi 0.17, raised dagger 1.0). Main-hand dagger raised to 35° (user 2026-10-13) so its blade reads in S (S scale 0.574, tip row 28.1), in the dual stance and as the tanto option of the one-handed stance (per-item pose overrides, `itemPoses`; the wakizashi keeps 10°). S layering fixed (user 2026-10-12): each weapon is split into depth slots rendered as separate sheets `<slot>-<item>-<depth>.png` (behind: under the body; front: over body and clothing, under the arms; top: over every character layer), with z per frame one slot or split at the grip ({hilt, blade}); in S the blades pointing at the viewer and the raised dagger in front of the head are top, the hilts under the fists are front; the user asked for separate one-handed and two-handed stances): `twoHandGuard` (katana, chudan middle guard: both hands on the hilt in front of the navel, near hand at the guard, far hand at the pommel mostly hidden behind the near forearm, blade forward and up at 40°) and `oneHandGuard` (wakizashi carried low in the near hand at the hip, tip forward and raised 10° (user 2026-10-12: not pointing down), free far hand up in the guard, lowered slightly (upper arm −38°, forearm 232°); reworked 2026-10-12 because the first version read the same as the two-handed stance); both on the approved guard legs and bob. Weapons are rigid layers rendered by `tools/character-weapon.mjs` from `production/source/characters/items/katana.json` and `wakizashi.json` (band construction along the weapon axis; the wakizashi is the katana construction shortened for one hand; palette only from approved clothing colours) into 128×128 frames (body frame at [32, 32], pivot [64, 95]) so swings can leave the 64×64 body frame; placed per frame at the authored grip (centre of the near fist, following the arm bob) and QC checks the grip lies under the arms layer; depth per frame (front: over body and clothing, under the arms; behind: under the body). `oneHandDualGuard` (user 2026-10-12: normal grip kept, reverse grip rejected and removed; then the tanto in both hands for the dual-wield grip): the one-handed stance with a tanto in each hand, normal grip, main hand low with the blade forward and raised 10°, off hand raised with the blade up; the tanto is also the alternative single-wield weapon in `oneHandGuard` (a hand slot lists alternative items, each rendered on the same grips as `<slot>-<item>.png`: oneHandGuard main-wakizashi / main-tanto, oneHandDualGuard main-tanto + off-tanto, twoHandGuard main-katana); combat idle loop with the guard motion (body bob 1, 1, 2, 2, head at the neck, arms at the shoulders a frame behind), both weapons riding their hands (grips follow the fists 0, −1, 0, +1). The tanto (`items/tanto.json`) has its hilt inside the fist (only pommel nub and guard show); the weapon tool carries one weapon per hand (`weapons`: main on the arms layer, off on the body layer). Not yet registered as runtime states;
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
