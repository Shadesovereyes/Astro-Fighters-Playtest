# Astro Fighters — Palm Healing 50% Output Test

_Date: 2026-08-13._

## Owner access clarification

Healing abilities are **not automatically part of every fighter kit**. Healing access is intended for support-focused AI and for players who explicitly find, learn, and choose to equip healing abilities. This means the previous all-kit stress harness materially overstated normal Palm Healing prevalence.

## Test interpretation

At ability level 10, the current progression system drives heals toward 1 HP per Chakra spent. Therefore this test applies the requested 50% reduction to **actual post-progression healing output**, not only to Palm Healing’s authored base 15. At L45/A10, Palm Healing is approximately 38 HP in the current model and approximately 19 HP in the 50% variant. Slots and Chakra cost remain unchanged.

All tests are uncapped and elimination-only. No still-active battle is classified as a draw.

## Long-context stress test (artificial: every fighter has Palm)

- Same paired-seed candidate sample: **294 battles per variant**.
- Baseline average TTK: **26.14 rounds**.
- 50% Palm average TTK: **7.42 rounds** (**-71.6%**).
- Removing automatic Palm entirely: **7.30 rounds**.

| Context | Baseline avg | Palm 50% avg | No automatic Palm avg |
|---|---:|---:|---:|
| Sign:Scorpio / ControlOffense | 28.33 | 6.81 | 6.60 |
| Weapon:Kyudo / MentalDefense | 27.43 | 7.62 | 7.29 |
| Sign:Sagittarius / ControlOffense | 24.81 | 8.48 | 8.33 |
| Martial:Judo / MentalDefense | 27.21 | 7.60 | 7.19 |
| Martial:MuayThai / MentalDefense | 31.00 | 7.43 | 7.36 |
| Martial:Karate / MentalDefense | 32.50 | 7.45 | 7.50 |
| Sign:Libra / ControlOffense | 11.71 | 6.55 | 6.83 |

The 50% result and no-automatic-heal result are nearly identical in ordinary-kit stress contexts. That strongly indicates the previous 25–30-round TTK problem was primarily caused by the harness granting mastered Palm Healing to every fighter, not by the candidate DC model alone.

## Already-fast physical contexts

- Candidate physical baseline: **6.47 rounds**.
- Palm 50%: **5.74 rounds**.
- No automatic Palm: **5.67 rounds**.

The 50% stress variant shortens physical fights, but they remain mostly in a usable multi-round range rather than collapsing into one-turn kills.

## Support-focused proxy

To account for the owner access rule, a separate proxy gave Palm Healing only to a support-persona Universal/Medical AI while ordinary opponent kits had no automatic Palm. Same L45/A10 Mental Defense build, candidate model, 8 mirrored seeds against every other kit.

| Palm output | Support win rate | Avg rounds | Median | P95 | Max |
|---|---:|---:|---:|---:|---:|
| Full | 82.7% | 11.74 | 11 | 17 | 33 |
| 50% | 29.2% | 7.53 | 8 | 9 | 11 |

The support proxy flips from very strong at full Palm to substantially underperforming at 50%. Because AI heal desirability is also based on heal magnitude, halving output both reduces HP restored and makes the AI select healing less often. This is a real gameplay consequence of the reduced power, but it means 50% is not a clean support-balance recommendation from this test alone.

## Gate result

1. **Do not use the old all-kit healing stress test as the normal combat model.** Automatic Palm access was contrary to the intended progression/loadout rules.
2. **Do not lock Palm Healing to 50% yet.** It cures the artificial universal-healing TTK loop, but in a support-only proxy it over-nerfs the support role.
3. The next support-specific calibration should compare full, 75%, and possibly 60–70% Palm output, with healing available only to support builds that actually learned/equipped it.
4. Ordinary Sign/Martial/Weapon TTK should be evaluated without automatically injecting Palm Healing into their loadouts.