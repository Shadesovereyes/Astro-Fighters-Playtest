# Kairo — Package 07 v35/v36 QA

> **Direction-convention correction (2026-08-27):** this historical QA uses reference-sheet/source-slot labels. Canonical gameplay uses `S = front`, `N = back`. The affected source slots `N / NE / E / W` correspond to canonical `S / SE / E / W`. The absent equipment source slot `NW` corresponds to canonical `SW`.

## v35 clean-chest body master candidate

The active base-body candidate removes the chest cross-bandage / X-wrap from the four affected **source slots**:

- source `N` → canonical `S`
- source `NE` → canonical `SE`
- source `E` → canonical `E`
- source `W` → canonical `W`

The correction is deliberately limited to the torso. Hair, face, shorts, wrist wraps, ankle/foot wraps, pose, proportions and the already-bare rear/diagonal source views remain sourced from the approved base-body reference.

v35 supersedes the earlier broad procedural cleanup experiments because it:
- copies only corrected torso regions rather than altering the whole character;
- expands the E/W correction to the complete chest edge;
- removes residual neutral/dark wrap speckles on source N/NE while preserving connected anatomy crease lines;
- keeps every direction on the shared 480×640 lattice (`x=240`, foot contact `y=560`).

This is an **active source candidate**, not production approval. The torso still needs final source-art review at full resolution before the body checklist item can pass.

## v36 integrated source test

v36 rebuilds all eight current dressed source candidates using:
- the v35 clean-chest body candidate;
- the accepted direction-specific manual garment placements from v29/v30/v31;
- independent belt-knot, pouch and gourd layers instead of the contaminated all-in-one sash.

The point of v36 is to verify that removing the chest wrap does not require returning to a coarse whole-garment overlay. The body remains split into core and late-visible anatomy so head, hands and feet can route in front where required.

v36 remains below source approval because:
- sleeve/cuff/hand seams still need per-facing polish;
- hairless body master is not authored;
- final weapon/scabbard placement still requires manual per-facing registration;
- four canonical SW equipment assets remain missing because source slot NW is absent;
- the complete source stack has not passed the final review gate.

## Runtime gate

**No 48×64 reduction yet.**

The locked sequence remains:

`SOURCE MASTER → DIRECTIONAL LAYER REVIEW → COMPLETE SOURCE APPROVAL → 48×64 NEAREST-NEIGHBOR DERIVATION → MANUAL PIXEL CLEANUP → PHASER`
