# Astro Fighters — Multi-Round Ecosystem Balance Pass 05

_Date: 2026-08-13._

## Purpose

Test the candidate DC, action-slot, and resource-cost model in actual multi-round combat across **all requested Sign, Universal, Martial, and Weapon kits** using legal character builds rather than synthetic +27-stat stress dummies.

The candidate DC switch remains **default-off** in ordinary play. This pass is a balance gate, not approval to enable the full candidate package.

## Test scope

- **22 kit families:** 12 Sign kits, Universal Arts, 6 Martial styles, and 3 Weapon kits.
- Four career/mastery bands: **L10/A0, L20/A5, L45/A10, L90/A10**.
- Five legal same-budget build profiles: Balanced, Physical Offense, Control Offense, Physical Defense, Mental Defense.
- Same-profile round-robin screening across every kit pair, legacy vs full candidate.
- Same-kit build stress: Physical Offense vs Physical Defense and Control Offense vs Mental Defense.
- Exhaustive fixed-planner screen: **19,184 battles**; round cap 12.
- Flagged contexts received larger-sample reruns and a **24-round** extension.
- Additional ablations isolated **DC**, **slots**, and **resource floors**.

### Legal build profiles

Every profile spends the exact legal attribute budget for its character level. Specialization changes distribution, not total power budget.

| Band | Profile | STR | AGI | FORT | INT | CHA |
|---|---|---:|---:|---:|---:|---:|
| L10/A0 | Balanced | 18 | 18 | 17 | 18 | 18 |
| L10/A0 | PhysicalOffense | 22 | 21 | 16 | 12 | 15 |
| L10/A0 | ControlOffense | 12 | 16 | 15 | 23 | 20 |
| L10/A0 | PhysicalDefense | 18 | 20 | 22 | 12 | 15 |
| L10/A0 | MentalDefense | 12 | 15 | 21 | 20 | 20 |
| L20/A5 | Balanced | 25 | 25 | 25 | 25 | 19 |
| L20/A5 | PhysicalOffense | 29 | 28 | 23 | 17 | 21 |
| L20/A5 | ControlOffense | 17 | 23 | 21 | 30 | 27 |
| L20/A5 | PhysicalDefense | 24 | 27 | 29 | 17 | 21 |
| L20/A5 | MentalDefense | 17 | 21 | 27 | 26 | 27 |
| L45/A10 | Balanced | 29 | 36 | 36 | 35 | 35 |
| L45/A10 | PhysicalOffense | 42 | 40 | 32 | 25 | 30 |
| L45/A10 | ControlOffense | 25 | 33 | 31 | 42 | 38 |
| L45/A10 | PhysicalDefense | 34 | 38 | 42 | 25 | 30 |
| L45/A10 | MentalDefense | 26 | 30 | 38 | 38 | 38 |
| L90/A10 | Balanced | 45 | 53 | 45 | 45 | 46 |
| L90/A10 | PhysicalOffense | 56 | 54 | 45 | 35 | 41 |
| L90/A10 | ControlOffense | 35 | 45 | 41 | 58 | 52 |
| L90/A10 | PhysicalDefense | 47 | 52 | 57 | 34 | 41 |
| L90/A10 | MentalDefense | 35 | 41 | 52 | 52 | 52 |

## Important planner correction

The first broad screen exposed a separate AI planning defect. `planFor()` did not track repetition strain inside the queue, subtracted only base resource cost while planning, did not track Supplies, and its aggression-floor insertion could exceed the five-slot budget. Candidate costs amplified this into large numbers of execution-time resource fizzles and produced false kit collapses.

The valid results below use a **test-local corrected planner** that:

- tracks within-round repeated uses,
- budgets repetition strain while planning,
- tracks Stamina, Chakra, Supplies, and total action slots,
- sanitizes the final queue after aggression-floor insertion.

