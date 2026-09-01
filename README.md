# Astro Fighters Playtest

Public runtime-only playtest host for Astro Fighters. The development repository remains separate/private. The playable build is published from `/docs` via GitHub Pages.

This repository also serves as the **art-development control surface and handoff record** for Imperial City production. A new chat session or development agent should be able to open this repository, read the documents below in order, inspect checklist progress, and continue work without restarting the art-direction discussion.

---

# Art Development Workflow — READ THIS FIRST

Astro Fighters art development is **source-driven, checklist-driven, and rubric-gated**. Do not improvise a new visual direction and do not treat technically functional placeholder art as production art.

The required operating sequence is:

> **MASTER ART DIRECTION → SOURCE-LAYER INTEGRITY RULES → CHECK BOTH ASSET CHECKLISTS → DEVELOP → SOURCE QA → INTEGRATE IN GAME → SCORE WITH RUBRIC → REFINE OR MARK COMPLETE → CONTINUE**

The five controlling documents on `main` are:

1. [`ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md`](./ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md) — **HOW to develop the art.**
2. [`ASTRO_FIGHTERS_MODULAR_SOURCE_LAYER_INTEGRITY_RULES.md`](./ASTRO_FIGHTERS_MODULAR_SOURCE_LAYER_INTEGRITY_RULES.md) — **HOW modular source layers must be authored and QA'd; visibility slices and occlusion-boundary clipping are automatic failures.**
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

# 1A. Modular Source Layer Integrity Is a Separate Mandatory Gate

Immediately after the Master Art Direction Prompt, read **`ASTRO_FIGHTERS_MODULAR_SOURCE_LAYER_INTEGRITY_RULES.md`** before creating or approving modular character/clothing/equipment source art.

The critical distinction is:

> **Visibility is not geometry. An occluder may hide a source component; it may not define where that component ends.**

A layer is not production-ready merely because the dressed composite reconstructs perfectly. Pants must continue beneath sashes and weapons, sleeves must continue to their real cuff/opening edges, haori near/far pieces must be coherent garment pieces rather than sparse visible fragments, and equipment must continue behind the body/garment according to its physical mount.

**Machine reconstruction PASS + clipped or fragmented standalone layers = SOURCE FAIL.**

Every modular package requires individual-layer review and the occluder-toggle test before it can be called `SOURCE PASS` or unblock the next direction.

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

For modular source art, **do not cut the visible fragments out of a finished illustration and call those fragments the production layers**. Use the finished illustration as a dressed visual authority, then author complete reusable component geometry under overlaps according to the Source Layer Integrity Rules.

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

For modular-source systems, integrated scoring occurs **after** the source package has already passed the standalone component-integrity gate. Integrated appearance cannot retroactively excuse clipped source components.

---

# 6. Mandatory Rubric Gate

Every presentation candidate must be evaluated with the **Astro Fighters Art Preview Review Rubric**.

The rubric has two kinds of gates:

## Automatic failures

Automatic-failure conditions override the numeric total. Examples include lower-quality world art than character art, primitive/blockout scenery, mannequin characters, incomplete clothing, generic box architecture, baked gameplay backgrounds, visible grid rhythm, clashing pixel densities/styles, incorrect directional bodies, unresolved occlusion problems, or modular source layers known to be clipped/fragmented.

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

For a modular character package, the numeric gameplay rubric does not replace the source-layer integrity gate: the source must first earn `SOURCE PASS` under the Source Layer Integrity Rules.

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
- modular packages whose individual layers contain clipped visibility slices or have not passed component-integrity/occluder-toggle QA

If a previously approved asset later proves incompatible with the Master Art Direction or fails in a more representative integration test, reopen the checklist item and refine it.

---

# 9. Continuous Development Rule

Do not interrupt the user for routine continuation decisions.

When the current result fails the gate:

1. identify the lowest-scoring rubric categories and any automatic failures;
2. return to the Master Art Direction Prompt and Source Layer Integrity Rules for the correct development approach;
3. inspect both checklists for the exact missing dependencies;
4. improve the assets and/or integration;
5. rerun source-layer integrity QA when modular source art changed;
6. re-score the integrated view;
7. repeat until a valid test candidate or production-approved result exists.

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

Do not describe a blockout, known placeholder scene, exact-composite-only modular stack, or clipped-layer package as production quality.

---

# 11. New Chat / New Agent Handoff Procedure

A new session should perform the following sequence before producing new art:

