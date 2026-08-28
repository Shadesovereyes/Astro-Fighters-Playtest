# Astro Fighters Playtest

Astro Fighters is an **open-world action-combat RPG**. The current playable implementation is the browser/Phaser RPG runtime published from `/docs` through GitHub Pages.

This repository is the **current public playtest/runtime surface** and also the **art-development control surface and handoff record** for Imperial City production. A new chat session or development agent should be able to open this repository, understand the actual game architecture, inspect the current playable state, read the production rules, and continue development without restarting architectural or art-direction discovery.

## Current authoritative development state

**PR #11 has been merged. The authoritative repository state is now `main`.**

New chat sessions, development agents, code assistants, and reviewers must start from `main` unless this README or `DEVELOPMENT_STATUS.md` explicitly identifies a newer active development branch.

The workflow previously developed on `development/art-review-workflow-v1` has been merged into `main`. That branch is now historical development context rather than the active authority. The merged Phaser/world corrections, art-review workflow, production manifest, early-player Imperial City plan, repository agent instructions, and handoff rules now live on `main`.

Before continuing world/runtime work, read `AGENTS.md` and `PHASER_WORLD_REFACTOR_V0.md` from `main`.

The active early-game production roadmap is [`IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md`](./IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md). It scopes the first connected production-quality route as **Southern Harbor → Docks/Shipwright → Civic Market → Residential/Canal transition → Astro Fighter Academy exterior → Academy interior/Sensei tutorial**.

---

# GAME ARCHITECTURE — READ BEFORE DEVELOPING

## Current game target

The game being built now is an **open-world, real-time action-combat RPG**. Its gameplay target includes:

- free exploration through a continuous authored world;
- real-time player movement rather than turn-by-turn battlefield movement;
- eight-direction character facing and animation;
- direct action combat rather than a five-slot turn queue;
- layered environments, collision, interactives, NPCs, foreground occlusion, and world traversal;
- real-time adaptation of Astro Fighters combat resources, abilities, statuses, astrology systems, and tactical rules;
- a playable Phaser/browser runtime under `/docs` as the current public test surface.

**Do not redesign Astro Fighters as a turn-based strategy game. Do not treat the old Unity prototype as the current game.**

## Legacy Unity Combat Strategy vertical slice

The private `Shadesovereyes/Astro-Fighters` Unity project is a **previous vertical slice for a turn-based tactical Combat Strategy prototype**. It exists as a combat-design and systems reference. It is **not** the current open-world RPG runtime, scene architecture, control model, release target, or development roadmap.

The Unity slice may be consulted to recover or validate reusable combat logic such as:

- physical, elemental, and mental damage concepts;
- mitigation and poise/stagger logic;
- stamina, chakra, strain, and other resource rules;
- statuses, crowd control, stealth/awareness concepts, grapples, counters, summons, and Seigan rules;
- astrology-derived affinities and loadout concepts;
- authored ability data and balance assumptions that remain compatible with the RPG design.

Those systems must be **adapted to real-time action combat**. The following Unity-specific structures are not the target architecture and must not be copied into the RPG merely because they exist in the vertical slice:

- turn rounds as the primary gameplay loop;
- five-action slot planning;
- the dynamic turn scheduler as a literal runtime scheduler;
- hex-battlefield encounter structure as the open-world movement model;
- IMGUI prototype UX;
- Unity recovery/battle scenes as the production world;
- any assumption that a system is correct for the action RPG simply because it worked in the turn-based slice.

When translating a mechanic from the Combat Strategy slice, preserve the **design intent and useful math**, then re-express it for real-time timing, hit windows, animation commitments, movement, cooldowns/recovery, interrupts, spatial collision, and player input.

## Authority when repositories disagree

For the current game:

1. this public playtest repository and its current runtime behavior define the active RPG implementation;
2. current locked art/gameplay production documents define the required presentation and integration rules;
3. the Unity Combat Strategy project is reference material for reusable combat logic only.

A future developer must **not redirect development into the Unity project** after discovering that its combat code is more mature in some areas. The task is to adapt useful combat logic into the open-world action RPG.

---

# Art Development Workflow — READ THIS FIRST

Astro Fighters art development is **source-driven, checklist-driven, and rubric-gated**. Do not improvise a new visual direction and do not treat technically functional placeholder art as production art.

The required operating sequence is:

