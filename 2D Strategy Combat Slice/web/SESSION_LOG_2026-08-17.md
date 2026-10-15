# Session log — 2026-08-17

## Scope

A full striker/grappler balance pass driven by real-engine round-robin testing (the actual
`AF.planFor` AI + `AF.resolveRound`, not simulated math), two engine-fairness bug fixes
(movement-phase collision resolution, initiative tie-break) discovered while investigating that
testing's own confounds, a new opponent/ally level-selection UI with a default that tracks the
player's level, a rewrite of the multi-combatant scenario system (1vX gang battles, and Team/FFA
generalized to a 10-combatant roster), and a ported bug fix (defeated-target retargeting) found
on an unmerged sibling branch while investigating a scenario-system regression report.

No new versioned HTML/JS page was created. All work is in the existing V3.4/V3.5 modules;
`astro-fighters-standalone.html` and `astro-fighters-artifact.html` were rebuilt repeatedly from
the same seven modules as the session progressed. Full rationale, before/after numbers, and
owner-ruling quotes for every change below are in `docs/DECISIONS.md` under matching
`2026-08-17` headers — this log is the file-level summary and chronology; that file is the
detailed record.

## Files changed

| File | Change |
|---|---|
| `web/af-core.js` | New `E.push`/`pushTarget` effect (Side Kick); Karate/Wrestling kit number changes; AI planner Guard-Break/Buff/Push scoring; style-NPC stat equalization to 48; `enemyLevelAnchor`/`scaleEnemyStats`; movement-phase and initiative-scheduling AGI-priority fixes; `retargetDefeated` + `resolveSingleEnemy` mid-round retarget. |
| `web/af-core-v3-patch.js` | Plan-sanitizer retarget of a start-of-round-dead chosen target. |
| `web/af-page-v3.js` | Opponent/ally level fields + player-level sync/default; dynamic roster UI and state (`S.roster`) for 1vX/Team/FFA; arc-based spawn anchoring for up to 10 combatants; `scenarioLabel` generalization. |
| `web/astro-fighters-2d-v3.4.html` | Opponent/ally level inputs; roster UI markup and `.roster-row`/`.roster-group` CSS; scenario `<select>` options (`onevx`, generalized Team/FFA labels). |
| `web/af-v3.4.smoke.js` | Updated assertions for every changed ability number; new regression tests: Side Kick push, movement-phase AGI priority, opponent-level scaling, initiative AGI tie-break, defeated-target retarget. Style-NPC stat-total test tightened to exact equality. |
| `web/astro-fighters-standalone.html`, `web/astro-fighters-artifact.html` | Rebuilt via `node build-standalone.js [--artifact]` after each runtime change (artifact is gitignored, rebuilt locally before each publish). |
| `web/README.md`, `web/HANDOFF.md`, `docs/DECISIONS.md` | Documentation pass (this session) — module list corrections, new dated decision entries, known-gaps updates, sibling-branch reconciliation notes. |

## 1. Round-robin balance testing methodology

Striking-vs-striking and grappling-vs-grappling only, per the standing 2026-08-15 archetype
ruling (cross-archetype results are intended counter-play, not a balance signal). All
style-NPC comparisons this session were run at **equal total stat budgets** (see §5) — an
explicit owner requirement, since kits differ in how they spend a stat spread, not in how much
of one they get.

## 2. Side Kick push, Wrestling cost cuts, AI Buff/Guard-Break valuation

- New engine primitive `E.push(tiles)` / `pushTarget(B, owner, target, tiles)`: displaces the
  **target** away from the owner in a straight line, one hex at a time, stopping early if boxed
  in. Distinct from the pre-existing `E.move`, which repositions the *owner*.
- Karate Side Kick carries `E.push(1)`, firing unconditionally on any landed hit — no separate
  save. This implements a previously-tracked known gap (the Sheet's authored "AGI DC12, push
  back 1 tile" rider had never been wired up) but deliberately diverges from that authored
  version; see `HANDOFF.md` Known Gap #2 and the Sheet-sync note below.
- Wrestling Suplex/Choke Slam Stamina cut 50 → 40 (owner-approved "for now," not a locked
  floor). Ground and Pound gained a `Stamina −12` rider, targeting its Mount-lock-in-gap root
  cause (no submission-style escalating hold, unlike Judo/Jiu-Jitsu).
- AI planner (`planFor().score()`): Guard Break poise damage now scores as real tempo denial;
  self-Buff effects score by real magnitude/duration instead of a flat useless `+4`, with a
  dedup guard against re-buffing an active stat; Push gets a flat score.
- Owner explicitly declined a per-round ability cap (e.g. capping Sweeping Low uses/round) as a
  balance lever — per-round throughput should stay resource-gated, not hard-capped. Standing
  rule for future passes.

## 3. Karate damage pass

Root-caused Karateka's ~2.5% striking-mirror net win rate via elimination testing (not a flat
buff): Sweeping Low 5→7, Karate Blitz 8→13, Side Kick 8→10, Hammer Fist 10→16, Whirlwind Kick
10→15. Stamina unchanged on every move, per owner direction. Power was skewed toward Hammer
Fist/Karate Blitz specifically (not a uniform percentage) so the AI's own greedy per-slot
scoring would naturally start picking the intended blitz-in/control/follow-up combo, rather than
just hitting harder with whatever it already over-picked. Result: 23.8% net win rate, Hammer
Fist/Karate Blitz usage ~0%→44-45%/9%. Deferred: Boxer is now the clear striking-mirror outlier
(76.3%) and is the dominant remaining explanation for Karate's floor.

