# Astro Fighters — DC Simulation Pass 02: Career-Stat Scaling

_Date: 2026-08-12. Simulation findings only._

This pass tests DC stat scaling against the actual career attribute-budget rules instead of arbitrary +/-5 stat examples.

## Career-stat reference points

The current career budget is base 6 in each stat, 14 spendable points at level 1, +5 points per later character level, with increasing marginal costs after 20/30/40/50.

Representative results from the existing allocation rules:

| Character level | Balanced relevant stat (approx.) | One-stat specialist maximum | Gap |
|---:|---:|---:|---:|
| 1 | 9 | 20 | 11 |
| 10 | 18 | 38 | 20 |
| 20 | 24 | 51 | 27 |
| 50 | 36 | 81 | 45 |
| 100 | 50 | 100 | 50 |

A fixed +/-4 DC cap on a 1-DC-per-4-stat model therefore saturates around level 10 for a specialist fighting a balanced defender. That would make later control-stat investment stop improving DC reliability too early.

## Candidate refinement: 1 DC per 5 relative stat points, cap +/-6

```text
StatEdge = clamp(trunc((AttackerControlStat - DefenderSaveStat) / 5), -6, +6)
MasteryBonus = floor(AbilityLevel / 4)
DC = TierOffset + StatEdge + MasteryBonus

TierOffset: C=13, B=10, A=8, S=7
Natural 1 on the save die = status lands
Natural 20 = status resisted
Otherwise d20 >= DC resists
```

Properties:

- equal investment remains exactly C 60%, B 45%, A 35%, S 30% at ability L0;
- each 5 relevant-stat advantage changes reliability by about 5 percentage points;
- specialization keeps improving through mid/high levels instead of saturating at level 10;
- the +/-6 cap limits the stat contribution to +/-30 percentage points;
- ability L10 currently adds +2 DC / +10 percentage points separately;
- even extreme hard-control specialization remains below automatic reliability.

## S-tier specialist vs balanced defender

| Character level | Relevant stat gap | S L0 | S ability L10 |
|---:|---:|---:|---:|
| 1 | +11 | 40% | 50% |
| 10 | +20 | 50% | 60% |
| 20 | +27 | 55% | 65% |
| 50 | +45 | 60% | 70% |
| 100 | +50 | 60% | 70% |

Thus a deeply specialized, fully mastered S-tier control user tops out around **70% save-failure reliability** against a balanced defender before attack-roll gating. A damaging S rider at a representative 75% hit chance would top out around **52.5% total raw-attempt proc rate** in that extreme matchup.

If the defender instead specializes heavily into the relevant save stat, the relationship reverses. Natural-1 protection ensures a nonzero landing floor; the candidate curve can push an unmastered S effect down to roughly 5% against a very large defensive stat edge, which is appropriate for a defender who has explicitly invested to counter that control axis.

## All-tier specialist progression

Specialist attacker versus balanced defender, using the same career-budget reference:

### Character level 1 (about +11 stat edge)

| Tier | L0 | ability L10 |
|---|---:|---:|
| C | 70% | 80% |
| B | 55% | 65% |
| A | 45% | 55% |
| S | 40% | 50% |

### Character level 10 (about +20 stat edge)

| Tier | L0 | ability L10 |
|---|---:|---:|
| C | 80% | 90% |
| B | 65% | 75% |
| A | 55% | 65% |
| S | 50% | 60% |

### Character level 20 (about +27 stat edge)

| Tier | L0 | ability L10 |
|---|---:|---:|
| C | 85% | 95% |
| B | 70% | 80% |
| A | 60% | 70% |
| S | 55% | 65% |

### Character level 50+ (stat-edge cap reached)

| Tier | L0 | ability L10 |
|---|---:|---:|
| C | 90% | 95% (natural-20 ceiling) |
| B | 75% | 85% |
| A | 65% | 75% |
| S | 60% | 70% |

## Interpretation

This curve currently looks healthier than the earlier half-stat and quarter-stat/+/-4-cap candidates:

- weak C-tier riders can become very reliable in the hands of a true specialist, which fits their 'common consequence' identity;
- B/A effects gain meaningful value from specialization without immediately becoming guaranteed;
- S hard control remains dangerous but cannot exceed about 70% even at extreme stat advantage plus max ability mastery;
- equal-investment matchups remain anchored to the owner-approved 60/45/35/30 ladder regardless of absolute character level;
- save-stat investment remains a real counter because the exact same relative formula works in the defender's favor.

## Remaining questions before approval

1. Whether the stat contribution cap should be +/-5 or +/-6 DC. +/-6 preserves more late-game specialization; +/-5 is more conservative.
2. Whether max ability mastery should stay +2 DC or use a nonlinear mastery curve.
3. Whether pure S control should use the same DC curve as S damaging riders or receive a separate reliability adjustment because it lacks the attack gate. The current cost/slot model already charges pure control more, so a separate DC penalty may not be necessary.
4. Which attacker control stat each ability should use. This should be authored by technique identity rather than globally forcing one stat.
5. Whether multiple-target/AoE control needs a DC penalty or whether its extra-target value should be paid entirely through resource/action cost.

The recommended next candidate for full Monte Carlo combat testing is therefore **relative stat edge / 5, capped at +/-6, plus floor(ability level / 4)**.