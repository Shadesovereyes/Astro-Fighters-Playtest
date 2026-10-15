# Astro Fighters — Palm Healing 75% Output Test

_Date: 2026-08-13._

## Test rule

Palm Healing remains 1 slot with unchanged Chakra cost and access rules. After normal ability-level scaling, its Heal effect is multiplied by **0.75**. At L45/A10 this is approximately **38 HP -> 29 HP** per cast. Combat is uncapped and ends only by elimination or simultaneous double KO; repeated exact states are test failures, not draws.

Ordinary Sign/Martial/Weapon fighters do **not** automatically receive Palm Healing. The main balance test therefore uses a support-persona Universal Arts fighter that actually knows Palm Healing against ordinary kits that do not.

## Direct support comparison — L45 Mental Defense

| Palm output | Support win rate | Avg rounds | Median | P95 | Max |
|---|---:|---:|---:|---:|---:|
| 100% | 82.7% | 11.74 | 11 | 17 | 33 |
| **75%** | **66.7%** | **11.25** | **11** | **15** | **23** |
| 50% | 29.2% | 7.53 | 8 | 9 | 11 |

75% is a much healthier midpoint than either prior endpoint in this proxy: full Palm is dominant, while 50% severely underperforms.

## Five-profile support sweep

The 75% support fighter was then tested against every other kit under each legal L45 profile, 168 battles/profile (840 total).

| Profile | Win rate | Avg rounds | Median | P95 | Max |
|---|---:|---:|---:|---:|---:|
| Balanced | 38.7% | 7.53 | 7 | 10 | 11 |
| PhysicalOffense | 23.8% | 4.91 | 5 | 6 | 8 |
| ControlOffense | 82.7% | 10.44 | 10 | 16 | 32 |
| PhysicalDefense | 38.7% | 7.08 | 7 | 9 | 10 |
| MentalDefense | 66.1% | 11.14 | 11 | 16 | 27 |

Across all five profiles, 75% Palm produced an aggregate **50.0% win rate** and **8.22 average rounds**. The variation is build-driven: high INT/CHA Control Offense and Mental Defense profiles make substantially better support chassis than Physical Offense. That is consistent with healing being a learned support investment rather than a universally optimal action.

## Artificial universal-heal sensitivity check

For continuity with the older stress harness, the seven previously long contexts were also rerun while artificially giving those fighters Palm Healing. This is **not** the intended access model, but it shows output sensitivity:

- Full-Palm candidate baseline: **26.14 rounds** average.
- 75% Palm: **8.15 rounds** average.
- 50% Palm: **7.42 rounds** average.
- No automatic Palm: **7.30 rounds** average.

Thus even 75% output largely removes the pathological universal-healing loop, but the more important correction is still the access rule: ordinary builds should not receive Palm Healing automatically.

## Result

**75% is the strongest candidate tested so far for Palm Healing itself.** It avoids the support collapse seen at 50% and reduces the dominance/long sustain seen at 100%. However, do not lock it solely from this proxy: final approval should test explicitly authored support loadouts and team fights where healing allies is part of the role.

No live runtime Palm Healing value was changed by this test.
