# Astro Fighters — Repository Agent Instructions

These instructions apply to the entire `Shadesovereyes/Astro-Fighters-Playtest` repository.

## Authority order

Before changing runtime code, world art, character art, production manifests, checklists, or review state, read:

1. `README.md`
2. `AGENTS.md`
3. `ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md`
4. `PHASER_WORLD_REFACTOR_V0.md`
5. `IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md`
6. `Astro Fighters — Art Preview Review Rubric.md`
7. `docs/data/art-review-rubric.json`
8. both production checklists
9. `production/asset-manifest.json`
10. `DEVELOPMENT_STATUS.md`

If an older implementation, branch, package note, or prototype conflicts with these authorities, treat the older material as technical debt or historical reference unless the user explicitly relocks it.

`main` is authoritative unless README or Development Status explicitly identifies a newer active development branch.

---

# Locked runtime standard

Astro Fighters is an **open-world, real-time action-combat RPG**. The active public runtime is **Phaser/browser under `/docs`**.

The private Unity project is a legacy turn-based tactical Combat Strategy vertical slice. It may supply reusable combat design intent/math, but it is not the current runtime, scene architecture, movement model, roadmap, or release target.

Do not reintroduce the Unity turn loop, five-action slot queue, dynamic turn scheduler, hex battlefield as exploration space, or prototype IMGUI flow.

---

# Phaser world standard

Production gameplay scenes must be constructed and rendered by Phaser from separate runtime assets and world data.

Use separate objects/containers/layers as appropriate for:

1. ground
2. decals / wear
3. architecture
4. architecture dressing
5. props-back
6. collision
7. interactives
8. actors
9. props-front / occluders
10. local shadows
11. atmosphere / FX

The exact implementation may evolve, but playable space must remain layered, traversable, depth-aware, and authored as game space.

## Forbidden production shortcuts

The following are reference/QA/scaffolding only and must never be presented as production-integrated gameplay:

- photo-collage or cut-and-paste composites;
- Python/PIL composites;
- generated montage boards;
- single baked full-screen district images standing in for playable construction;
- cropped presentation-board pieces treated as production modular assets without independent authoring/QA;
- custom mock canvases or isolated renderers presented as Phaser proof;
- mixed-resolution imagery that reads as a collage;
- persistent visible 32×32 grid overlays;
- repeated seams/spacing that reveal the hidden grid;
- ordinary exploration driven by fixed integer tile stepping.

A beautiful concept image is still concept art. A loaded PNG is not proof of world integration.

---

# Integration gate

An integrated gameplay-art review is valid only when the reviewed scene is rendered by the actual Phaser runtime.

Verify in Phaser:

- separate runtime assets are loaded and assembled as world layers;
- the player moves continuously in real time;
- collision is authored independently from appearance imagery;
- eight-direction facing/animation responds to movement;
- foreground/background depth ordering works;
- the player can pass in front of and behind appropriate objects;
- authored cutaways/roof behavior works where applicable;
- interactions remain readable;
- the hidden grid is not persistently visible or inferable;
- pixel-art rendering remains crisp and homogeneous;
- review screenshots/video come from the running Phaser canvas.

Do not award an integrated rubric score to a presentation board, collage, source assembly, concept painting, contact sheet, isolated asset preview, or non-Phaser mockup.

---

# Exploration movement standard

Ordinary exploration uses continuous real-time movement:

- WASD/arrows/controller or equivalent input;
- velocity in pixels/second;
- delta-time update;
- normalized diagonal movement;
- eight-direction facing from movement vector;
- idle/walk/ready state from real movement state;
- authored world collision;
- pixel-snapped rendering where appropriate.

The logical 32×32 grid may still support AI, navigation sectors, authored placement, combat telegraphs, encounter logic, or abilities. It is structural, not graphical.

---

# Pixel rendering standard

Retain unless explicitly changed:

- `pixelArt: true`
- `antialias: false`
- `roundPixels: true`
- nearest-neighbor / pixel-preserving scaling
- coherent runtime pixel density across characters, props, architecture, ground, VFX, and gameplay-adjacent UI

Do not smooth or photographically interpolate production pixel art.

---

# Locked base geometry — change control

The finalized male and female character sheets are **production geometry, not inspiration**. Approved base frames are never regenerated, reinterpreted, smoothed, or redrawn. Base geometry may grow only through the approval gate below; it is never changed casually.

The rule exists for two reasons, and both must keep holding:

1. **no drift** — generators and redraws must not reinterpret the character; approved pixels are authored data, not a style suggestion;
2. **exact registration** — every clothing, armor, equipment, and accessory overlay is registered pixel-for-pixel to the base. Interchangeable equipment depends on base geometry that does not move.

## Reference poses

- The existing native **512×64** sheets (**eight contiguous 64×64 frames**) remain untouched as the reference poses and as frame 0 of the `ready` state for each direction.
- Do not reorder, resize, reposition, warp, or resample the reference frames.
- Preserve every reference-pose pixel unless the user explicitly authorizes a base-character edit.

## Approval gate for new base frames (animation bases)

New body frames for animation states (idle, walk, ready, attack, and later states) may be authored only when they:

- are authored as data specs rendered deterministically — never converted from generator output;
- use only the locked body palette, hard alpha, and no shading, texture density, contour, or anatomy beyond the established sprite vocabulary;
- keep the shared 64×64 frame and pivot/foot contact unless the motion intends otherwise (jump, lunge);
- trace every part to reference-pose pixels or to an approved part variant (cut-out rig moves are whole-pixel only; no rotation or resampling);
- carry committed anchor and per-frame draw-order metadata;
- receive user approval, recorded per state per direction.

