# Astro Fighters — Palm Healing 70% + Team Combat Test

_Date: 2026-08-13._

## Scope
Palm Healing remains 1 slot and keeps current Chakra cost/access. Test output is 70% after normal progression scaling (L45/A10: about 38 HP -> 27 HP). Ordinary Sign/Martial/Weapon fighters do not automatically receive Palm Healing. Combat is uncapped and elimination-only.

## Team-AI harness correction
Current runtime `planFor()` values a Heal only when the healer itself is below 55% HP. The team harness corrects this for testing so a support AI values healing when any living ally is below 55% HP. Runtime AI is unchanged.

## 1v1 support sweep
840 uncapped L45 battles at 70%, compared with the prior same-seed 75% sweep.

| Profile | 70% win | 70% rounds | 75% win | 75% rounds |
|---|---:|---:|---:|---:|
| Balanced | 36.3% | 7.46 | 38.7% | 7.53 |
| Physical Offense | 23.8% | 4.89 | 23.8% | 4.91 |
| Control Offense | 82.1% | 10.25 | 82.7% | 10.44 |
| Physical Defense | 38.7% | 7.05 | 38.7% | 7.08 |
| Mental Defense | 40.5% | 8.46 | 66.1% | 11.14 |
| Overall | 44.3% | 7.62 | 50.0% | 8.22 |

70% meaningfully reduces solo self-sustain, especially Mental Defense, while leaving most other profiles close to 75%.

## 2v2 replacement-value test
Format: Support + kit K vs kit K + kit K. Support uses Control Offense or Mental Defense; the other fighters use legal L45 Balanced builds. Support starts behind its ally. 336 battles per Palm value.

| Palm | Support-team win | Avg rounds | Palm casts/battle |
|---|---:|---:|---:|
| No Palm | 43.2% | 7.79 | 0.00 |
| 70% | 59.2% | 8.44 | 1.68 |
| 75% | 61.6% | 8.46 | 1.93 |

At 70%, Control Offense support teams win 46.4% and Mental Defense support teams 72.0%. Palm contributes about +16.1 percentage points over the no-Palm control.

## 3v3 backline-support test
Format: Support + 2x kit K vs 3x kit K. Support is one row behind two frontline allies; enemy formation is mirrored. 168 battles per Palm value.

| Palm | Support-team win | Avg rounds | Palm casts/battle |
|---|---:|---:|---:|
| No Palm | 66.1% | 7.06 | 0.00 |
| 70% | 74.4% | 7.24 | 1.85 |
| 75% | 75.0% | 7.26 | 2.00 |

70% and 75% are effectively equivalent in this team-size sample. The no-Palm support proxy is already strong, so other Universal support/utility tools account for much of the 3v3 result; 70% Palm adds about +8.3 points.

## Result
70% is the preferred test value over 75% in this pass: it preserves nearly all team contribution while reducing healer dueling/self-sustain. Team TTK remains around 7–8.5 rounds and does not recreate the former universal-healing TTK pathology.

This is still a provisional balance candidate. No live Palm Healing value or runtime AI behavior was changed.