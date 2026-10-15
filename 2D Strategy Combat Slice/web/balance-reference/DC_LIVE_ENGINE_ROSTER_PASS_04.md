# Astro Fighters — Live Engine DC Roster Pass 04

_Date: 2026-08-12._

This pass exercises the candidate DC model through the real `AF.resolveRound` / `applyStatus` path with candidate mode enabled only inside the harness. It covers Sign, Universal, Martial, and Weapon abilities together.

## Scope

- Roster abilities: **170**
- Tiered hostile Status/DOT effects: **67**
- Legacy automatic hostile effects normalized by candidate mode: **14**
- Trials per effect/scenario: **800**
- Total real-engine resolved rounds: **214,400**

## Provisional attacker control-stat schema

This is a test hypothesis, **not owner-locked**. Explicit ability/effect metadata overrides all defaults.

- Genjutsu → CHA
- Ninjutsu → INT
- Trap / Medical hostile control → INT
- Physical finesse riders (Bleed, Blind, Slow, Prone, Root, Snare, Cripple) → AGI
- Other physical force/control riders → STR
- Dojutsu (outside this requested roster) → CHA for GenVisual, INT otherwise

## Aggregate conditional landing results

| Scenario | Tier | Effects | Observed | Exact target | Deviation |
|---|---|---:|---:|---:|---:|
| equal_L0 | C | 13 | 59.7% | 60.0% | -0.33 pp |
| equal_L0 | B | 23 | 44.8% | 45.0% | -0.17 pp |
| equal_L0 | A | 18 | 35.1% | 35.0% | +0.08 pp |
| equal_L0 | S | 13 | 30.1% | 30.0% | +0.09 pp |
| equal_L10 | C | 13 | 70.2% | 70.0% | +0.19 pp |
| equal_L10 | B | 23 | 54.5% | 55.0% | -0.52 pp |
| equal_L10 | A | 18 | 45.0% | 45.0% | -0.03 pp |
| equal_L10 | S | 13 | 40.4% | 40.0% | +0.42 pp |
| specialist_attacker_L10 | C | 13 | 94.4% | 95.0% | -0.59 pp |
| specialist_attacker_L10 | B | 23 | 80.1% | 80.0% | +0.14 pp |
| specialist_attacker_L10 | A | 18 | 70.0% | 70.0% | +0.00 pp |
| specialist_attacker_L10 | S | 13 | 64.6% | 65.0% | -0.43 pp |
| specialist_defender_L10 | C | 13 | 44.1% | 45.0% | -0.92 pp |
| specialist_defender_L10 | B | 23 | 30.1% | 30.0% | +0.10 pp |
| specialist_defender_L10 | A | 18 | 20.3% | 20.0% | +0.32 pp |
| specialist_defender_L10 | S | 13 | 14.3% | 15.0% | -0.71 pp |

## Cost/slot shadow audit

- Status abilities that would gain slots under the current candidate formula: **27**.
- Status abilities below the current candidate authored-resource recommendation: **34**.

## Interpretation

The real resolver reproduces the candidate tier probabilities after delivery while preserving the engine's actual attack/range gate before single-target damaging riders. Automatic legacy riders now participate in the same save path during candidate-mode tests. This pass validates plumbing and probability behavior; it does **not** approve the provisional control-stat assignments or final resource/slot changes.
