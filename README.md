# Astro Fighters Playtest

Astro Fighters is an **open-world, real-time action-combat RPG**. The current public implementation is the browser/Phaser runtime published from `/docs` through GitHub Pages.

This repository is the active public playtest/runtime surface and the production-control handoff for Imperial City development.

## Authoritative development state

**`main` is authoritative** unless this README or `DEVELOPMENT_STATUS.md` explicitly identifies a newer active development branch.

Old package branches and superseded pull requests remain useful as Git history, but they are not current production authority.

## Read before developing

Use this order:

1. [`README.md`](./README.md) — project orientation and architecture
2. [`AGENTS.md`](./AGENTS.md) — repository/runtime/development behavior
3. [`ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md`](./ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md) — visual canon
4. [`PHASER_WORLD_REFACTOR_V0.md`](./PHASER_WORLD_REFACTOR_V0.md) — current world-runtime migration gate
5. [`IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md`](./IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md) — active route, scope, and production order
6. [`Astro Fighters — Art Preview Review Rubric.md`](./Astro%20Fighters%20%E2%80%94%20Art%20Preview%20Review%20Rubric.md) — human review rules
7. [`docs/data/art-review-rubric.json`](./docs/data/art-review-rubric.json) — machine scoring authority
8. [`Astro Fighters — Imperial City Zone-by-Zone Asset Checklist.md`](./Astro%20Fighters%20%E2%80%94%20Imperial%20City%20Zone-by-Zone%20Asset%20Checklist.md) — world completion inventory
9. [`ASTRO_FIGHTERS_CHARACTER_CLOTHING_ACCESSORY_CHECKLIST.md`](./ASTRO_FIGHTERS_CHARACTER_CLOTHING_ACCESSORY_CHECKLIST.md) — character completion inventory
10. [`production/asset-manifest.json`](./production/asset-manifest.json) — current machine-readable package contract

`DEVELOPMENT_STATUS.md` is a concise handoff snapshot, not a second source of completion truth.

---

# Game architecture

## Current game

The game being built now is an **open-world, real-time action-combat RPG** with:

- free exploration through continuous authored space;
- continuous real-time movement;
- eight-direction facing and animation;
- direct action combat;
- layered world construction;
- collision independent from appearance imagery;
- NPCs, interactives, foreground occlusion, and cutaway interiors;
- real-time adaptation of Astro Fighters combat resources, abilities, statuses, astrology systems, and tactical logic;
- Phaser/browser runtime under `/docs` as the active public test surface.

Do not redesign the current game as a turn-based strategy title.

## Legacy Unity project

The private `Shadesovereyes/Astro-Fighters` Unity project is a **legacy turn-based tactical Combat Strategy vertical slice**.

It may be consulted for reusable design intent or math such as:

- damage and mitigation;
- poise/stagger;
- stamina/chakra/strain;
- statuses and crowd control;
- stealth/awareness;
- grapples and counters;
- summons and Seigan;
- astrology affinities;
- authored ability/balance concepts.

It is **not** the current runtime, scene architecture, movement model, UX, roadmap, or release target.

Do not port its turn loop, five-action slot planning, dynamic turn scheduler, hex battlefield, IMGUI prototype flow, or Unity battle/recovery scenes wholesale. Adapt useful mechanics to real-time timing, hit windows, animation commitment, interrupts, collision, cooldown/recovery, movement, input, and AI.

---

# Phaser runtime standard

The public build genuinely uses Phaser, but the current prototype still contains legacy shortcuts described in `PHASER_WORLD_REFACTOR_V0.md`.

Production world development must move from:

> **baked district image + visible grid + fixed tile-step actor**

into:

> **modular Phaser scene + hidden structural grid + continuous real-time actor**

A production gameplay scene must be assembled by Phaser from separate assets/layers such as ground, decals, architecture, dressing, props, collision, interactives, actors, foreground occluders, shadows, and atmosphere/FX.

A collage, presentation board, source assembly, contact sheet, Python/PIL composite, or mock renderer may be useful for reference or QA, but it **cannot be presented as an integrated gameplay preview**.

