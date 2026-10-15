# Astro Fighters — Multi-Round Elimination-Only Correction

_Date: 2026-08-13._

## Owner ruling

**There is no round cap in combat.** A battle is decided when one character in a duel, or one entire faction/team in a team battle, is eliminated.

Balance simulations must therefore never classify a still-active battle as a draw because a test reached an arbitrary round number.

A simultaneous double KO may be reported separately because both sides were actually eliminated. A simulation that enters a genuinely non-progressing repeated state is a **NON_TERMINATING_BATTLE test/engine failure**, not a draw.

## Pass 05 correction

The 12-round and 24-round `draw rate` metrics in `DC_MULTIROUND_ECOSYSTEM_PASS_05.md` are **superseded and must not be used as outcome metrics**. They measured unresolved-at-cap fights, not valid game outcomes.

The correct interpretation of those results is that the candidate package created very long battles. The resource-scaling diagnosis remains useful, but claims framed as draw/stalemate percentages require elimination-only retesting.

## Uncapped targeted rerun

A corrected local rerun used the same normalized 170-ability snapshot, corrected within-round planner budgeting, and **no battle round limit**. It covered the seven previously important L45 contexts against every other kit, with four mirrored seeds per opponent: **1,176 elimination-based battles**.

No fight in this targeted set was ended because of elapsed rounds. No repeated-state non-termination failure occurred.

| Context | Model | Win rate | Avg rounds | Median | P90 | P95 | Max |
|---|---|---:|---:|---:|---:|---:|---:|
| Scorpio / Control Offense | legacy | 67.9% | 10.75 | 10 | 14 | 18 | 38 |
| Scorpio / Control Offense | candidate | 65.5% | **29.07** | 24 | 53 | 62 | 92 |
| Kyudo / Mental Defense | legacy | 69.0% | 14.76 | 10 | 27 | 30 | 71 |
| Kyudo / Mental Defense | candidate | 64.3% | **28.42** | 28 | 48 | 57 | 83 |
| Sagittarius / Control Offense | legacy | 73.8% | 10.10 | 10 | 13 | 13 | 31 |
| Sagittarius / Control Offense | candidate | 61.9% | **24.64** | 22 | 41 | 49 | 74 |
| Judo / Mental Defense | legacy | 79.8% | 14.45 | 10 | 30 | 34 | 65 |
| Judo / Mental Defense | candidate | 67.9% | **29.06** | 25 | 54 | 59 | 88 |
| Muay Thai / Mental Defense | legacy | 75.0% | 13.06 | 10 | 24 | 27 | 51 |
| Muay Thai / Mental Defense | candidate | 60.7% | **29.62** | 27 | 51 | 61 | 102 |
| Karate / Mental Defense | legacy | 77.4% | 12.94 | 10 | 24 | 29 | 70 |
| Karate / Mental Defense | candidate | 83.3% | **30.57** | 28 | 52 | 64 | 115 |
| Libra / Control Offense | legacy | 69.0% | 10.77 | 10 | 14 | 16 | 42 |
| Libra / Control Offense | candidate | **20.2%** | 11.05 | 10 | 17 | 18 | 29 |

Kyudo candidate produced one simultaneous double KO in 84 battles (1.2%); this is an actual elimination result and is tracked separately rather than as a round-cap draw.

## Revised interpretation

1. The candidate DC model still makes harmful control materially functional.
2. The full candidate economy still produces a major **combat-duration problem**, but the problem is long time-to-elimination rather than a valid draw rate.
3. Candidate resource scaling remains the first recalibration target because the prior DC/slot/resource ablations showed resources were the dominant pacing brake in most flagged contexts.
4. Libra remains a distinct non-pacing outlier: its candidate win rate collapses while battle duration remains near legacy, pointing to control-stat/effect identity or kit interaction rather than resource-driven long fights.
5. Future acceptance criteria should use elimination-round distributions (median/P90/P95/max), win rates, double-KO rate, control uptime, resource sustain, and non-termination failures — **never round-cap draws**.

## Harness change

`tools/dc_multiround_matrix.js` now runs `while (!Battle.decided())` with no combat round cap. It reports only A win, B win, or simultaneous double KO. An exact repeated combat state for 100 consecutive rounds throws `NON_TERMINATING_BATTLE` so an engine loop cannot be silently converted into an outcome.

The full 22-kit elimination-only matrix should be rerun from a current checkout after the runtime AI planner legality correction is committed.