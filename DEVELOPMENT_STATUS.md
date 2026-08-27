# Astro Fighters — Current Development Status

**Updated:** 2026-08-27  
**Working branch:** `development/art-review-workflow-v1`

## Current production state

No world or character checklist item is currently recorded as rubric-approved/struck through. Existing runtime art must therefore be treated as unapproved until an integrated Phaser review passes the mandatory gate.

## Active dependency package

`AF-IC-SHARED-FOUNDATION`

The package is contracted in [`production/asset-manifest.json`](./production/asset-manifest.json). It pairs the first shared Imperial City surface/architecture dependencies with the first fully dressed fighter benchmark so character and world quality advance together.

The package remains **contracted / missing source art**. Do not mark its checklist items complete until the integrated Phaser result scores 42+ with no automatic failures and all critical minimums satisfied.

## Runtime engineering completed in this branch

- Extracted the v4 launcher hotfix from inline HTML into `docs/js/playtest-v4-patch.js` without intentionally changing behavior.
- Reduced `docs/play-v4.html` to a stable launcher that loads the versioned patch file.
- Added `docs/art-review.html`, a GitHub Pages review surface that enforces automatic-failure and critical-minimum rules.
- Added `docs/data/art-review-rubric.json` as the machine-readable scoring authority used by the review surface.
- Added `production/asset-manifest.json` as the single-current-state registration/production manifest.

## Next production gate

Create and approve narrow source references for the active package before runtime derivation:

1. shared Imperial stone / threshold / drainage material slice;
2. shared timber-post / beam / plaster-wall / stone-foundation architectural slice;
3. eight-direction base-underlayer turnaround on the 480×640 lattice;
4. eight-direction fully dressed fighter benchmark on the same lattice;
5. modular source component set registered to the benchmark;
6. source assembly QA;
7. 48×64 / target-resolution cleanup;
8. Phaser integration;
9. integrated rubric review using `/docs/art-review.html`.

If any upstream gate fails, repair it before continuing downstream. Git history is the iteration archive; keep only the current accepted/active manifest and source authorities in the repository.
