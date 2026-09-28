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

# Player-relative world scale standard

The player is the visual scale authority for the whole game world.

- Player runtime frame: **64×64 px**. The approved player sheet is **512×64 = eight contiguous 64×64 directional frames**.
- Every asset is proportioned against that player: architecture, doors, windows, counters, furniture, crates, bridges, stairs, railings, NPCs, enemies, weapons, vehicles, signs, foreground occluders, interaction distances, combat effects, and collision geometry.
- The hidden 32×32 grid is logic only (navigation, AI, placement, telegraphs, sectors). It never sets visual scale and must not be visually exposed during exploration.
- Required order: **64×64 player frame → believable player-relative proportion → author asset → independent collision/occlusion → test beside the player in Phaser.**
- Forbidden: **32×32 cell → multiply dimensions → assume the object is correctly scaled.** A manifest runtime canvas is a container size, not proof of scale.
- Player collision is an authored foot box (`production/asset-manifest.json` → `canonical.playerScale.collision`), never the full 64×64 sprite bounds.
- A door must read as walkable, a counter must land near hip height, stairs must match the character's feet and stride, crates must read at carry/storage scale, bridges must give believable passage width, and foreground walls must occlude the character without swallowing the whole sprite.
- Ratios live in `docs/js/world/scale-guide.js` as multiples of the measured player stature S, and are judged visually in the Phaser scale reference scene (`docs/index.html?scale`). They remain provisional until approved beside the approved 512×64 player.

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

# Locked character-sheet preservation standard

The finalized male and female character sheets are **production geometry, not inspiration**. When creating clothing, armor, equipment, accessories, or inspection previews, preserve the approved character pixels rather than regenerating or reinterpreting them.

Mandatory rules:

- **Never regenerate the base character.** Do not redraw the body, hair, face, anatomy, stance, proportions, directional pose, silhouette, or frame placement.
- **Never reinterpret the pixel style.** Match the approved sprite vocabulary exactly; do not smooth, modernize, increase detail density, or introduce a different shading language.
- Work on the native **512×64 character sheet**, consisting of **eight contiguous 64×64 frames**. Do not reorder, resize, reposition, warp, or resample the approved base frames.
- Preserve every existing source pixel unless the user explicitly authorizes changing the base character itself.
- Clothing/equipment must be built as **separate transparent pixel overlays** fitted to the existing silhouette. Do not alter the body to make a garment fit.
- Enlarged inspection versions must be derived only from the native asset using **integer nearest-neighbor scaling**. A 10× inspection sheet is therefore **5120×640**.
- Do not use an AI-generated dressed-character image as a composite preview. Composite previews must be made mechanically by placing the approved overlay over the untouched approved base sheet.
- Do not add extra shading, contour detail, texture density, or anatomical information beyond the established source-sprite vocabulary merely because a generator can produce it.
- If a garment or equipment layer cannot be placed without guessing hidden body geometry, stop at the specific ambiguous frame/area and identify the uncertainty rather than inventing anatomy, pose changes, or replacement pixels.
- High-contrast-background inspection may be used to find holes, stray transparency, floating pixels, broken seams, and routing errors, but QC corrections belong in the overlay—not in the locked base character.

For character-sheet asset work, these preservation rules override older experimental source-lattice assumptions or branch/package notes that would require redrawing the approved base geometry. Do not silently convert the locked 512×64 sheets into a different source format.

The approved paper-doll source is `/Paperdolls` (male and female: base body ×2 skin tones, clothing, arms, armor shoulders, hair, eyes), each a 512×64 sheet of eight 64×64 frames in the order **S, SE, E, NE, N, NW, W, SW**. Runtime copies under `docs/assets/characters/` are byte-identical and registered in `docs/js/world/characters.js`; draw order is body → clothing → arms → shoulders → hair → eyes. One frame per direction; no in-between animation frames may be invented. The Gi is the starter outfit; Red/Blue Armor are male-only until female armor layers are authored. QA: `node tools/validate-source-png.mjs sheet|overlay|inspection` and `node tools/validate-world-data.mjs`.

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

The current `docs/index.html` runtime and its legacy baked district backdrops may contain prototype debt. Their existence does not make their architecture canonical. Slice 0 scaffold textures (`docs/js/world/scaffold-textures.js`) are engine scaffolding only and must never be marked source-approved, runtime-candidate, integrated, or approved.

---

# Handoff rule

When reporting progress, clearly distinguish:

- concept/reference art;
- modular source art;
- runtime candidate assets;
- Phaser-integrated gameplay;
- rubric-approved production work.

Never describe one category as another.