1. Open this repository and read this `README.md`.
2. Read `ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md` in full.
3. Read `ASTRO_FIGHTERS_MODULAR_SOURCE_LAYER_INTEGRITY_RULES.md` in full before creating or approving modular source art.
4. Read `Astro Fighters — Art Preview Review Rubric.md` in full.
5. Inspect `Astro Fighters — Imperial City Zone-by-Zone Asset Checklist.md` and identify:
   - already struck/approved items;
   - currently incomplete items;
   - dependencies for the next playable district or scene.
6. Inspect `ASTRO_FIGHTERS_CHARACTER_CLOTHING_ACCESSORY_CHECKLIST.md` and identify the corresponding incomplete character work.
7. Inspect the current playable files under `/docs` and the most recent integrated gameplay state.
8. Do **not** assume existing art is approved merely because it appears in the build. Checklist strike-through plus qualifying source-integrity and rubric results are the approval signals.
9. Select the next world and character dependencies together.
10. Develop according to the Master Art Direction Prompt and Source Layer Integrity Rules.
11. For modular source packages, review every layer alone and run the occluder-toggle test before runtime reduction.
12. Integrate accepted source/runtime work into gameplay.
13. Evaluate with the Art Preview Review Rubric.
14. Continue refining automatically if it fails.
15. At 42+, update/strike the completed items in both checklists as applicable.
16. Continue to the next dependencies.

This sequence is the default continuation workflow. A new chat should not restart art-direction discovery unless the user explicitly changes a locked rule.

---

# 12. Current Repository Roles

`/docs` contains the public playtest host. At the time this README was formalized it contains the published runtime files, including the main playtest page and a `play-v4.html` entry point.

The root Markdown documents are production-control documents. They should remain readable and current because they are the primary handoff mechanism between sessions.

The development repository remains separate/private; this repository is the public playtest and art-production handoff surface.

---

# 13. Core Locked Reminders

Keep these rules visible during every art pass:

- **The world must match the quality and pixel-art style of the approved character models.**
- **Characters must be fully clothed and accessorized in presentation-quality previews.**
- **The hidden 32×32 square grid must not be visible to the player.**
- **Movement/facing supports eight directions.**
- **The game uses a flat-faced 3/4 cabinet projection.**
- **Playable environments are layered runtime constructions, not baked full-screen illustrations.**
- **Modular source layers must describe complete components, not visible fragments clipped at occlusion boundaries.**
- **Exact composite reconstruction alone is never `SOURCE PASS`.**
- **Individual-layer review and occluder-toggle QA are mandatory before a modular direction/package can pass.**
- **Imperial City must feel dense, lived-in, martial, analog-industrial, and distinctly Astro Fighters.**
- **The Master Art Direction Prompt determines how to build.**
- **The Source Layer Integrity Rules determine whether modular source geometry is actually reusable.**
- **The checklists determine what remains to build.**
- **The rubric determines whether the integrated work is acceptable.**
- **Below the quality gate, keep working without asking for permission to continue.**
- **Only 42+ integrated, rubric-passing work with all prerequisite source gates passed is struck from the checklists as production complete.**

---

# Development Loop Summary

```text
READ MASTER ART DIRECTION
        ↓
READ SOURCE-LAYER INTEGRITY RULES
        ↓
CHECK WORLD + CHARACTER CHECKLISTS
        ↓
SELECT NEXT DEPENDENCIES
        ↓
DEVELOP MATCHING PRODUCTION ASSETS
        ↓
INDIVIDUAL-LAYER + OCCLUDER-TOGGLE SOURCE QA
        ↓
   SOURCE PASS? ── NO ──→ FIX SOURCE GEOMETRY ──┐
        │                                        │
       YES                                       │
        ↓                                        │
INTEGRATE INTO PLAYABLE PHASER SCENE             │
        ↓                                        │
SCORE INTEGRATED VIEW WITH ART RUBRIC             │
        ↓                                        │
   PASS 42+? ── NO ──→ REFINE AUTOMATICALLY ─────┤
        │                                        │
       YES                                       │
        ↓                                        │
STRIKE COMPLETED CHECKLIST ITEMS                  │
        ↓                                        │
SELECT NEXT DEPENDENCIES ←────────────────────────┘
```

The goal is not to accumulate assets. The goal is to systematically produce a **homogeneous, production-quality Astro Fighters world and cast** in which every approved element has survived source-layer integrity review and integrated gameplay review.