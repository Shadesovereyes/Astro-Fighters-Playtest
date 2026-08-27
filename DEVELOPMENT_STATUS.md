# Astro Fighters — Current Development Status

**Updated:** 2026-08-27  
**Working branch:** `development/art-review-workflow-v1`  
**Draft PR:** #11

## Current game architecture

Astro Fighters is being developed as an **open-world, real-time action-combat RPG**.

The active public gameplay implementation is the **Phaser/browser RPG runtime under `/docs`**. Development should advance that runtime, its open-world traversal, real-time action combat, character systems, world integration, and production art.

The private `Shadesovereyes/Astro-Fighters` Unity project is a **legacy turn-based tactical Combat Strategy vertical slice**. It is not the current game, target runtime, scene architecture, or roadmap. It may be consulted for reusable combat design logic and math, but those systems must be translated into real-time action-RPG semantics.

Reusable ideas from the Unity slice may include damage/mitigation, stamina/chakra, poise/stagger, statuses/CC, stealth/awareness, grapples, counters, summons, Seigan, astrology affinities, ability data, and balance assumptions. Do **not** port its round loop, five-action slot queue, dynamic turn scheduler, hex encounter structure, IMGUI presentation, or Unity battle/recovery scenes as though those define the RPG.

If repository assumptions conflict, the current public RPG runtime and current locked production documents take precedence over legacy Unity implementation details.

## Current production state

No world or character checklist item is currently recorded as rubric-approved/struck through. Existing runtime art must therefore be treated as unapproved until an integrated Phaser review passes the mandatory gate.

The active art package remains **pre-art / contracted**. No checklist item was marked complete during the workflow/QA engineering work on this branch.

## Repository boundary

This repository is the **current public open-world action-RPG playtest/runtime surface and art-production control surface** described by the root README. It records the current runtime, contracts, acceptance rules, logical source registration, runtime destinations, review tooling, and handoff state.

Do not redirect gameplay development into the private Unity Combat Strategy vertical slice merely because its combat engine is more mature in some areas. Extract reusable mechanics from it only when they help the current real-time RPG.

Source art may be authored or retained outside this public runtime repository, but do not assume the private Unity Combat Strategy repository is the source-art authority. The public manifest, locked art direction, checklists, runtime paths, and integrated review state define what the current RPG expects.

Do not substitute generated/procedural placeholder art merely to satisfy a source path. The locked source workflow still applies wherever source-authority art is produced.

## Active dependency package

`AF-IC-SHARED-FOUNDATION`

The package contract in [`production/asset-manifest.json`](./production/asset-manifest.json) is now complete enough to begin source production. It locks:

- canonical `N, NE, E, SE, S, SW, W, NW` facing order;
- 480×640 per-direction character source canvas;
- shared character body center `[240,600]` and foot-contact line `y=600`;
- 48×64 runtime benchmark frame and pivot `[24,60]`;
- 10× world source-to-runtime scale for this package;
- source/runtime dimensions for every shared-foundation world dependency;
- world layer role, palette/material families, anchor, collision role, occlusion role, and stable runtime path;
- explicit `{direction}` source patterns for base-underlayer and dressed benchmark masters;
- explicit `{layer}/{direction}` modular character source registration;
- fully dressed unarmed Academy street-fighter benchmark outfit and palette families;
- the mandatory source gate that blocks runtime derivation until reference, modular assembly, and isolation/anchor QA pass.

The package remains `contracted`; its actual source images are still missing/unapproved.

## Runtime / workflow engineering completed in this branch

- Clarified in the root README that the target game is an open-world real-time action RPG and that the private Unity project is a legacy turn-based Combat Strategy vertical slice/reference.
- Extracted the v4 launcher hotfix from inline HTML into `docs/js/playtest-v4-patch.js` without intentionally changing behavior.
- Reduced `docs/play-v4.html` to a stable launcher that loads the versioned patch file.
- Added `docs/art-review.html`, a GitHub Pages review surface that enforces automatic-failure and critical-minimum rules.
- Added `docs/data/art-review-rubric.json` as the machine-readable scoring authority used by the review surface.
- Synced the browser rubric with the revised Master Prompt automatic failures for anatomical equipment routing, clothing occlusion, contaminated modular isolates, and uncleaned automatic reductions.
- Added `production/asset-manifest.json` as the single-current-state registration/production contract.
- Added `tools/validate-production.mjs` to reject drift in canonical direction rules, source/runtime dimensions, package registration, score gates, and approval evidence.
- Added `tools/validate-source-png.mjs` for PNG-level QA of contracted world and character assets. It checks expected dimensions, RGBA format, hard alpha, non-empty pixels, transparency where required, and reports registration/contact/color diagnostics.
- Added `.github/workflows/validate-production.yml` so GitHub Actions syntax-checks the QA/browser scripts and runs the production contract validator on pushes and pull requests.

## Combat Strategy adaptation rule

When a mechanic is brought forward from the Unity Combat Strategy vertical slice, perform an explicit adaptation pass before integrating it into the RPG:

1. identify the mechanic's design intent and reusable math;
2. remove assumptions that depend on turns, slots, or a closed hex encounter;
3. define its real-time trigger/timing model;
4. define movement, collision, animation commitment, hit window, interrupt, recovery, cooldown/resource, and AI implications as applicable;
5. implement it in the Phaser action-RPG runtime;
6. validate it in live movement/combat rather than judging it by Unity vertical-slice behavior alone.

The Unity slice is a source of **combat knowledge**, not a second active game that should be developed in parallel.

## Source QA commands

World source example:

```bash
node tools/validate-source-png.mjs world stone-clean source path/to/stone-clean.png
```

World runtime candidate example:

```bash
node tools/validate-source-png.mjs world timber-post runtime path/to/timber-post.png
```

Character source example:

```bash
node tools/validate-source-png.mjs character S source path/to/base-underlayer/S.png base
```

Character dressed benchmark example:

```bash
node tools/validate-source-png.mjs character NE source path/to/dressed-benchmark/NE.png dressed
```

The PNG tool is diagnostic/contract enforcement only. Passing it does not make an asset production-approved; source comparison, target pixel cleanup, Phaser integration, and the mandatory integrated rubric still remain downstream gates.

## Next production gate

Continue the **current Phaser open-world action RPG**, while creating and approving the narrow art dependencies needed for the next representative gameplay slice:

1. inspect the current `/docs` RPG state and identify the next gameplay dependency for a representative open-world/action-combat test;
2. adapt any required combat logic from the legacy Combat Strategy slice into real-time semantics rather than continuing the Unity prototype;
3. create the shared Imperial stone / threshold / drainage material slice;
4. create the shared timber-post / beam / plaster-wall / stone-foundation architectural slice;
5. create eight separate canonical base-underlayer masters on the shared 480×640 lattice;
6. create eight separate fully dressed benchmark masters on that same lattice;
7. register the modular source component set to the benchmark;
8. perform PNG isolation / dimension / hard-alpha QA plus visual source-assembly QA;
9. approve source art;
10. derive and manually clean the 48×64 / target-resolution runtime art;
11. integrate gameplay logic and art into the Phaser action-RPG runtime using stable public paths;
12. run the integrated rubric review using `/docs/art-review.html`;
13. only at 42+ with no automatic failures and all critical minimums passing, strike corresponding art checklist items.

If any upstream gate fails, repair it before continuing downstream. Git history is the iteration archive; keep only current authorities and current handoff state.