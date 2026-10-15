# Astro Fighters — DC / Resource Simulation Pass 01

_Date: 2026-08-12. Simulation findings only; do not treat candidate DC constants or family multipliers as owner-locked until approved._

## Inputs already approved by owner

- Post-hit equal-investment rider targets: C 60%, B 45%, A ~35%, S ~30%.
- Standard melee-Stamina damaging-rider anchors: C 10, B 12, A 15, S 20, S+Guard Break 25.
- Pure A and Pure S control must cost more resource than damaging riders of the same tier.
- Effect tier is not automatically final slot cost.
- Stamina melee is intentionally the lowest numerical resource family.
- Chakra offensive/control abilities intentionally cost more because they buy ranged delivery.
- Kyudo/ranged-Stamina abilities intentionally cost more Stamina than ordinary melee Stamina because they also buy range.

## 1. Resource multiplier fit

An 8-Stamina clean melee reference reproduces the approved rider ladder exactly with:

- C ×1.25 -> 10
- B ×1.50 -> 12
- A ×1.875 -> 15
- S ×2.50 -> 20
- Guard Break package modifier ×1.25 -> S+GB 25

This is a useful formulaic fit because stronger clean comparators can use the same tier multiplier instead of every move receiving a hand-authored absolute number.

## 2. Candidate delivery-family scales

First sustain pass uses these temporary family scales:

- melee Stamina ×1.00
- ranged Stamina ×1.25
- Chakra ×1.50

From the same normalized 8-resource reference, the damaging-rider floors become:

| Tier | Melee Stamina | Ranged Stamina | Chakra |
|---|---:|---:|---:|
| C | 10 | 13 | 15 |
| B | 12 | 15 | 18 |
| A | 15 | 19 | 23 |
| S | 20 | 25 | 30 |
| S + Guard Break | 25 | 32 | 38 |

Provisional pure-control multipliers (higher because there is no attack-roll gate):

| Pure control | Melee-Stamina equivalent | Ranged-Stamina equivalent | Chakra |
|---|---:|---:|---:|
| Pure A | 20 | 25 | 30 |
| Pure S | 30 | 38 | 45 |

The ×1.25 ranged-Stamina and ×1.50 Chakra family factors are not approved yet; only the hierarchy is approved.

## 3. Sustain interpretation

Current pool/regen formulas:

```text
max Stamina = 20 + FORT × 5
max Chakra  = 50 + CHA × 10
Stamina regen = 5 + FORT × 0.5
Chakra regen  = 5 + CHA × 0.5
```

At equal FORT/CHA, Stamina and Chakra regenerate at the same raw rate even though the Chakra pool is larger. Therefore a higher raw Chakra price genuinely increases replacement time per cast and is a useful way to price range rather than merely compensating for the larger pool.

Example at stat 10: both resources regenerate 10/round. An S damaging rider at the candidate floors costs 20 Stamina (2 rounds of regen) versus 30 Chakra (3 rounds of regen). Pure S is 30 Stamina (3 rounds) versus 45 Chakra (4.5 rounds).

## 4. Legal Karate string under the new S-rider floor

Approved active-stance control string:

`Karate Blitz 10 -> Side Kick 8 -> Side Kick 8 -> Sweeping Low 20 -> Hammer Fist 10`

Base round cost = **56 Stamina**. Side Kick is used only twice, so repetition strain does not surcharge the string.

Representative sustain before any additional balance changes:

- FORT 10: max 70, regen 10. One full string is affordable; a second consecutive full string is not.
- FORT 20: max 120, regen 15. Two consecutive full strings are affordable; a third is not.
- FORT 30: max 170, regen 20. Heavy FORT investment can sustain several consecutive full strings.

This is directionally desirable: the S-tier rider is available inside the intended five-action Karate combo, but repeatedly executing the entire premium string requires meaningful FORT investment.

## 5. Simultaneous slot-pressure candidate

Candidate L0 action-pressure model uses the total raw attempt proc rate rather than intrinsic rank alone:

```text
ProcRate = tier landing rate × attack gate
Tier action weights: C=1, B=2, A=4, S=5
ActionPressure = TierWeight × ProcRate × SetupFactor
               + pure-control bonus
               + stacked-package bonuses
               - meaningful damage-sacrifice credit

pressure < 1.00       -> 1 slot
1.00 to <2.25         -> 2 slots
pressure >= 2.25      -> 3 slots
```

With a 75% representative hit gate and the approved rider landing targets, the first anchors are:

- C damaging rider -> 1 slot
- B damaging rider -> 1 slot
- ordinary A damaging rider -> 2 slots
- ordinary S damaging rider -> 2 slots
- Pure A -> 2 slots
- Pure S -> 3 slots
- S + Guard Break -> 2 slots in the ordinary single-target case
- Sweeping Low can remain 1 slot because it gives up base damage relative to Side Kick while still paying the full 20-Stamina S-tier resource floor.

The exact action-pressure constants remain provisional; the structure is the important result.

## 6. DC simulation: original half-stat candidate

The first candidate used half of the attacker stat and half of the defender stat. It preserved equal-investment baselines but a +/-5 stat gap shifted reliability by roughly 10–15 percentage points and larger gaps quickly became too dominant.

That is concerning because high-level Astro Fighters can create much larger specialization gaps than five stat points.

## 7. DC simulation: relative quarter-stat candidate

A cleaner candidate is to scale only the **relative relevant-stat edge**:

```text
StatEdge = clamp(trunc((AttackerControlStat - DefenderSaveStat) / 4), -4, +4)
MasteryBonus = floor(AbilityLevel / 4)
DC = TierOffset + StatEdge + MasteryBonus

TierOffset: C=13, B=10, A=8, S=7
Natural 1 on save = status lands
Natural 20 on save = status resisted
Otherwise d20 >= DC resists
```

This preserves the exact equal-investment L0 targets while making stat scaling controlled and target-relative.

### L0 landing rates by stat edge

| Attacker relevant stat vs defender | C | B | A | S |
|---:|---:|---:|---:|---:|
| -20 or worse (cap) | 40% | 25% | 15% | 10% |
| -10 | 50% | 35% | 25% | 20% |
| -5 | 55% | 40% | 30% | 25% |
| equal | **60%** | **45%** | **35%** | **30%** |
| +5 | 65% | 50% | 40% | 35% |
| +10 | 70% | 55% | 45% | 40% |
| +20 or better (cap) | 80% | 65% | 55% | 50% |

Ability level 10 currently adds +2 DC, i.e. +10 percentage points before the natural-roll ceiling/floor. Thus an extreme +20-stat S specialist at ability L10 reaches about 60% rather than becoming near-automatic; an equal-investment L10 S ability is about 40%.

This candidate better matches the design target of **investment matters, but hard control does not become automatic**.

## 8. Next simulation gates

1. Test the relative-quarter-stat DC curve against actual low/mid/high stat allocations generated by the career budget rather than arbitrary stat numbers.
2. Monte Carlo full attack -> hit -> save -> status sequences for representative C/B/A/S moves.
3. Test new resource anchors over 3–6 round fights at FORT/CHA specialist, balanced, and neglected-resource builds.
4. Compare ranged-Stamina ×1.25 versus nearby candidates (for example ×1.20 and ×1.30).
5. Compare Chakra ×1.50 versus nearby candidates while accounting for the existing `elementalCostMult` so range is charged exactly once.
6. Apply the formula to actual Martial/Weapon moves only after the same-kit clean comparator for each move is identified.
7. Fix AI status-rider scoring before using planner pick-rate as evidence for final costs.