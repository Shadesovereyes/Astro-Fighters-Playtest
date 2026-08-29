# Astro Fighters — Repository Agent Instructions

These instructions apply to the entire `Shadesovereyes/Astro-Fighters-Playtest` repository.

## Authority order

Before changing runtime code, world art, character art, production manifests, checklists, or review state, read:

1. `README.md`
2. `AGENTS.md`
3. `ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md`
4. `production/NEGATIVE_PROMPT_REGISTER.md`
5. `PHASER_WORLD_REFACTOR_V0.md`
6. `IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md`
7. `Astro Fighters — Art Preview Review Rubric.md`
8. `docs/data/art-review-rubric.json`
9. both production checklists
10. `production/asset-manifest.json`
11. `DEVELOPMENT_STATUS.md`

If an older implementation, branch, package note, or prototype conflicts with these authorities, treat the older material as technical debt or historical reference unless the user explicitly relocks it.

`main` is authoritative unless README or Development Status explicitly identifies a newer active development branch.

---

# User-correction capture rule

Every explicit user correction to generated art, asset style, proportions, materials, composition, presentation, prompt wording, or recurring visual drift must be persisted so the user does not have to repeat it.

For every such correction:

1. identify the rejected failure mode precisely;
2. add or update the appropriate negative constraint in `production/NEGATIVE_PROMPT_REGISTER.md` before further related generation;
3. update the relevant lasting canon/contract file as well when the correction changes a durable production rule;
4. preserve prior corrections unless the user explicitly reverses or supersedes them;
5. treat the register as required prompt context for future related image generation and art review.

Do not rely only on chat memory for a correction that affects production art.

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

Character-generation prompts must also apply the negative constraints in `production/NEGATIVE_PROMPT_REGISTER.md`, including the locked rejection of chibi / super-deformed player proportions.

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
