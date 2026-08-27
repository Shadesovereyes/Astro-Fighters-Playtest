# Kairo — Package 07 Direction Convention

**Locked gameplay convention:** `S` is front-facing / toward camera. `N` is back-facing / away from camera.

This document resolves an earlier Package 07 labeling mistake. Some approved/reference sheets use direction labels that do not match the gameplay convention. Raw source art is not rotated or repainted simply to rename it; metadata maps each source slot to the correct canonical gameplay facing.

## Canonical gameplay facings

| Canonical facing | Visual orientation |
| --- | --- |
| `N` | back / away from camera |
| `NE` | back-right 3/4 |
| `E` | right profile |
| `SE` | front-right 3/4 |
| `S` | front / toward camera |
| `SW` | front-left 3/4 |
| `W` | left profile |
| `NW` | back-left 3/4 |

## Reference-sheet source-slot remap

The current Kairo reference sheets were previously interpreted with `N` as front. Preserve their source slots, but convert them to canonical game facings as follows:

| Reference/source slot | Canonical gameplay facing |
| --- | --- |
| source `N` | `S` |
| source `NE` | `SE` |
| source `E` | `E` |
| source `SE` | `NE` |
| source `S` | `N` |
| source `SW` | `NW` |
| source `W` | `W` |
| source `NW` | `SW` |

Inverse mapping:

- canonical `N` ← source `S`
- canonical `NE` ← source `SE`
- canonical `E` ← source `E`
- canonical `SE` ← source `NE`
- canonical `S` ← source `N`
- canonical `SW` ← source `NW`
- canonical `W` ← source `W`
- canonical `NW` ← source `SW`

## Consequences for Package 07

- Front-facing body/chest work is canonical `S`, not `N`.
- The clean-chest source slots `N / NE / E / W` correspond to canonical `S / SE / E / W`.
- Rear-facing inner-top suppression belongs to canonical `NE / N / NW`.
- The equipment sheet's absent source `NW` slot corresponds to missing canonical `SW` equipment art.
- Any historical Package 07 QA that says `N = front`, `S = back`, or calls the missing equipment direction `NW` is using the superseded source-slot convention.

## Runtime rule

All engine/Phaser-facing APIs, manifests, animation names, movement-facing state, and future 48×64 assets use **canonical gameplay direction names**. Raw source filenames may retain source-slot labels only when accompanied by an explicit `source_slot` field.

No new production metadata may rely on implicit direction interpretation.
