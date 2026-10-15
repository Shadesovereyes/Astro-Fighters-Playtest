# Astro Fighters — DC / Cost Roster Simulation Pass 03B

_Date: 2026-08-12. Monte Carlo + sustain follow-up to `DC_ROSTER_SIMULATION_PASS_03.md`._

## Monte Carlo scope

The 61 ordinary direct-status/DOT abilities from the sign, Universal, Martial and Weapon roster were each simulated for 50,000 raw action attempts under four candidate-DC scenarios:

1. equal relevant stats, ability level 0;
2. equal relevant stats, ability level 10;
3. level-20 specialist attacker versus balanced defender (about +27 relevant-stat edge), ability level 10;
4. level-20 balanced attacker versus specialist defender (about -27 edge), ability level 10.

Single-target damaging moves use a representative 75% attack gate before the status save. Pure control and `PointRadius` AoE status packages use a 100% delivery gate because the current AoE resolver does not make the ordinary single-target accuracy roll.

Candidate DC:

```text
StatEdge = clamp(trunc((AttackerControlStat - DefenderSaveStat) / 5), -6, +6)
MasteryBonus = floor(AbilityLevel / 4)
DC = TierOffset + StatEdge + MasteryBonus
TierOffset C/B/A/S = 13/10/8/7
nat 1 save -> status lands; nat 20 -> resisted
```

## Monte Carlo aggregate results

| Tier / delivery | Equal L0 | Equal L10 | L20 specialist attacker L10 | L20 specialist defender L10 |
|---|---:|---:|---:|---:|
| C, attack-gated | 45.1% | 52.5% | 71.2% | 33.8% |
| B, attack-gated | 33.8% | 41.2% | 60.0% | 22.6% |
| B, single-gate | 45.1% | 55.1% | 79.9% | 29.9% |
| A, attack-gated | 26.2% | 34.0% | 52.3% | 15.2% |
| A, single-gate | 34.9% | 45.0% | 70.0% | 20.0% |
| S, attack-gated | 22.4% | 29.8% | 48.8% | 11.2% |
| S, single-gate | 29.9% | 39.9% | 65.0% | 15.0% |

Results track the exact discrete d20 expectations. The model therefore preserves the intended reliability ladder while letting specialization matter strongly without making S-tier hard control automatic.

## Full-roster sustain test

For each direct-status ability, candidate slots and the new minimum resource floor were applied **only upward**—an ability already above its tier floor was not reduced. Existing Elemental ×1.75 resolver cost was retained and counted once. Repetition strain remains active after the second use of the same ability.

Representative resource formulas:

```text
Max Stamina = 20 + FORT*5
Max Chakra = 50 + CHA*10
Ability L10 authored resource cost = base * 1.50
Repetition: first 2 same-ability uses free of strain; 3rd+ adds +50% per overage step
Round budget = 5 action slots
```

### Resource stat 10

Same-ability maximum uses in one five-slot round after candidate floors/slots:

- C tier: 3–4 uses depending on current cost/family.
- B tier: mostly 4–5; two expensive packages are lower.
- **A tier: all 18 direct-status abilities cap at exactly 2 uses.**
- S tier: 4 pure/single-gate hard controls cap at 1 use; 7 ordinary S attacks cap at 2; Sweeping Low alone reaches 3 because it intentionally remains 1 slot.

### Resource stat 20

- A tier still caps at exactly 2 uses because slots, not resource pool, are the anti-spam gate.
- S pure control remains 1 use and ordinary S attacks remain 2.
- Sweeping Low can reach 4 repeated uses only on a heavily FORT-invested base-level character; repetition strain makes the fourth use consume the entire round's large Stamina pool. Its intended mixed Karate string uses it once.

## S-tier anchors at resource stat 10

| Ability/package | Candidate slots | Base same-ability uses | Ability-L10 same-ability uses |
|---|---:|---:|---:|
| Shatter Punch (S + GB) | 2 | 2 | 1 |
| Killing Intent (pure S) | 3 | 1 | 1 |
| Sonic Sweep | 2 | 2 | 2 |
| Hydro Cannon Palm | 2 | 2 | 2 |
| Kneel (pure S) | 3 | 1 | 1 |
| Mausoleum | 2 | 2 | 2 |
| Bubble Prison | 2 | 2 | 2 |
| Siren's Lure (pure S) | 3 | 1 | 1 |
| Escapism (pure S) | 3 | 1 | 1 |
| Heavenly Kick | 2 | 2 | 2 |
| Sweeping Low | 1 | 3 | 2 |
| Hilt Bash (S + GB) | 2 | 2 | 1 |

This is the desired simultaneous behavior: action slots enforce hard frequency ceilings, while resource cost and mastery growth determine whether the fighter can actually pay for the maximum allowed repetitions.

## Resource-family result

The clean-attack audit remains important when interpreting these sustain numbers:

- melee Stamina clean-damage median resolver spend: 10;
- ranged Stamina: 20;
- Chakra: 35.

Chakra pools are larger than Stamina pools at equal CHA/FORT, but both regenerate at the same raw formula. Higher numerical Chakra prices therefore create slower replacement time even when the caster has more opening burst capacity. The action-slot model prevents A/S control from converting that larger opening pool into unlimited same-round hard-control spam.

## Current recommendation

The `/5 stat edge, ±6 cap, +floor(abilityLevel/4)` DC model plus the owner resource ladder and tier-based slot pressure is now internally coherent across the full requested roster.

Before changing runtime values roster-wide, the remaining balance tasks are:

1. choose attacker control-stat identity per status ability;
2. decide whether any of the ten currently automatic hostile riders are intentional exceptions;
3. establish the extra-target/AoE premium above the single-gate floor;
4. establish resource-drain tiers;
5. establish harmful Trap Supply premiums;
6. fix AI planner scoring so damaging status riders receive both damage and expected-control value;
7. then apply candidate costs/slots/DCs to a test branch and run actual engine battles, not just probability/economy simulations.