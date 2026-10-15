# Astro Fighters Web Testbed — Session Log

**Date:** 2026-08-05  
**Branch:** `claude/astrofighters-test-version-p1sw5a`  
**Scope:** Make the headless 2-D core playable, package it for chat testing, and repair release-blocking functionality and UX gaps found through user testing.

## Starting point

The branch had a strong DOM-free `web/af-core.js` with chart calculation, hex movement/LoS, combat resolution, AI personas, and a PVE enemy roster. The working browser artifact was still the older 1-D page. The 2-D core was not connected to a complete UI.

## Work completed

### 1. First 2-D browser wiring

Created the first `web/astro-fighters-2d.html` with:

- Birth-chart setup and chart-derived loadout preview.
- Manual UTC-offset selection.
- SVG hex arena, generated terrain, movement planning, LoS hover line, HUD, queue, and combat log.
- PVE enemy selection and existing archetype AI.

**User-found defect:** the downloadable page depended on a sibling `af-core.js`, so the chat-delivered file reported “engine failed to load.”

**Response:** stopped treating HTML syntax as sufficient validation, created a self-contained standalone package, and added a deterministic headless smoke test covering chart/loadout creation, terrain, LoS, movement, AI planning, and repeated round resolution.

### 2. Movement and training corrections

**User-found defects:** movement selection appeared nonfunctional, and the setup limited the player to one martial art.

Root causes and fixes:

- The SVG was being rebuilt during hover, replacing the element before a stable click could finish. Hover now changes the existing polygon instead of rebuilding the arena.
- Added a planned-move ghost token and route line.
- Allowed multiple trained martial styles.
- Preserved mutual exclusivity at the stance level rather than at character creation.
- Deduplicated shared techniques such as Clinch while retaining all valid parent styles.
- Added regression coverage for a real coordinate change and multi-style loadout construction.

This became the V2 candidate.

### 3. Functional and UX audit / V3 rebuild

**User-found blockers:** universal actions appeared missing, the ability list was poorly organized, dependency actions caused option overload, and level selection was absent.

The V3 rebuild added:

- Permanent Focus rail for Catch Breath and Charge Chakra.
- Category tabs, authored-source filters, search, contextual counts, and grouped ability panels.
- Parent-child dependency behavior for martial stances, weapon stances, eyes, grapples, and mounts.
- Queue-order validation and cascading removal of invalid dependents.
- Engine-side rejection of martial/weapon children without their active stance.
- Canonical level milestones from L1 through L100.
- 1v1, 2v2, and three-way FFA scenarios.
- Movement-only rounds.
- Expanded balance/debug controls.
- A written V3 functional/UX audit and manual acceptance checklist.
- A deterministic repository-target smoke test.

The older implementation specification had intentionally skipped leveling for the vertical slice. V3 instead follows the current progression document while retaining a force-unlock override for catalog testing.

### 4. Map readability pass

**User request:** occupied hexagons and LoS-blocking terrain needed to alter or highlight their tiles so the battle map could be read quickly.

Implemented:

- Cyan occupied tile and center ring for the player.
- Green occupied tile and center ring for allied NPCs.
- Red occupied tile and center ring for hostile NPCs.
- Violet tile treatment for terrain that blocks sight but permits movement.
- Orange tile treatment for terrain that blocks both movement and sight.
- Compact legend above the arena.
- Reachable and selected-movement treatments remain visually dominant when applicable.

### 5. LoS action enforcement and stance reveal

**User-found defects:** blocked ranged actions appeared to shoot through terrain, and queueing a stance did not reliably expose its child abilities.

**Correction:**

- Exhaustive geometry tests confirmed the hex LoS algorithm itself was correct.
- Found and removed hidden player auto-approach during action resolution; players now attack only from their explicitly selected movement destination.
- Added projected-position LoS/range validation and clear rejection logs.
- Queueing a martial or weapon stance now opens the matching category/source panel and clears filters that concealed its children.
- The latest queued stance is the projected active stance, preserving martial/weapon exclusivity.
- Added `af-v3.2.smoke.js` for blocker enforcement and stance-child visibility.

## Files created or materially changed during the session