> **MASTER ART DIRECTION → CHECK BOTH ASSET CHECKLISTS → DEVELOP → INTEGRATE IN GAME → SCORE WITH RUBRIC → REFINE OR MARK COMPLETE → CONTINUE**

The five controlling production documents are:

1. [`ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md`](./ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md) — **HOW to develop the art.**
2. [`IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md`](./IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md) — **WHICH world/character dependencies are first for the early player experience.**
3. [`Astro Fighters — Imperial City Zone-by-Zone Asset Checklist.md`](./Astro%20Fighters%20%E2%80%94%20Imperial%20City%20Zone-by-Zone%20Asset%20Checklist.md) — **WHAT world/scenery assets remain to be developed.**
4. [`ASTRO_FIGHTERS_CHARACTER_CLOTHING_ACCESSORY_CHECKLIST.md`](./ASTRO_FIGHTERS_CHARACTER_CLOTHING_ACCESSORY_CHECKLIST.md) — **WHAT character clothing, hair, equipment, and accessory work remains to be developed in parallel.**
5. [`Astro Fighters — Art Preview Review Rubric.md`](./Astro%20Fighters%20%E2%80%94%20Art%20Preview%20Review%20Rubric.md) — **WHEN an integrated result is good enough to test or mark production-complete.**

These files are not optional reference notes. Together they define the production process.

---

# 1. Master Art Direction Is the Governing Authority

Before creating, editing, integrating, or evaluating any visual asset, read the **LOCKED MASTER ART DIRECTION PROMPT**.

It governs:

- 90s-anime-inspired pixel-art language
- character/world quality parity
- Edo + martial + hip-hop/streetwear identity
- Imperial City world identity
- warm analog/Japandi-industrial materials
- monumental ancient-industrial infrastructure
- hidden 32×32 square-grid presentation
- eight-direction character and movement requirements
- flat-faced 3/4 cabinet projection
- modular layered world construction
- character clothing/equipment expectations
- material and palette discipline
- occlusion and interior cutaway behavior
- presentation-preview requirements
- prohibited shortcuts and automatic art failures

**Do not lower the character standard to match weak scenery. The world must rise to the quality of the approved character models.**

If a proposed asset conflicts with the Master Art Direction Prompt, the asset is wrong even if it is technically convenient.

---

# 2. World Development Uses the Zone-by-Zone Checklist

After reading the Master Art Direction Prompt, inspect the **Imperial City Zone-by-Zone Asset Checklist**.

Use it to determine the next world dependencies rather than inventing ad-hoc scenery. Development should consider shared/global Imperial City assets first when they unblock multiple districts, then proceed through the district families and current playable slice needs.

The checklist covers, among other areas:

- global Imperial City surfaces and architectural components
- Imperial Harbor / Docks
- Civic Market / Shops
- Artisan / Workshop Ward
- Astro Fighter Academy exterior
- Astro Fighter Academy interiors
- Residential / canal neighborhoods
- Shrines / spiritual pockets
- Civic / administrative ward
- Imperial Palace exterior
- Imperial Palace interiors
- Industrial / infrastructure corridors
- Fringe / outer ward
- Bridges / canal network
- Major city gates / transitions
- atmosphere and FX
- occlusion requirements
- district completion packages

A checklist entry is **not complete because an asset file exists**. It is complete only after the asset is integrated into a representative gameplay scene and earns the production-completion score defined below.

---

# 3. Character Development Runs Simultaneously

At the same time, inspect the **Character Clothing & Accessory Production Checklist**.

World development must not advance by repeatedly placing an unfinished or mannequin-like base character into increasingly detailed scenes. Player characters and visible NPCs must be developed alongside the environment.

The character checklist governs:

- body/skin and face treatment
- production-quality Afro-descended hairstyles
- inner tops
- outerwear
- pants
- footwear
- belts/sashes
- weapons and scabbards
- charms, tags, pouches, cords, wraps, beads, and profession accessories
- eight-direction validation
- idle/walk/ready animation coverage
- district/profession clothing sets
- palette compliance
- material rendering
- runtime silhouette/readability
- world integration

**No presentation-quality gameplay preview may use bare/mannequin characters or placeholder clothing.**

---

# 4. Build Assets as Game Assets, Not Illustrations

The playable world must be made from modular, layered runtime elements rather than a single baked background.

A representative environment should support the appropriate combination of:

- ground
- decals / wear
- architecture
- architecture dressing
- props-back
- collision objects
- interactive objects
- actors
- props-front / occluders
- local shadows
- atmosphere / FX

