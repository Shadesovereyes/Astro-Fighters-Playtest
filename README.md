# Astro Fighters Playtest

Public runtime-only playtest host for Astro Fighters. The development repository remains separate/private. The playable build is published from `/docs` via GitHub Pages.

This repository also serves as the **art-development control surface and handoff record** for Imperial City production. A new chat session or development agent should be able to open this repository, read the documents below in order, inspect checklist progress, and continue work without restarting the art-direction discussion.

---

# Art Development Workflow — READ THIS FIRST

Astro Fighters art development is **reference-guided, source-driven, checklist-driven, and rubric-gated**. Do not improvise a new visual direction and do not treat technically functional placeholder art as production art.

The required operating sequence is:

> **MASTER ART DIRECTION → REFERENCE / GAME-ASSET CLASSIFICATION → PIXEL SOURCE STANDARD → SOURCE-LAYER INTEGRITY RULES → CHECK BOTH ASSET CHECKLISTS → DEVELOP → SOURCE QA → INTEGRATE IN GAME → SCORE WITH RUBRIC → REFINE OR MARK COMPLETE → CONTINUE**

The six controlling documents on this branch are:

1. [`ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md`](./ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md) — **HOW to develop the art.**
2. [`ASTRO_FIGHTERS_PIXEL_ART_SOURCE_STANDARD.md`](./ASTRO_FIGHTERS_PIXEL_ART_SOURCE_STANDARD.md) — **WHERE polished reference illustration is allowed and WHERE true pixel art becomes mandatory for source/runtime/in-game assets.**
3. [`ASTRO_FIGHTERS_MODULAR_SOURCE_LAYER_INTEGRITY_RULES.md`](./ASTRO_FIGHTERS_MODULAR_SOURCE_LAYER_INTEGRITY_RULES.md) — **HOW modular production layers must be authored and QA'd; visibility slices and occlusion-boundary clipping are automatic failures.**
4. [`Astro Fighters — Imperial City Zone-by-Zone Asset Checklist.md`](./Astro%20Fighters%20%E2%80%94%20Imperial%20City%20Zone-by-Zone%20Asset%20Checklist.md) — **WHAT world/scenery assets remain to be developed.**
5. [`ASTRO_FIGHTERS_CHARACTER_CLOTHING_ACCESSORY_CHECKLIST.md`](./ASTRO_FIGHTERS_CHARACTER_CLOTHING_ACCESSORY_CHECKLIST.md) — **WHAT character clothing, hair, equipment, and accessory work remains to be developed in parallel.**
6. [`Astro Fighters — Art Preview Review Rubric.md`](./Astro%20Fighters%20%E2%80%94%20Art%20Preview%20Review%20Rubric.md) — **WHEN an integrated result is good enough to test or mark production-complete.**

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

# 1A. Reference Material and In-Game Assets Are Different Asset Classes

Astro Fighters may use **polished illustration, cel-shaded art, painted turnarounds, anatomy studies, garment studies, material studies, equipment studies, and presentation-quality concept art as reference material**.

That is allowed and useful.

The critical rule is:

> **POLISHED ILLUSTRATION IS ALLOWED FOR REFERENCE. ANYTHING IDENTIFIED FOR ACTUAL GAME USE MUST BE TRUE PIXEL ART.**

Reference material may establish:

- character identity and Afro-feature treatment;
- anatomy and proportions;
- garment construction and hidden geometry;
- directional pose and silhouette;
- weapon/equipment mounting;
- material and color relationships;
- the quality target that production pixel art must match.

Reference material must be identified as **`REFERENCE ONLY`** or **`REFERENCE PASS`**. It is not a sprite/source/runtime/game asset merely because it is transparent, sits on a checkerboard, has filenames printed on it, is labeled `480×640`, or resembles a sprite sheet.

The moment an asset is identified as `SOURCE CANDIDATE`, `PIXEL SOURCE`, `SOURCE PASS`, `RUNTIME CANDIDATE`, `RUNTIME PASS`, `IN-GAME`, `PHASER ASSET`, or is intended to be loaded by gameplay, it must satisfy `ASTRO_FIGHTERS_PIXEL_ART_SOURCE_STANDARD.md`.

Do **not** promote illustration to game art by cropping, shrinking, palette quantization, a pixelation filter, or cutting its visible parts into transparent PNGs. The reference guides a separately authored pixel asset.

---

# 1B. Modular Source Layer Integrity Is a Separate Mandatory Gate

Immediately after the Pixel-Art Source Standard, read **`ASTRO_FIGHTERS_MODULAR_SOURCE_LAYER_INTEGRITY_RULES.md`** before creating or approving modular character/clothing/equipment source art.

The critical distinction is:

> **Visibility is not geometry. An occluder may hide a source component; it may not define where that component ends.**