On approval, a new base frame becomes **locked production geometry** with protection identical to the reference poses. Changing any approved frame requires an explicit user unlock, a recorded reason, and re-verification of every overlay registered to it.

## Body geometry and skin variants

- Each body (male, female) has one canonical geometry. Skin-tone variants are palette swaps of that geometry, not separate sheets.
- Male Body1/Body2 already share an identical silhouette. Female Body1/Body2 differ by 8 silhouette pixels; one canonical version must be chosen through a one-time explicit base edit before female overlays are produced.

## Equipment and overlays

- Clothing, armor, equipment, and accessories are separate transparent pixel overlays fitted to approved base frames. Never alter the body to make a garment fit.
- Overlays contain no replacement skin, body, hair, face, or background pixels.
- **Rigid items** (helmets, shoulder pieces, weapons, shields) are authored per direction plus approved variants and placed by anchor with integer offsets.
- **Deformable items** (garments, armor bodies, sleeves, trousers, hair) are authored per body-part pose (torso, head, near/far arm, near/far leg) and reused wherever that part pose appears.
- Draw order comes from per-frame metadata and follows the character's anatomical side.
- An equipment item is not runtime-eligible until its coverage table shows every direction × state × frame covered by an overlay, an anchor placement, or a reused part pose.
- QC corrections belong in the overlay — never in a locked base frame.
- If fitting an item requires hidden or unapproved body geometry, stop at the specific frame/area and report it rather than inventing anatomy or pose changes.

## Generated imagery

AI-generated images are reference only (pose ideas, silhouettes, palette studies). No production pixel may come from converting a generated image, including palette-matched or downsampled conversions. Production pixels come only from authored specs or direct pixel authoring.

## Inspection and previews

- Enlarged inspection versions use **integer nearest-neighbor scaling** only. A 10× inspection sheet is **5120×640**.
- Composite previews are mechanical: approved overlays placed over untouched approved base frames. Never present an AI-generated dressed-character image as a composite.
- High-contrast-background inspection may be used to find holes, stray transparency, floating pixels, broken seams, and routing errors.

These rules override older experimental `480×640` source-lattice / `48×64` runtime assumptions, which are retired for character production. Do not silently convert the locked sheets into a different source format.

---

# Art pipeline standard

Use:

`CONTRACT → REFERENCE → PURPOSE-BUILT MODULAR SOURCE → ISOLATION/ANCHOR QA → SOURCE ASSEMBLY → SOURCE APPROVAL → RUNTIME DERIVATION → TARGET-PIXEL CLEANUP → PHASER INTEGRATION → RUBRIC`

Reference images define design/quality targets. They do not become production-ready by cropping, shrinking, segmenting, or compositing.

World and character modules must be purpose-built for the runtime contract, including anchors, alpha, palette, scale, direction, collision/occlusion role, and layer routing.

---

# Generation vocabulary discipline

The Imperial City has repeatedly drifted when generic latent-space magnet words are used in generation prompts. Do not use the following as generic generation anchors:

- `neon`
- `wet street` / `wet asphalt` / reflective pavement
- `machine hall`
- `engine room`
- `boiler`
- generic `machinery`
- `pistons`
- `gears`
- `clockwork`
- generic `brass`
- generic `pipes`
- `steam` as a hero aesthetic
- `furnace`
- generic `factory`
- `monumental city`
- generic `tower` / `spire`
- `ziggurat`
- `pagoda`
- `temple gate`
- generic `Asian city`
- `cyberpunk`
- `Blade Runner`
- magenta/cyan glow language

When a checklist contains a legacy functional label such as a pipe, control box, tower, or wet harbor surface, interpret the **function** through the Master Art Direction instead of copying the risky noun into a generation prompt.

Preferred Imperial City language includes:

- pale civic stone, slate, patinated copper, warm aged timber;
- sealed/recessed service channels and integrated instrument housings;
- restrained clean-iron brackets and practical junction hardware;
- dry matte streets with only localized waterline darkening where physically appropriate;
- warm sodium amber and weak cathode green only when evening lighting is needed;
- horizontal inherited civic massing and named canonical apparatus rather than generic industrial spectacle.

---

# Review and completion rules

The machine rubric in `docs/data/art-review-rubric.json` is the scoring authority. The Markdown rubric must mirror it.

- `0–29`: rejected
- `30–36`: rework required
- `37–41`: conditional/internal candidate only
- `42–45`: production approved
- `46–50`: lock quality

Checklist completion requires **42+**, zero automatic failures, and all critical minimums passing.

Current automatic blockers include collage appearance, baked-background substitution, visible/inferable grid, mismatched pixel density/style, broken depth/occlusion, mannequin characters, non-Phaser imagery presented as integrated gameplay, and fixed grid-step exploration presented as final open-world movement.

---

# Completion-state ownership

To prevent redundant state:

- world checklist owns world completion;
- character checklist owns character completion;
- `asset-manifest.json` owns active package/runtime registration;
- EPE owns route scope and production order;
- Development Status owns only the current handoff snapshot;
- Git history owns iteration history.

Do not create permanent versioned status files or duplicate completion checklists.

---

# Temporary documents and debt

`PHASER_WORLD_REFACTOR_V0.md` is a temporary migration authority. Keep it until its completion gate passes, then retire/archive it rather than allowing it to become permanent historical process text.

`production/SLICE_0_SOURCE_ART_BRIEF.md` is a temporary active execution brief. Retire it after Slice 0 is locked and the next package becomes authoritative.

The current `docs/index.html`, `play-v4.html`, and launcher patch may contain prototype debt. Their existence does not make their architecture canonical.

---

# Handoff rule

When reporting progress, clearly distinguish:

- concept/reference art;
- modular source art;
- runtime candidate assets;
- Phaser-integrated gameplay;
- rubric-approved production work.

Never describe one category as another.
