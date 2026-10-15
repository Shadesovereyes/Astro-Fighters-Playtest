# Astro Fighters — DC + Unified Slot/Resource Cost Model v0.2

_Last updated: 2026-08-12. PROVISIONAL FORMULA — owner-approved tier anchors and resource-family hierarchy; family multipliers and action-pressure constants remain under simulation._

This document supersedes the cost portion of `docs/DC_COST_MODEL_V0_1.md` while retaining the same candidate DC curve. It supplements `docs/DC_CC_BALANCE_FRAMEWORK.md`.

## A. Candidate DC model

The current fixed authored DC 11–13 model does not scale with character stats or ability mastery. Candidate v0.2 remains:

```text
Control = floor(attacker relevant control stat / 2)
Save    = floor(defender relevant save stat / 2) + d20
DC      = Control + TierOffset + MasteryBonus
MasteryBonus = floor(abilityLevel / 4)

Natural 1 on the save die = status lands.
Natural 20 on the save die = status is resisted.
Otherwise, Save >= DC resists; Save < DC lands.
```

Tier offsets target the owner-approved equal-investment post-hit landing rates at ability level 0:

| Tier | Offset | Equal-stat L0 landing target |
|---|---:|---:|
| C | +13 | 60% |
| B | +10 | 45% |
| A | +8 | 35% |
| S | +7 | 30% |

At equal investment, the current mastery candidate gives:

| Tier | Ability L0 | L5 | L10 |
|---|---:|---:|---:|
| C | 60% | 65% | 70% |
| B | 45% | 50% | 55% |
| A | 35% | 40% | 45% |
| S | 30% | 35% | 40% |

With a representative 75% attack hit chance, damaging-rider total attempt proc rates at L0 are C 45%, B 33.75%, A 26.25%, S 22.5%. Pure control has no attack-roll gate and therefore uses the full save landing rate.

## B. Owner-locked resource hierarchy

Resource families are intentionally **not numerically equivalent**.

1. **Stamina melee is the lower-cost resource family.** Martial and ordinary close-range physical techniques are intended to be cheaper in raw resource numbers.
2. **Chakra-costing offensive/control abilities are intentionally more expensive.** Chakra techniques buy the inherent tactical advantage of ranged delivery, so their numerical Chakra cost must sit above comparable Stamina techniques rather than being normalized to the same raw cost.
3. **Ranged Stamina is an intermediate family.** Kyudo deliberately costs more Stamina than most Stamina techniques because it buys the same kind of range advantage without paying Chakra. Other genuinely ranged Stamina techniques should be evaluated the same way.
4. The comparison must use **effective paid cost**, not accidentally stack multiple hidden range/family multipliers. The current engine already contains an `elementalCostMult` family multiplier; implementation must reconcile that with this model rather than adding a second range tax on top without inspection.
5. If an ability consumes both Stamina and Chakra, harmful-status and Guard Break premiums apply to both channels, but the Chakra channel should remain numerically higher for an otherwise comparable contribution.

This hierarchy is an intentional game-design choice, not an artifact of current authored values.

## C. Owner-locked damaging-rider Stamina anchors

For a standard one-target damaging rider delivered by a normal melee Stamina technique, the target **base resource floors** are:

| Package | Stamina anchor |
|---|---:|
| C light rider | **10** |
| B tactical rider | **12** |
| A rider | **15** |
| S rider | **20** |
| S rider + Guard Break | **25** |

These are not arbitrary one-off move prices. They define the calibration ladder the formula must reproduce.

Using a clean 8-Stamina melee comparator, the corresponding tier multipliers are:

```text
C = ×1.25
B = ×1.50
A = ×1.875
S = ×2.50
Guard Break package modifier = ×1.25
```

Thus:

```text
8 × 1.25  = 10   C
8 × 1.50  = 12   B
8 × 1.875 = 15   A
8 × 2.50  = 20   S
8 × 2.50 × 1.25 = 25   S + Guard Break
```

The same multipliers scale from a more expensive clean comparator when the underlying attack is already stronger than a basic 8-resource technique. The absolute tier anchor is a floor, not a cap.

## D. Resource-family floor model

Candidate family scales for simulation:

| Delivery/resource family | Candidate scale | Design role |
|---|---:|---|
| Melee Stamina | **×1.00** | baseline / lowest numerical cost |
| Ranged Stamina | **×1.25** | Kyudo-style range tax without Chakra |
| Chakra | **×1.50** | higher numerical cost for ranged chakra delivery |

These **×1.25 / ×1.50 values are provisional simulation constants**, not yet owner-locked. The hierarchy itself is owner-locked.

With the 8-resource normalized reference, the tier floors become:

| Tier | Melee Stamina | Ranged Stamina | Chakra |
|---|---:|---:|---:|
| C | 10 | 13 | 15 |
| B | 12 | 15 | 18 |
| A | 15 | 19 | 23 |
| S | 20 | 25 | 30 |
| S + Guard Break | 25 | 32 | 38 |

For each consumed resource channel:

```text
NormalizedBase = max(
    clean same-family comparator cost,
    8 × ResourceFamilyScale
)

RiderCost = ceil(
    NormalizedBase
    × TierMultiplier
    × GuardBreakMultiplier
    × MagnitudeDurationMultiplier
    × OtherPackageMultipliers
)
```

Do not lower the result below the owner-approved tier floor simply because an ability has setup. Setup primarily earns **action-slot credit**; it may justify later fine-tuning of resources, but it does not erase the harmful-effect resource premium.

## E. Pure control premium

Pure control bypasses the attack-roll gate, so A/S pure-control abilities must carry **higher resource premiums than damaging riders of the same intrinsic tier**.

Initial simulation multipliers:

```text
Pure A multiplier = ×4/3 on top of the A rider cost
Pure S multiplier = ×1.50 on top of the S rider cost
```

This produces the following provisional floors from the same 8-resource reference:

| Pure control | Melee-Stamina equivalent | Ranged-Stamina equivalent | Chakra |
|---|---:|---:|---:|
| Pure A | **20** | 25 | **30** |
| Pure S | **30** | 38 | **45** |

The owner has approved the rule that Pure A/Pure S require higher resource premiums; the exact 20/30 Stamina-equivalent and 30/45 Chakra values remain test candidates until sustain simulations are complete.

## F. Simultaneous action-slot formula

Final slots and final resources are generated from the **same ability package description**, but slots do not directly subtract the tier resource floor. This preserves the ruling that action slots supplement rather than replace resource premiums.

Define the L0 expected proc rate:

```text
ProcRate = TierLandingRate × AttackGate
AttackGate = representative hit probability for damaging riders
AttackGate = 1.0 for pure control
```

Candidate action weights:

| Tier | Action weight |
|---|---:|
| C | 1 |
| B | 2 |
| A | 4 |
| S | 5 |

Candidate pressure calculation:

```text
ActionPressure = TierActionWeight × ProcRate × SetupFactor

+ 0.80 if Pure Control
+ 0.25 if Guard Break
+ small package terms for AoE / Priority / Reach when they exceed the clean comparator
- DamageSacrificeCredit when the move gives up meaningful base damage versus its clean comparator
```

Candidate slot bands:

```text
ActionPressure < 1.00        -> 1 slot
1.00 <= pressure < 2.25      -> 2 slots
ActionPressure >= 2.25       -> 3 slots
```

Slots are authored from the **base L0 package**. Ability mastery does not dynamically increase slot count; mastery already raises resource cost through progression.

At the current baseline probabilities this yields the intended first anchors:

- C damaging rider: 1 slot.
- B damaging rider: 1 slot.
- A damaging rider at normal damage: 2 slots.
- S damaging rider at normal damage: 2 slots.
- S + Guard Break damaging package: 2 slots in the ordinary single-target case.
- Pure A control: 2 slots.
- Pure S control: 3 slots.

### Sweeping Low exception produced by the formula, not by rank exemption

Sweeping Low has S-tier Prone, but it also deals less damage than Karate's clean Side Kick comparator. The damage-sacrifice credit can pull its ActionPressure below the 1-slot threshold while its resource cost still pays the full **S-tier 20-Stamina floor**. This preserves the owner-approved five-action Karate string without pretending Prone is a weaker status.

### Hilt Bash stacked package

Hilt Bash combines damage + S-tier Stun + Guard Break. Its package pressure remains in the 2-slot band, while the Stamina floor is **25** from the S + Guard Break ladder. This makes both action economy and resource economy visibly pay for the stacked premium mechanics.

## G. Why the family hierarchy matters in sustain terms

Stamina and Chakra have different pools but currently similar flat regeneration formulas. At equal FORT/CHA, both regenerate `5 + stat × 0.5` per round, while Chakra's maximum pool is larger.

A higher raw Chakra cost therefore serves two purposes:

- it prices the inherent range advantage;
- it increases the number of regeneration rounds needed to replace one cast, preserving a meaningful sustain difference even though the Chakra pool starts larger.

The ranged-Stamina/Kyudo premium is the same design logic applied to a Stamina technique that gains long-range delivery.

## H. DC + cost simulation gates

Before these candidate constants become implementation canon, test:

1. DC rates at equal stats and +/-5 relevant-stat edges for low/mid/high absolute stat bands.
2. Ability levels 0/5/10 and the existing +5% resource growth per ability level.
3. Total attempt proc rates for damaging riders versus pure control.
4. Legal five-slot strings and repetition strain under the new 10/12/15/20/25 Stamina anchors.
5. Resource sustain over 2–4 rounds at representative FORT/CHA pools and regen.
6. Melee Stamina versus ranged Stamina versus Chakra delivery families.
7. Stacked Guard Break + status packages.
8. Setup-gated grapple/mount techniques separately.
9. Audit the current `elementalCostMult` implementation so the new chakra/range hierarchy is represented exactly once and displayed clearly to the player.

The goal is to lock a model where **effect tier, landing reliability, delivery advantage, resource family, setup burden, and action economy are all visible terms rather than hidden one-off tuning decisions**.