With the correction, mean resource fizzles fell to about **0.008/battle legacy** and **0.068/battle candidate**. The earlier catastrophic Universal/Taurus/Sagittarius collapse results are discarded.

This planner legality correction still needs to be implemented in the repository runtime before broad AI pick-rate/win-rate evidence is considered final.

## Ecosystem-wide result

| Metric | Legacy | Full candidate | Change |
|---|---:|---:|---:|
| Avg battle length | 5.97 rounds | 7.95 rounds | +33.2% |
| Draw rate | 7.6% | 18.0% | +10.5 pp |
| Harmful status lands / battle | 4.23 | 14.17 | +9.94 |
| Resisted status attempts / battle | 26.29 | 15.09 | -11.19 |
| Hard action denials / battle | 0.000 | 0.802 | +0.801 |
| Resource fizzles / battle | 0.008 | 0.068 | +0.060 |

**Interpretation:** the candidate DC model succeeds at its primary job—CC/DOT is no longer mathematically inert—but the **full DC + slot + resource package slows combat too much**, especially in high-level/mastered contexts.

## Build-stress result

High-sample same-kit mirrors (1,056 battles per model/matchup):

| Build matchup | Model | Offense win | Defense win | Draw | Avg rounds |
|---|---|---:|---:|---:|---:|
| Physical Offense vs Physical Defense | Legacy | 42.5% | 57.4% | 0.1% | 5.34 |
| Physical Offense vs Physical Defense | Candidate | 16.8% | 83.2% | 0.0% | 6.32 |
| Control Offense vs Mental Defense | Legacy | 30.4% | 48.0% | 21.6% | 7.72 |
| Control Offense vs Mental Defense | Candidate | 26.8% | 47.0% | 26.2% | 8.95 |

The full candidate package strongly favors the FORT-heavy Physical Defense profile. That is consistent with Stamina premiums interacting with FORT's simultaneous HP, max-Stamina, regen, poise, and save benefits. The mental/control matchup shifts much less.

## High-level pacing is a real problem

The draw-heavy L45/A10 cases were rerun with a **24-round cap**. Several still ended in roughly 45–53% draws, so the issue is not simply a 12-round test cap:

- Scorpio / Control Offense: candidate **49.4% draw**, 18.81 rounds average.
- Kyudo / Mental Defense: **48.2%**, 18.79 rounds.
- Sagittarius / Control Offense: **45.2%**, 19.10 rounds.
- Judo / Mental Defense: **50.0%**, 19.05 rounds.
- Muay Thai / Mental Defense: **47.6%**, 19.24 rounds.
- Karate / Mental Defense: **53.0%**, 19.35 rounds.

Libra is different: its L45 Control-Offense candidate collapse remains even with low draw rate (23.2% win vs 72.6% legacy). That points to a **DC/control-identity or kit-interaction issue**, not an economy stalemate.

## DC vs economy ablation

Testing the same flagged contexts with `DC only`, `economy only`, and `full candidate` shows the worst stalls are generally an **interaction effect**. DC-only makes control functional; economy-only lengthens fights; combining the two produces the large stalemate rates.

For example:

- Karate Mental Defense: legacy 13.5% draw -> DC-only 15.1% -> economy-only 13.5% -> **full 50.8%**.
- Judo Mental Defense: 11.1% -> 6.3% -> 12.7% -> **full 47.6%**.
- Sagittarius Control Offense: 0.8% -> 9.5% -> 5.6% -> **full 38.1%**.

Libra again behaves differently: DC-only already changes L45 Control-Offense win rate from ~69.8% to ~15.9%, so Libra needs an individual control-stat/effect review.

## Slots vs resource floors

The more useful split is candidate DC + candidate slots versus candidate DC + candidate resource floors:

| Context | Legacy draw | DC only | DC + slots | DC + resources | Full |
|---|---:|---:|---:|---:|---:|
| Weapon:Kyudo | 11.9% | 8.3% | 16.7% | 42.9% | 53.6% |
| Sign:Sagittarius | 0.0% | 4.8% | 38.1% | 29.8% | 46.4% |
| Martial:Judo | 16.7% | 13.1% | 20.2% | 45.2% | 52.4% |
| Martial:MuayThai | 14.3% | 6.0% | 32.1% | 47.6% | 51.2% |
| Martial:Karate | 11.9% | 17.9% | 16.7% | 47.6% | 57.1% |

**Resource scaling is the dominant high-level pacing brake in four of the five representative contexts.** Slots still matter, especially for Sagittarius and Muay Thai, but the results do not support abandoning the owner's A/S action-economy direction. The first recalibration target should be the resource formula.

## Mastery-compounding experiment

The current candidate floor is effectively subjected to normal +5%/ability-level cost growth after the floor is raised. At A10 that turns S20 into 30 and S+GB25 into 37–38 before other family effects. A test alternative kept the approved A0 anchor but added the status premium **after** normal clean-move progression.

This helped some melee cases (Karate draw ~54.8% -> ~39.3%; Muay Thai ~47.6% -> ~40.5%; Judo ~48.8% -> ~40.5%) but did **not** solve Kyudo or Sagittarius. Therefore flat premium growth is promising for melee mastery scaling but is not sufficient as the final universal formula.

## What is validated vs what is not

### Strongly supported by this pass

1. The `/5 stat-edge, +/-6 cap` candidate DC plumbing is usable for further testing; it fixes the obsolete fixed-DC problem without making hard control automatic.
2. The owner-approved **base** melee-Stamina anchors C10/B12/A15/S20/S+GB25 do not need to be discarded because of this test.
3. The current **high-level application** of candidate resource floors is too punitive when combined with functional CC.
4. Resource scaling is generally a bigger pacing issue than A/S slot taxes.
5. Full candidate economy must remain **default-off** until the resource formula is recalibrated and retested.
6. The AI planner's within-round repetition/resource/slot budgeting must be fixed before AI balance evidence is treated as final.

### Still unresolved

- Exact ranged-Stamina and Chakra family multipliers (current x1.25 / x1.50 are provisional).
- Pure A/S Chakra floors.
- Per-ability attacker control-stat assignments; Libra is a high-priority review case.
- AoE extra-target premium.
- Resource-drain tiers.
- Harmful Trap Supply premium.
- Magnitude-aware DOT tiering: the current helper treats Bleed/Burn/Poison/Psychosomatic as C by status name, while earlier audit work intended heavier DOTs to up-tier by total damage.

## Recommended next formula direction

Preserve the owner's base anchors, but separate the components that currently compound each other:

```text
Final Resource = Scaled clean comparator
               + Effect-tier premium
               + Range/resource-family premium
               + package modifiers (GB / AoE / etc.)
```

Instead of multiplying the entire harmful-effect floor by mastery and then multiplying again for delivery family, let ordinary ability progression scale the clean move and price the harmful rider/range advantage as explicit premiums. The next simulation should calibrate those additive premiums so that:

- A0 melee still reproduces **10 / 12 / 15 / 20 / 25**.
- melee Stamina < ranged Stamina < Chakra remains intact.
- A/S slots still constrain action frequency.
- L45/L90 mastered combat no longer drifts into 40–50% stalemates.

## Test limitations

- The local execution snapshot was normalized from a slightly older standalone to the current 170-ability roster using the current audited catalog and current approved Martial/Weapon values.
- Current reach behavior was approximated for Karate Blitz / Single Leg in the local snapshot; exact gap-close movement should be rerun from a current checkout before final lock.
- Neutral Libra sign was used for fighters to remove natal Sign affinity as a confounder.
- Open arena only; terrain/LoS is a later balance layer.
- Grapples remain on their separate contest system.

## Gate decision

**Do not enable the full candidate DC + slot + resource package by default.** Continue with the candidate DC test path, fix planner legality, and recalibrate the resource formula before the next full-roster multi-round pass.