- `web/astro-fighters-2d.html`
- `web/astro-fighters-2d-v2.html`
- `web/astro-fighters-2d-v3.html`
- `web/astro-fighters-2d-v3.1.html`
- `web/astro-fighters-2d-v3.4.html`
- `web/af-map-v3.js`
- `web/af-progression-v3.js`
- `web/af-core-v3-patch.js`
- `web/af-ui-v3.js`
- `web/af-page-v3.js`
- `web/af-core.smoke.js`
- `web/af-v2-regression.js` and related V2 regression artifacts
- `web/af-v3.smoke.js`
- `web/af-v3.4.smoke.js`
- `web/ASTRO_FIGHTERS_2D_V3_AUDIT.md`
- `web/HANDOFF.md`
- `web/SESSION_LOG_2026-08-05.md`

The exact V2 auxiliary filenames should be treated as historical references; V3.4 is the only current candidate.

## Validation performed

- JavaScript syntax checks for page/controller and V3 modules.
- Deterministic chart and level-profile tests.
- Universal Focus-action count and visibility contract.
- Martial/weapon/eye dependency visibility and queue ordering.
- Engine-side stance enforcement.
- Movement-only and planned movement resolution.
- Multi-combatant scenario resolution.
- Deterministic full battles to a clean result.
- Standalone packaging with no external scripts.
- Static duplicate-ID audit.
- Static map-readability assertions for occupied and blocking tile treatments, redraw observation, and current script wiring.
- Exhaustive LoS geometry checks and blocked-action regression coverage.
- Fog-of-war visibility checks across movement, awareness, Stealth, and allies.
- Canonical L1/L20/L100 stat budgets, escalating cost boundaries, auto-allocation, level-down trimming, and canonical player-stat injection into combat.

## Current recommendation

Use `web/astro-fighters-2d-v3.4.html` as the only active candidate. Keep the older 1-D page published and preserve V1/V2 as references until V3.4 passes the manual browser acceptance checklist in `web/ASTRO_FIGHTERS_2D_V3_AUDIT.md`.

## Remaining risks and gaps

- Browser interaction has not been fully automated in the available runtime.
- Explicit action target selection is still simplified.
- Historical timezone handling and the full city database remain incomplete.
- North Node, Decan/Dwad effects, morality morphs, transit effects, and eye stage-passives remain unauthored or deferred.
- NPC opponent levels/stat budgets are not independently selectable in the web setup.

### 6. Perception-based fog of war

**User-found defect:** combat LoS correctly rejected blocked attacks, but the SVG battle map still rendered every living hostile, including opponents behind terrain.

**Correction:**

- Added an active-battle tracking wrapper in `af-map-v3.js`.
- Hostile map tokens now render only when `Battle.perceives(player, hostile)` succeeds.
- Hidden hostiles no longer produce faction-colored occupied tiles or occupant rings.
- Visibility recalculates after every arena redraw, including player and NPC movement.
- Added `af-v3.3.smoke.js` covering terrain occlusion, reveal after movement, re-hide after returning behind cover, awareness range, Stealth, and ally visibility.

### 7. Canonical level and attribute allocation

**User-found defect:** changing fighter level altered chart-kit unlocks but did not alter the attribute-point allowance; the form still required five raw attributes to total exactly 44.

**Root cause:** the early V3 web setup retained a temporary fixed-sum test rule. The Unity source already defines the intended system in `BalanceConfig`, `StatCosts`, and `BattlePrototypeUI`:

- Each attribute has a base value of 6.
- Level 1 grants 14 spendable points.
- Each level after 1 grants 5 more points.
- Point costs escalate by current stat value: 1 below 20, 2 below 30, 3 below 40, 4 below 50, and 5 thereafter.

**Correction:**

- Ported the canonical budget and cost curve into `AF.BAL` / `AFUI`.
- Added `af-progression-v3.js`, which replaces the visible fixed-44 form with the canonical budget allocator. As a compatibility bridge, it satisfies the legacy controller check with a temporary 44-sum proxy, then injects the real canonical stats into the player fighter at creation.
- Added points-spent, total-budget, remaining/overspent, and per-stat next-cost feedback.
- Added **Auto-spend evenly** and **Reset to base 6** controls.
- Lowering level automatically trims the most expensive/highest purchased points until the allocation is legal.
- Raising level increases available points without silently rewriting a customized build.
- Added `af-v3.4.smoke.js`, covering L1/L20/L100 budgets, every cost threshold, maximum-stat cost, auto-allocation, level-down trimming, and removal of the old fixed-44 rule.
- Re-ran the full-battle, LoS, stance, and fog-of-war regressions successfully.