## 4. Wrestling grappling-mirror pass

Suplex/Choke Slam cost cut and the Ground and Pound Stamina rider (§2) brought Wrestling to
~50% net win rate in the grappling mirror (parity). Jiu-Jitsu's ~14% floor was **not**
addressed this session — no Jiu-Jitsu numbers changed; its "zero standing offence" structural
cause (every damaging option needs an established relationship) is unresolved and still open
for a ruling.

## 5. Style-NPC stat-budget equalization

Investigating a post-AI-fix Boxer/Muay Thai shift (50/50 → 63/38) surfaced a pre-existing,
unrelated bug: MuayThaiFighter's total stat budget was 44 against the other five NPCs' 47-49 —
a coincidental cancellation the AI fix had stopped masking. All six style NPCs
(`Boxer`/`MuayThaiFighter`/`Judoka`/`Jiujiteiro`/`Karateka`/`Wrestler`) now total **exactly 48**
each, keeping their individual relative shapes. Enforced by an exact-equality regression test
(was a 2.5-point tolerance band).

## 6. Movement-phase collision resolution

Found while chasing a residual seat-order confound in the round-robin data: identical fighters
spawned apart split 44/56 by `plans`-array position alone. Root cause: the old movement
resolver processed moves strictly in array order with no fairness rule — a fighter whose target
cell lost a contest kept its full movement budget unspent, which a *separate*, unrelated
mid-action "approach anyway" fallback in `resolveSingleEnemy` then spent during that fighter's
own attack, letting it reach melee a full round sooner than the fighter who "won" the cell.
**This affects real player-vs-AI battles**, not just test harnesses — the player is always
`plans[0]` in `af-page-v3.js`.

Fixed per an explicit owner design spec: movement resolves as its own AGI-priority sub-phase
before actions — highest AGI claims a contested cell first, each lower-AGI contender claims
whichever adjacent-to-its-target cell is closest and still reachable. AGI ties keep original
plan order (the one tiebreak the spec didn't cover). Verified 44/56 → 47/53 with identical
fighters, and with a deterministic regression test that deliberately lists the lower-AGI
fighter first in the plans array.

## 7. Initiative tie-break

The residual 47/53 gap after §6 traced to the same bug one layer up: the per-action scheduling
loop's tie-break favored `plans`-array position on an exact key tie. Fixed identically — ties
now go to higher current AGI, falling back to array order only if AGI also ties. Verified with
a test that engineers a genuine key tie between two different-AGI, different-ability fighters
(confirmed to fail without the fix).

## 8. Opponent/ally level selection

`AF.scaleEnemyStats(stats, level)`: linear scaling of a style NPC's canonical (48-point) stat
block, anchored so level 20 reproduces this session's tuned numbers exactly. New level fields
in setup for each opponent/ally slot. Owner ruling: these default to and track the player's own
level selector — including its true out-of-the-box default of **level 1** (a fact this session
discovered belonged to `af-progression-v3.js`'s point-buy allocator, not `af-page-v3.js`'s own
`setLevel(20)` call, which runs first and is then overridden) — until a specific field is
hand-edited, which detaches only that field.

## 9. 1vX and scalable Team/FFA scenarios

New "1 vs X" scenario (player vs 1-9 same-faction opponents). Team battle and free-for-all
rewritten from fixed 2v2/3-way shapes into a dynamic add/remove roster (style + level per
combatant), capped at 10 combatants total including the player, as an explicit scalability
testbed. Verified live in-browser at default size, at the 10-combatant cap, and running an
actual round of 1-vs-9 combat with no errors. Duel/Escort/Ambush unchanged.

While investigating a user report that "1vX/XvX scenarios are missing," discovered a sibling
branch, `claude/astro-fighter-dev-continue-1pffha` (diverged 2026-08-13, never merged), that had
already built a different, simpler gauntlet/choose-count scenario system covering the same
need — it was never merged into this line of work, which is why it appeared "missing." The
roster-based design here supersedes it; see `docs/DECISIONS.md` for the full reconciliation
state of that branch's other 16 commits.

## 10. Redirect queued attacks off a defeated target

A queued single-target action whose chosen enemy dies before it resolves (mid-round, from an
earlier queued action, or already dead at round start from a stale queue/DOT) now retargets to
the weakest reachable foe instead of fizzling or being silently dropped. Ported from the
sibling branch found in §9 (`80a2e4d`, 2026-08-13) — reimplemented against the current
`resolveSingleEnemy` and plan sanitizer rather than cherry-picked, since both have materially
changed since that branch diverged. Both the mid-round and start-of-round paths are covered by
a regression test, each independently confirmed to fail without its half of the fix.

## Documentation pass

`web/README.md` and `web/HANDOFF.md` updated for accuracy: missing `af-dc-model-v3.js` added to
both modules lists; V3.4→V3.5 version-string clarification; standalone/artifact build
instructions; all balance sections above reflected with current numbers; Known Gaps list
updated (Side Kick resolved-with-deviation, NPC level selection resolved); sibling-branch
discovery and reconciliation state recorded. `docs/DECISIONS.md` got one dated entry per major
change above. The canonical Google Sheet's reconciliation status against this session's changes
is tracked separately — see the "Workbook synchronization note" in `HANDOFF.md`.