A layer is not production-ready merely because the dressed composite reconstructs perfectly. Pants must continue beneath sashes and weapons, sleeves must continue to their real cuff/opening edges, haori near/far pieces must be coherent garment pieces rather than sparse visible fragments, and equipment must continue behind the body/garment according to its physical mount.

**Machine reconstruction PASS + clipped or fragmented standalone layers = SOURCE FAIL.**  
**Component integrity PASS + non-pixel production rendering = SOURCE FAIL.**

Every modular package requires individual-layer review, pixel-source review, and the occluder-toggle test before it can be called `SOURCE PASS` or unblock the next direction.

---

# 2. World Development Uses the Zone-by-Zone Checklist

After reading the controlling art standards, inspect the **Imperial City Zone-by-Zone Asset Checklist**.

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

A polished illustrated fighter reference may be used to guide the character package. The fighter that appears in actual gameplay must be the approved pixel-art runtime asset, not the illustration.

---

# 4. Build Game Assets as Pixel Assets; Use Illustration as Reference

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

For modular source art, **do not cut the visible fragments out of a finished illustration and call those fragments the production layers**. Use the finished illustration as a dressed visual authority, then author complete reusable component geometry in true pixel art under overlaps according to the Source Layer Integrity Rules and Pixel-Art Source Standard.

A beautiful standalone image is useful as concept/reference art, but it does **not** satisfy a source, runtime, or gameplay checklist item by itself.

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

For modular-source systems, integrated scoring occurs **after** the source package has already passed pixel-source and standalone component-integrity gates. Integrated appearance cannot retroactively excuse clipped source components or non-pixel production rendering.

---

# 6. Mandatory Rubric Gate

Every presentation candidate must be evaluated with the **Astro Fighters Art Preview Review Rubric**.

The rubric has two kinds of gates:

## Automatic failures

Automatic-failure conditions override the numeric total. Examples include lower-quality world art than character art, primitive/blockout scenery, mannequin characters, incomplete clothing, generic box architecture, baked gameplay backgrounds, visible grid rhythm, clashing pixel densities/styles, incorrect directional bodies, unresolved occlusion problems, modular source layers known to be clipped/fragmented, or non-pixel/painterly art being used as an actual gameplay asset.

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

For a modular character package, the numeric gameplay rubric does not replace the source gates: production source must first earn `PIXEL SOURCE PASS` and `COMPONENT INTEGRITY PASS`, then `SOURCE PASS`, before downstream runtime promotion.

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
- concept/reference images used only as visual targets
- illustrative/painterly art that has not been re-authored as production pixel art
- modular packages whose individual layers contain clipped visibility slices or have not passed component-integrity/occluder-toggle QA
- modular packages that have not passed the Pixel-Art Source Standard

If a previously approved asset later proves incompatible with the Master Art Direction or fails in a more representative integration test, reopen the checklist item and refine it.

---

# 9. Continuous Development Rule

Do not interrupt the user for routine continuation decisions.

When the current result fails the gate:

1. identify the lowest-scoring rubric categories and any automatic failures;
2. return to the Master Art Direction Prompt, Pixel-Art Source Standard, and Source Layer Integrity Rules for the correct development approach;
3. confirm whether the current file is `REFERENCE ONLY`, production `SOURCE`, or `RUNTIME` so the correct standards are applied;
4. inspect both checklists for the exact missing dependencies;
5. improve the assets and/or integration;
6. rerun pixel-source and source-layer integrity QA when production source art changed;
7. re-score the integrated view;
8. repeat until a valid test candidate or production-approved result exists.

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

Do not describe a reference illustration, blockout, known placeholder scene, exact-composite-only modular stack, clipped-layer package, or non-pixel production candidate as production quality.

---

# 11. New Chat / New Agent Handoff Procedure

A new session should perform the following sequence before producing new art:

1. Open this repository and read this `README.md`.
2. Read `ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md` in full.
3. Read `ASTRO_FIGHTERS_PIXEL_ART_SOURCE_STANDARD.md` in full and preserve the distinction between illustrative **REFERENCE** material and pixel-authored **SOURCE/RUNTIME/IN-GAME** assets.
4. Read `ASTRO_FIGHTERS_MODULAR_SOURCE_LAYER_INTEGRITY_RULES.md` in full before creating or approving modular source art.
5. Read `Astro Fighters — Art Preview Review Rubric.md` in full.
6. Inspect `Astro Fighters — Imperial City Zone-by-Zone Asset Checklist.md` and identify:
   - already struck/approved items;
   - currently incomplete items;
   - dependencies for the next playable district or scene.
