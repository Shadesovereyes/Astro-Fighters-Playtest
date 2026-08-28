# Astro Fighters — Repository Agent Instructions

These instructions apply to the entire `Shadesovereyes/Astro-Fighters-Playtest` repository.

## Authority and required reading

Before changing runtime code, world art, character art, production manifests, checklists, or review status, read and obey:

1. `README.md`
2. `ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md`
3. `PHASER_WORLD_REFACTOR_V0.md`
4. `IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md`
5. `Astro Fighters — Art Preview Review Rubric.md`
6. both active world/character production checklists

If an older implementation conflicts with these instructions, the older implementation is technical debt unless the user explicitly relocks it.

---

# Locked Runtime Standard

Astro Fighters is an **open-world, real-time action-combat RPG**. The active public runtime is **Phaser/browser under `/docs`**.

Phaser is not merely a wrapper around a flattened illustration. Production gameplay scenes must be constructed and rendered by Phaser from separate runtime assets and world data.

## Required production world architecture

A production gameplay scene must use separate Phaser objects, containers, tile/object data, or equivalent runtime layers for the world, including as applicable:

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

The exact implementation may evolve, but the world must remain genuinely layered, traversable, depth-aware, and authored as game space.

## Forbidden production shortcuts

The following may be used only as reference, concept, diagnostic, or temporary scaffolding and **must never be presented as production-integrated gameplay**:

- photo-collage or cut-and-paste presentation composites;
- Python/PIL composites presented as gameplay;
- generated montage boards presented as gameplay;
- a single baked full-screen district image standing in for playable world construction;
- cropped pieces of a presentation board treated as production modular assets without proper source-authoring and QA;
- a custom mock canvas or isolated renderer presented as proof of Phaser integration;
- mixed-resolution imagery that reads as a collage rather than one coherent pixel-art game;
- persistent visible 32×32 grid overlays;
- pavement, floorboards, prop spacing, or architecture that visibly exposes the hidden gameplay grid;
- ordinary exploration driven by fixed integer tile stepping.

A beautiful concept image is still concept art. A technically loaded PNG is still not proof of world integration.

---

# Phaser Integration Gate

An integrated gameplay-art review is valid only when the reviewed scene is rendered by the actual Phaser runtime.

For a scene to count as integrated, verify in Phaser:

- separate runtime assets are loaded and assembled as world layers;
- the player moves through the scene in real time;
- collision is authored independently from the appearance image;
- eight-direction facing and animation respond to movement;
- foreground/background depth ordering works;
- the player can pass in front of and behind appropriate objects;
- cutaways/roof behavior works by authored architectural region where applicable;
- interactions remain readable;
- the hidden grid is not persistently visible or inferable;
- pixel-art rendering remains crisp and stylistically homogeneous;
- the screenshot or video used for integrated review comes from the running Phaser canvas.

Do not award an integrated rubric score to a presentation board, collage, source assembly, concept painting, isolated asset preview, or non-Phaser mockup.

---

# Exploration Movement Standard

Ordinary exploration must use continuous real-time movement rather than fixed tile stepping.

Required behavior:

- input from WASD/arrows/controller or equivalent;
- movement expressed in pixels per second;
- delta-time update;
- normalized diagonal movement;
- eight-direction facing selected from the movement vector;
- idle/walk/ready state driven by real movement state;
- authored collision against world geometry;
- visually smooth movement while retaining pixel-snapped rendering where appropriate.

The logical 32×32 grid may remain internally useful for AI, combat telegraphs, navigation sectors, encounter logic, placement, or ability systems. It is **structural, not graphical**, and must not dictate the visible cadence of normal exploration.

---

# Pixel Rendering Standard

Retain the Phaser pixel-rendering contract unless the user explicitly changes it:

- `pixelArt: true`
- `antialias: false`
- `roundPixels: true`
- nearest-neighbor / pixel-preserving scaling
- coherent runtime pixel density across characters, props, architecture, ground, VFX, and UI-adjacent gameplay art

Do not smooth, photographically interpolate, or mix incompatible pixel densities in production gameplay.

---

# Art Pipeline Standard

Use the locked workflow:

`CONTRACT → REFERENCE → MODULAR SOURCE → ISOLATION QA → SOURCE ASSEMBLY → SOURCE APPROVAL → RUNTIME DERIVATION → TARGET-PIXEL CLEANUP → PHASER INTEGRATION → RUBRIC`

Reference images establish target quality and design. They do not become game-ready simply by being cropped, reduced, or composited.

World and character modules must be purpose-built for the runtime contract, including correct anchors, alpha, palette, scale, direction, collision/occlusion role, and layer routing.

---

# Review and Completion Rules

The active art-review rubric remains mandatory.

- Below the gate: continue development automatically.
- `37–41`: conditional/internal candidate only if all automatic and critical gates pass.
- `42–45`: production approved.
- `46–50`: lock-quality target.

A checklist item may be marked complete only after representative **actual Phaser gameplay integration** passes the required score and no automatic failure is present.

The following are automatic blockers regardless of visual attractiveness:

- collage appearance;
- baked-background substitution for layered game space;
- visible/inferable permanent grid;
- mismatched character/environment pixel density or style;
- broken depth/occlusion;
- mannequin/incomplete presentation characters;
- non-Phaser preview presented as integrated gameplay;
- fixed grid-step exploration presented as the final open-world movement model.

---

# Current Legacy Debt

The existing Phaser vertical slice contains prototype shortcuts, including full-frame environment images and fixed grid-step exploration. Their presence in the current build does **not** make those patterns approved production architecture.

Treat `PHASER_WORLD_REFACTOR_V0.md` as the correction plan. Refactor toward modular Phaser world construction and continuous real-time movement before calling Imperial City Slice 0 production-integrated.

Do not regress to the old Unity turn-based tactical architecture. The private Unity project is reference material for reusable combat logic only.

---

# Handoff Rule

When reporting visual/runtime progress, clearly distinguish among:

- concept/reference art;
- modular source art;
- runtime candidate assets;
- Phaser-integrated gameplay;
- rubric-approved production work.

Never describe one category as another. In particular, never call a collage, source composite, or baked scene image an in-engine Phaser gameplay preview.