Characters and NPCs must be able to move correctly in front of and behind appropriate objects. Tall architecture and organic scenery must use the locked occlusion/cutaway rules.

A beautiful standalone image is useful as concept/reference art, but it does **not** satisfy a runtime checklist item by itself.

---

# 5. Integrate Before Scoring

The primary review surface is the **integrated gameplay view**.

Do not score an isolated tree, roof, jacket, dock, or character layer as though it were automatically game-ready. Place it into a representative game scene and judge it alongside:

- the approved character art
- surrounding world materials
- architecture
- lighting
- shadows
- props
- occlusion
- clothing/equipment
- gameplay-scale readability

The Art Preview Review Rubric intentionally evaluates the game as a coherent image. An isolated asset that looks good but visibly breaks character/world homogeneity after integration remains unfinished.

---

# 6. Mandatory Rubric Gate

Every presentation candidate must be evaluated with the **Astro Fighters Art Preview Review Rubric**.

The rubric has two kinds of gates:

## Automatic failures

Automatic-failure conditions override the numeric total. Examples include lower-quality world art than character art, primitive/blockout scenery, mannequin characters, incomplete clothing, generic box architecture, baked gameplay backgrounds, visible grid rhythm, clashing pixel densities/styles, incorrect directional bodies, or unresolved occlusion problems.

If any automatic failure is present, continue development.

## Critical minimums

The following critical areas must satisfy their required minimums regardless of total score:

- Character / World Style Homogeneity
- Character Completion & Clothing
- Environment Pixel-Art Quality
- Astro Fighters World Identity
- Architectural Detail & Silhouette
- Projection, Depth & Occlusion

A high total does not compensate for failing a critical category.

---

# 7. Score Thresholds and Required Behavior

Use these thresholds as the operating contract:

| Result | Development behavior |
|---|---|
| **Below 36** | Continue development automatically. Do not stop to ask whether to keep working. |
| **36** | Still rework territory under the rubric; do not mark checklist items complete. Continue refinement unless the user specifically requests inspection of the intermediate state. |
| **37–41** | Conditional/internal test candidate only if there are no automatic failures and all critical minimums pass. Checklist items remain active. |
| **42–45** | Production approved. Relevant checklist items may be marked complete and struck through. |
| **46–50** | Lock-quality visual target. Relevant checklist items may be marked complete and used as reference quality for subsequent work. |

The completion threshold for both checklists is therefore **42+**, not merely “an asset exists” and not merely “the scene runs.”

---

# 8. Checklist Completion / Strike-Through Protocol

When a world or character checklist item earns **42 or above** in representative integrated gameplay, and all automatic/critical gates pass, update the corresponding checklist entry.

Preferred format:

```md
- [x] ~~Weathered dock planking~~ — 43/50, production approved
```

For a larger grouped item or district package, include enough context to make the completion auditable, for example:

```md
- [x] ~~Harbor crane / hoist set~~ — 44/50 integrated docks review, 2026-08-25
```

Do **not** strike through:

- isolated assets that have not been integrated
- temporary blockouts
- assets below 42
- assets associated with an automatic failure
- assets whose scene fails a critical minimum
- concept images used only as visual targets

If a previously approved asset later proves incompatible with the Master Art Direction or fails in a more representative integration test, reopen the checklist item and refine it.

---

# 9. Continuous Development Rule

Do not interrupt the user for routine continuation decisions.

When the current result fails the gate:

1. identify the lowest-scoring rubric categories and any automatic failures;
2. return to the Master Art Direction Prompt for the correct development approach;
3. inspect both checklists for the exact missing dependencies;
4. improve the assets and/or integration;
5. re-score the integrated view;
6. repeat until a valid test candidate or production-approved result exists.

The expected response to a failed art pass is **more development**, not “Should I continue?”

---

# 10. When to Inform the User That a Testable State Exists

A scene may be presented as an **internal test candidate** when it reaches the conditional range and passes all automatic/critical gates.

A scene should be presented as **production-approved art** only at **42+**.

When surfacing a testable state, provide:

- the integrated gameplay preview / playable build
- the rubric score
- critical-category scores
- any remaining known weaknesses
- which checklist items were newly completed
- which checklist items remain active

Do not describe a blockout or known placeholder scene as production quality.

---

# 11. New Chat / New Agent Handoff Procedure

A new session should perform the following sequence before producing new art or changing runtime code:

1. Confirm that `main` is the current authoritative repository state unless this README or `DEVELOPMENT_STATUS.md` explicitly identifies a newer active development branch.
2. Open this repository and read this `README.md`.
3. Read `AGENTS.md` and `PHASER_WORLD_REFACTOR_V0.md` in full.
4. Read `ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md` in full.
5. Read `IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md` and identify the active slice/queue position.
6. Read `Astro Fighters — Art Preview Review Rubric.md` in full.
7. Inspect `Astro Fighters — Imperial City Zone-by-Zone Asset Checklist.md` and identify:
   - already struck/approved items;
   - currently incomplete items;
   - dependencies for the next playable district or scene.
8. Inspect `ASTRO_FIGHTERS_CHARACTER_CLOTHING_ACCESSORY_CHECKLIST.md` and identify the corresponding incomplete character work.
9. Inspect the current playable files under `/docs` and the most recent integrated gameplay state.
10. Do **not** assume existing art is approved merely because it appears in the build. Checklist strike-through plus a qualifying rubric result is the approval signal.
11. Select the next world and character dependencies together from the active early-player production queue.
12. Develop according to the Master Art Direction Prompt and repository runtime instructions.
13. Integrate the work into the actual Phaser runtime.
14. Evaluate with the Art Preview Review Rubric.
15. Continue refining automatically if it fails.
16. At 42+, update/strike the completed items in both checklists as applicable.
17. Continue to the next dependencies.

This sequence is the default continuation workflow. A new chat should not restart game-architecture or art-direction discovery unless the user explicitly changes a locked rule.

---

# 12. Current Repository Roles

`/docs` contains the active public Phaser/open-world action-RPG playtest host, including the main runtime and `play-v4.html` entry point.

The root Markdown documents are production-control documents. They should remain readable and current because they are the primary handoff mechanism between sessions.

The private Unity Combat Strategy repository is legacy combat-reference material, not the active game runtime.

---

# 13. Core Locked Reminders

Keep these rules visible during every art pass:

- **`main` is the authoritative repository state unless a newer development branch is explicitly identified in this README or `DEVELOPMENT_STATUS.md`.**
- **Read and obey root `AGENTS.md` and `PHASER_WORLD_REFACTOR_V0.md` before world/runtime work.**
- **The world must match the quality and pixel-art style of the approved character models.**
- **Characters must be fully clothed and accessorized in presentation-quality previews.**
- **The hidden 32×32 square grid must not be visible to the player.**
- **Movement/facing supports eight directions.**
- **The game uses a flat-faced 3/4 cabinet projection.**
- **Playable environments are layered runtime constructions, not baked full-screen illustrations.**
- **Integrated gameplay review means an actual running Phaser-canvas view, not a collage/source composite.**
- **Imperial City must feel dense, lived-in, martial, analog-industrial, and distinctly Astro Fighters.**
- **The active early-player route is Harbor → Market → Residential/Canal → Academy.**
- **The Master Art Direction Prompt determines how to build.**
- **The early-player plan determines what to build first.**
- **The checklists determine what remains to build.**
- **The rubric determines whether the work is acceptable.**
- **Below the quality gate, keep working without asking for permission to continue.**
- **Only 42+ integrated, rubric-passing work is struck from the checklists as production complete.**

---

# Development Loop Summary

```text
CONFIRM AUTHORITATIVE REPOSITORY STATE (`main` unless superseded)
        ↓
READ AGENTS + GAME ARCHITECTURE + MASTER ART DIRECTION
        ↓
CHECK EARLY-PLAYER PRODUCTION QUEUE
        ↓
CHECK WORLD + CHARACTER CHECKLISTS
        ↓
SELECT NEXT DEPENDENCIES
        ↓
DEVELOP MATCHING PRODUCTION ASSETS
        ↓
INTEGRATE INTO PLAYABLE PHASER ACTION-RPG SCENE
        ↓
SCORE INTEGRATED VIEW WITH ART RUBRIC
        ↓
   PASS 42+? ── NO ──→ REFINE AUTOMATICALLY ──┐
        │                                      │
       YES                                     │
        ↓                                      │
STRIKE COMPLETED CHECKLIST ITEMS               │
        ↓                                      │
SELECT NEXT DEPENDENCIES ←─────────────────────┘
```

The goal is not to accumulate assets. The goal is to systematically produce a **homogeneous, production-quality Astro Fighters world and cast** in which every approved element has survived integrated gameplay review.