7. Inspect `ASTRO_FIGHTERS_CHARACTER_CLOTHING_ACCESSORY_CHECKLIST.md` and identify the corresponding incomplete character work.
8. Inspect the current playable files under `/docs` and the most recent integrated gameplay state.
9. Do **not** assume existing art is approved merely because it appears in the build or because a polished image is labeled like a sprite sheet. Checklist strike-through plus qualifying pixel-source, source-integrity, and rubric results are the approval signals.
10. Classify each active visual file correctly as `REFERENCE ONLY`, `REFERENCE PASS`, `SOURCE CANDIDATE`, `SOURCE PASS`, `RUNTIME CANDIDATE`, `RUNTIME PASS`, or `IN-GAME`.
11. Select the next world and character dependencies together.
12. Develop according to the Master Art Direction Prompt, Pixel-Art Source Standard, and Source Layer Integrity Rules.
13. For modular production source packages, review every layer alone, inspect true pixel construction, and run the occluder-toggle test before runtime reduction.
14. Integrate accepted runtime work into gameplay.
15. Evaluate with the Art Preview Review Rubric.
16. Continue refining automatically if it fails.
17. At 42+, update/strike the completed items in both checklists as applicable.
18. Continue to the next dependencies.

This sequence is the default continuation workflow. A new chat should not restart art-direction discovery unless the user explicitly changes a locked rule.

---

# 12. Current Repository Roles

`/docs` contains the public playtest host. At the time this README was formalized it contains the published runtime files, including the main playtest page and a `play-v4.html` entry point.

The root Markdown documents are production-control documents. They should remain readable and current because they are the primary handoff mechanism between sessions.

The development repository remains separate/private; this repository is the public playtest and art-production handoff surface.

Reference and production imagery should be kept visibly distinct in paths/metadata where practical:

- `reference/` — polished visual authorities/studies; may be illustrative;
- `source/` — pixel-authored production masters and modular layers;
- established runtime/Phaser asset paths — manually cleaned game-resolution pixel assets.

---

# 13. Core Locked Reminders

Keep these rules visible during every art pass:

- **Polished illustration / cel-shaded art is allowed for REFERENCE material.**
- **Anything identified for source, runtime, Phaser, or in-game usage must be true pixel art.**
- **Reference art guides production pixel art; it is not converted into production merely by cropping, shrinking, filtering, or quantization.**
- **The world must match the quality and pixel-art style of the approved character models.**
- **Characters must be fully clothed and accessorized in presentation-quality gameplay previews.**
- **The hidden 32×32 square grid must not be visible to the player.**
- **Movement/facing supports eight directions.**
- **The game uses a flat-faced 3/4 cabinet projection.**
- **Playable environments are layered runtime constructions, not baked full-screen illustrations.**
- **Modular source layers must describe complete components, not visible fragments clipped at occlusion boundaries.**
- **Exact composite reconstruction alone is never `SOURCE PASS`.**
- **Individual-layer review, pixel-source review, and occluder-toggle QA are mandatory before a modular direction/package can pass.**
- **Imperial City must feel dense, lived-in, martial, analog-industrial, and distinctly Astro Fighters.**
- **The Master Art Direction Prompt determines the visual direction.**
- **The Pixel-Art Source Standard determines when reference rendering must become production pixel art.**
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
CLASSIFY CURRENT ART
REFERENCE ONLY / REFERENCE PASS / SOURCE / RUNTIME
        ↓
REFERENCE MATERIAL? ── YES ──→ POLISHED ILLUSTRATION ALLOWED
        │                              ↓
        │                    USE AS DESIGN AUTHORITY
        │                              ↓
        └────────────────────→ AUTHOR TRUE PIXEL SOURCE
                                       ↓
READ PIXEL-ART SOURCE STANDARD
        ↓
READ SOURCE-LAYER INTEGRITY RULES
        ↓
CHECK WORLD + CHARACTER CHECKLISTS
        ↓
SELECT NEXT DEPENDENCIES
        ↓
DEVELOP MATCHING PIXEL PRODUCTION ASSETS
        ↓
PIXEL-SOURCE + INDIVIDUAL-LAYER + OCCLUDER-TOGGLE QA
        ↓
   SOURCE PASS? ── NO ──→ FIX PIXELS / SOURCE GEOMETRY ──┐
        │                                                 │
       YES                                                │
        ↓                                                 │
DERIVE / CLEAN RUNTIME PIXELS                             │
        ↓                                                 │
INTEGRATE INTO PLAYABLE PHASER SCENE                     │
        ↓                                                 │
SCORE INTEGRATED VIEW WITH ART RUBRIC                    │
        ↓                                                 │
   PASS 42+? ── NO ──→ REFINE AUTOMATICALLY ─────────────┤
        │                                                 │
       YES                                                │
        ↓                                                 │
STRIKE COMPLETED CHECKLIST ITEMS                          │
        ↓                                                 │
SELECT NEXT DEPENDENCIES ←────────────────────────────────┘
```

The goal is not to accumulate assets. The goal is to systematically produce a **homogeneous, production-quality Astro Fighters world and cast** in which polished reference material guides — but never masquerades as — the actual pixel-authored game assets, and every approved production element has survived pixel-source review, source-layer integrity review, and integrated gameplay review.
