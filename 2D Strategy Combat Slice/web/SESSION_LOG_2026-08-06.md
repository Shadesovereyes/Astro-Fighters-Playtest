# Astro Fighters Web Testbed — Session Log

**Date:** 2026-08-06
**Branch:** `claude/astrofighters-test-version-p1sw5a` (continued from the cleanup commit `9f4aa89`)
**Scope:** Continue V3.4 development from the cleanup commit — run the standing manual browser acceptance checklist, now that browser automation is available, and fix any real defect found in place without recreating the version-file accumulation problem.

## Starting point

The repository was at the first-cleanup commit: `web/index.html` redirects to
`web/astro-fighters-2d-v3.4.html`, backed by the six split runtime modules
(`af-core.js`, `af-core-v3-patch.js`, `af-ui-v3.js`, `af-page-v3.js`, `af-map-v3.js`,
`af-progression-v3.js`) and the two smoke suites (`af-core.smoke.js`,
`af-v3.4.smoke.js`). Both suites were green. The standing blocker across prior sessions
was that "full browser interaction automation has not been available," leaving manual
browser acceptance unperformed.

## Browser acceptance is now possible

This environment ships Chromium at `/opt/pw-browsers/chromium`. Installing
`playwright-core` out of tree and pointing `executablePath` at that binary drives the
`file://` build directly. A scratchpad acceptance driver walked the audit's manual
checklist as automated interaction:

- Level 1/10/15/20 unlock profiles and level-scaled stat budgets (14 at L1, +5/level).
- Auto-spend / reset-to-base allocator controls (auto-spend leaves no *affordable*
  point; a leftover that costs more than the remaining budget is expected by design).
- Two pinned Focus actions (Catch Breath, Charge Chakra) visible under every filter.
- Martial stance panel: stance shown, children gated, stance-queue reveal, dependent
  cascade on stance removal.
- Ability search/category/source filters reducing the list predictably.
- Movement-only round resolution from a selected reachable hex.
- Occupied-cell and soft/hard LoS-blocker tile treatments plus the five-item legend.
- All three scenarios (1v1, 2v2, 3-way FFA) starting and resolving with **zero console
  errors**.

Final run: **31/31 checks, 0 console errors.**

This is automated interaction, which is stronger than headless Node validation but is
**not** a substitute for a human walking the checklist. V3.4 must not be promoted to the
published artifact on the strength of the automated pass alone.

## Defect found and fixed — trained martial styles produced no abilities

The first automated pass surfaced a real regression: with a martial style selected, the
Martial category count was 0 and the built loadout contained no stances or techniques.

**Root cause.** The V3.4 page builds loadouts via `AFUI.buildPlayerAbilities`, which
calls `AF.buildLoadout({ martials: [...] })` (plural array). The `af-core-v3-patch.js`
override reads `opt.martials` correctly, but it first delegates to the original
`AF.buildLoadout`, and the core only honored a singular `opt.martial` string. The array
was therefore ignored and no martial abilities were ever added; the patch then annotated
an empty set. `af-core.smoke.js` did not catch this because it passes the singular
`martial: "MuayThai"` argument, which the core still handled.

**Fix.** `af-core.js` `buildLoadout` now normalizes both the plural `martials` array and
the legacy singular `martial` key, and de-duplicates repeated style keys before pushing
each style's stance and moves. The V3 patch's existing shared-technique merge (e.g.
Clinch appearing under multiple styles) is unchanged and still collapses duplicates to a
single multi-parent card.

**Regression coverage.** `af-v3.4.smoke.js` was extended (not duplicated) with a focused
block that builds a two-style + weapon loadout through the real page path and asserts:
both stances present with correct `styleKey`/tag/category, per-style techniques present,
shared Clinch de-duplicated to one card listing both parents, weapon stance present,
single-style selection also works, and a technique is dependency-gated before its stance
is queued and revealed after. It fails against the pre-fix core and passes after.

## Validation performed

- `node af-core.smoke.js` — green (singular-`martial` path preserved).
- `node af-v3.4.smoke.js` — green, including the new martial-style regression.
- Headless engine check: pure-AI 2v2 resolves in 8/8 seeds (8–18 rounds), confirming the
  automated harness's earlier "team undecided" result was a passive-player harness
  artifact, not an engine stalemate.
- Automated browser acceptance: 31/31 checks, 0 console errors, martial stance panel
  confirmed rendering live (Boxing Stance visible, 6 techniques revealed on queue,
  cascade on removal).

## What was intentionally NOT done

- No new versioned HTML page; the fix is in the active core runtime file.
- No duplicate smoke suite; the existing V3.4 suite was extended.
- The browser acceptance driver was **not** committed — it needs an out-of-tree
  `playwright-core` install. The technique is documented in `HANDOFF.md` for reuse.
- The six modules were not merged; cleanup remains separable from gameplay fixes until
  human acceptance passes.

## Remaining risks and gaps (unchanged)

- Human manual browser acceptance is still recommended before promoting the artifact.
- Explicit combat target selection and ground-targeted AoE remain simplified.
- NPC levels/attribute budgets are not independently selectable in the web setup.
- Historical timezone/DST handling and the city database remain incomplete.
- North Node ultimate, Decan/Dwad effects, morality morphs, transit modifiers, and eye
  stage-passives remain unauthored or deferred.

## Follow-up — combat-log copy and Focus-aware action planning

After a manual test (1v1 duel, level 10) confirmed the martial fix in live play, two
usability changes were requested and implemented in the active runtime files:

1. **Copy combat log.** Added a "Copy log" button to the combat-log panel
   (`astro-fighters-2d-v3.4.html` + `af-page-v3.js` `copyLog`). It copies the
   tag-stripped log with the clipboard API and an `execCommand` textarea fallback (the
   published artifact runs in a sandboxed iframe where the async clipboard API can be
   blocked), and flashes "Copied!" for feedback.

2. **Focus restores fund later queued actions.** Previously the affordability gate
   (`AFUI.lockReason`) summed gross queue costs against current resources, so it blocked
   planning a Catch Breath -> expensive-move combo even though the engine resolves it
   fine (restores apply mid-round via `af-core.js` `applyResource`). `lockReason` now
   runs an order-aware simulation (`actionCost`, `selfRestore`, `queueResourceState`)
   that credits each queued action's self-targeted Stamina/Chakra restore, capped at the
   player's maxima, before testing the next action. Credit is queue-ordered: a Focus
   action slotted after a move does not retroactively fund it. `projectedCosts` (the
   gross "S · C" queue summary) is unchanged.

**Validation.**
- `af-v3.4.smoke.js` extended (not duplicated) with a Focus-restore regression: an
  ungated stamina move is blocked at zero stamina, becomes queueable after Catch Breath
  is slotted, a second copy is gated per remaining restored stamina, and an empty queue
  leaves the gate unchanged; plus HTML markers for the copy button.
- Both smoke suites green. Browser acceptance still 31/31, 0 console errors. A focused
  browser check confirmed the copy button (clipboard content matches the on-screen log)
  and the Focus-restore gate live.
- The self-contained testbed artifact was rebuilt and republished to the same URL.

Notes for continuation: the log analysis also surfaced two non-blocking behaviors worth
revisiting — a skirmisher AI that repeatedly picks an out-of-range melee instead of
closing or using its ranged options, and a poise/guard-break stagger loop that can lock
a downed fighter out of acting until death. Neither was changed this pass.