Integrated art review is valid only from the **running Phaser canvas**.

Pixel-rendering contract:

- `pixelArt: true`
- `antialias: false`
- `roundPixels: true`
- nearest-neighbor/pixel-preserving scaling
- coherent runtime pixel density across characters and world art

---

# Current milestone

The active milestone is **Imperial City Early Player Experience v0**.

First connected route:

> **SOUTHERN HARBOR ARRIVAL → DOCKS / SHIPWRIGHT → MARKET / SHOPPING STREET → RESIDENTIAL / CANAL TRANSITION → ASTRO FIGHTER ACADEMY EXTERIOR → ACADEMY INTERIOR / SENSEI TUTORIAL**

The Academy tutorial retains the established progression intent:

- Sensei teaches the combat foundation;
- General/Trap ability access is introduced;
- the player receives **100 mon**;
- the player chooses **3 distinct trap types, 10 of each**;
- inventory/paper-doll/action-RPG state reflects the result.

Crab-island/cave production is downstream and outside this milestone gate.

## Immediate production proof: Slice 0

Before Harbor production expands, **Foundation Courtyard Slice 0** must prove the art/runtime pipeline in Phaser using separate assets for:

- Imperial stone ground and decals;
- threshold and drainage;
- aged stone foundation;
- timber/plaster wall;
- timber post and beam;
- restrained analog dressing;
- one foreground occluder;
- fully dressed benchmark player.

The current active package is `AF-IC-SHARED-FOUNDATION` in `production/asset-manifest.json`.

Prior generated boards or collage-derived candidate packages are reference/scaffolding only and are not production source masters.

---

# Production document roles

To prevent duplicated or contradictory state:

- **README** — orientation and architecture
- **AGENTS.md** — repository/runtime/development behavior
- **Master Art Direction** — visual canon and generation discipline
- **EPE v0** — route scope and production order
- **World checklist** — world completion state
- **Character checklist** — character completion state
- **asset-manifest.json** — active package/runtime registration state
- **Rubric JSON** — machine scoring authority
- **Rubric Markdown** — synchronized human-readable rubric
- **DEVELOPMENT_STATUS.md** — concise current handoff snapshot
- **PHASER_WORLD_REFACTOR_V0.md** — temporary migration plan until its completion gate passes
- **SLICE_0_SOURCE_ART_BRIEF.md** — temporary execution brief until Slice 0 is locked

Git history is the version archive. Do not create permanent `v12`, `v13`, `v14` status files simply to preserve iterations.

---

# Art workflow

The required production sequence is:

> **CONTRACT → REFERENCE → PURPOSE-BUILT MODULAR SOURCE → ISOLATION/ANCHOR QA → SOURCE ASSEMBLY → SOURCE APPROVAL → RUNTIME DERIVATION → TARGET-PIXEL CLEANUP → PHASER INTEGRATION → RUBRIC**

Reference art establishes quality and design. It does not become production art merely by cropping, isolating, or shrinking it.

The world must rise to the quality of the approved character models. Do not lower character quality to match weak scenery.

Checklist completion occurs only after representative **actual Phaser gameplay** passes the locked review gate.

Review thresholds:

- **0–29:** rejected
- **30–36:** rework required
- **37–41:** conditional/internal candidate only
- **42–45:** production approved
- **46–50:** lock quality

Approval also requires zero automatic failures and all critical category minimums passing.

---

# Run / review surfaces

- `/docs/index.html` — current base runtime/prototype
- `/docs/play-v4.html` — current playtest launcher wrapper
- `/docs/art-review.html` — browser review/scoring surface

The launcher/patch and monolithic base runtime are temporary technical debt where identified by `PHASER_WORLD_REFACTOR_V0.md`; do not treat their current architecture as the production target simply because it already runs.

---

# Handoff rule

When reporting progress, distinguish clearly among:

- concept/reference art;
- modular source art;
- runtime candidate assets;
- Phaser-integrated gameplay;
- rubric-approved production work.

Never describe one category as another.
