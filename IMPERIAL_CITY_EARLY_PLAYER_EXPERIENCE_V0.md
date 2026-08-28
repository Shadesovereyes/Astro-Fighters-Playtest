# Astro Fighters — Imperial City Early Player Experience v0

**Status:** Active production plan  
**Target game:** Open-world, real-time action-combat RPG  
**Runtime:** Phaser/browser under `/docs`  
**Completion inventories:** world and character production checklists  
**Machine contract:** `production/asset-manifest.json`

This document owns **route scope, production priority, composition requirements, and execution order**. It does **not** own asset completion state. Mark assets complete only in the world/character checklists after qualifying Phaser-integrated review.

---

# 1. Purpose

Turn the current browser prototype into one connected, production-quality Imperial City early-game route rather than trying to finish the entire city before testing.

First playable route:

> **SOUTHERN HARBOR ARRIVAL → DOCKS / SHIPWRIGHT → MARKET / SHOPPING STREET → RESIDENTIAL / CANAL TRANSITION → ASTRO FIGHTER ACADEMY EXTERIOR → ACADEMY INTERIOR / SENSEI TUTORIAL**

This route must establish:

- coherent city traversal;
- interaction and commerce;
- paper-doll character presentation;
- role-specific NPC population;
- foreground/background occlusion;
- interiors/cutaways;
- early real-time combat;
- the Academy tutorial progression.

Tutorial intent remains:

- Sensei introduces the combat foundation;
- General/Trap ability access is introduced;
- player receives **100 mon**;
- player chooses **3 distinct trap types, 10 of each**;
- inventory/paper-doll/action-RPG state reflects the issue.

The Harbor should visually support the later shipwright/boat system, but crab-island/cave production is outside this milestone gate.

---

# 2. Definition of Done

Imperial City Early Player Experience v0 is complete only when:

- the player traverses Harbor → Market → Residential/Canal → Academy exterior → Academy interior in Phaser;
- the route reads as one city rather than disconnected test rooms;
- normal exploration uses continuous real-time movement;
- the hidden 32×32 grid is not persistently visible or inferable;
- environments are assembled from modular Phaser layers rather than baked district backgrounds;
- player and visible NPCs are fully dressed and production-quality;
- collision, walk-behind depth, foreground occlusion, and authored cutaways work live;
- shops, doors, signage, dialogue targets, and tutorial interactives read clearly;
- early combat enters/exits without switching to a turn-based presentation;
- player readability survives every major material/lighting condition;
- integrated review has zero automatic failures;
- all critical rubric minimums pass;
- the route scores **42+** before checklist completion is recorded;
- **46+** remains the lock-quality target for assets that seed later city production.

---

# 3. Production priority

## P0 — Shared foundation and playable benchmark

These dependencies block efficient downstream production.

### P0-A — Shared-foundation world kit

The active manifest contracts 14 world dependencies:

1. `stone-clean`
2. `stone-cracked`
3. `stone-patched`
4. `stone-timber-transition`
5. `building-threshold`
6. `drainage-channel`
7. `drainage-grate`
8. `cracks`
9. `stains`
10. `cart-wear`
11. `timber-post`
12. `horizontal-beam`
13. `timber-plaster-wall`
14. `aged-stone-foundation`

These establish the first shared material/architecture language. Their exact dimensions, anchors, layer roles, collision/occlusion roles, and runtime destinations live in `production/asset-manifest.json`.

### P0-B — Shared architecture needed by the route

After Slice 0 proves the foundation, prioritize route-critical shared architecture before district-specific duplication:

- heavy/sliding doors;
- shopfront shutters;
- lattice/paper windows;
- roof straight/corner/ridge/eave/cutaway starter set;
- low foreground wall/cutaway;
- veranda and railing;
- exterior stairs and raised platform;
- narrow bridge module;
- small gate;
- sign mounts/signboards;
- noren-style curtain;
- restrained lantern fixtures;
- wall notices/charm strips.

### P0-C — Shared prop minimum

Create only enough shared props to make the early route feel inhabited:

- crate family;
- barrel;
- basket;
- sack;
- rope coil;
- bucket;
- stool/bench/small table;
- handcart;
- cleaning-tool bundle;
- fabric bundle;
- notice board;
- lantern pole;
- debris grouping;
- potted plant;
- shrub/grass clusters.

### P0-D — Playable character benchmark

Complete the contracted male benchmark source authorities:

- eight-direction base-underlayer turnaround;
- eight-direction fully dressed benchmark turnaround;
- modular layer source set;
- clean source assembly matching the benchmark;
- source isolation/anchor QA;
- target-resolution derivation and manual pixel cleanup;
- idle/walk/ready coverage;
- actual Phaser paper-doll integration.

Benchmark identity:

- brown-skinned male fighter;
- short Afro;
- sleeveless fighter wrap;
- short utility jacket;
- loose fighter trousers;
- sneaker-hybrid martial shoes;
- cloth sash;
- wrist wraps;
- neck cord/charm;
- no weapon required for this first benchmark.

Locked contract facts remain in the manifest: `480×640`, center `[240,600]`, foot-contact `y=600`, runtime `48×64`, pivot `[24,60]`, canonical eight directions.

### P0-E — Female base parity

Produce the corresponding female base-underlayer on the same lattice and direction system:

- body/skin;
- hair/face;
- base shorts;
- sports bra;
- all eight directions;
- same anchor/contact rules;
- compatibility with the shared modular clothing contract.

---

# 4. Slice 0 — Foundation Courtyard

Slice 0 is the immediate visual/runtime proof before Harbor production expands.

It must be assembled in the **actual Phaser runtime** from separate assets and include:

- Imperial stone ground;
- crack/stain/cart-wear treatment as appropriate;
- street/building threshold;
- drainage channel/grate;
- aged stone foundation;
- timber/plaster wall;
- timber post;
- horizontal beam;
- one restrained sign/lantern/noren-style dressing cue;
- one foreground occluder;
- fully dressed benchmark player.

It must prove:

- character/world style homogeneity;
- flat-faced 3/4 cabinet projection;
- continuous movement at correct gameplay scale;
- hidden-grid concealment;
- separate collision;
- live depth sorting/occlusion;
- source → runtime asset pipeline;
- crisp coherent pixel density.

A presentation board, collage, source assembly, or mock renderer cannot satisfy this gate.

---

# 5. P1 route composition requirements

These are **scene requirements**, not completion checkboxes. The world/character checklists own completion state.

## P1-A — Imperial Harbor Arrival

Minimum scene identity:

- stone quay and dock planking;
- water edge/animation;
- shipwright or harbor-office frontage;
- small warehouse/loading structure;
- cargo awning/loading platform;
- restrained hoist/loading infrastructure;
- mooring/rope infrastructure;
- nets, sacks, crates, rope bundles, weathered tarp, trade clutter;
- one production-quality small skiff/player-boat visual;
- one larger docked vessel silhouette;
- shipwright work area and dialogue target;
- fully dressed player;
- at least three dressed Harbor NPCs;
- one meaningful walk-behind foreground element;
- clear route inward toward Market.

Harbor surfaces should use waterline darkening, salt wear, algae, and localized dampness while remaining matte and non-cyberpunk.

Priority NPC roles:

- shipwright;
- dockworker;
- merchant or fisher;
- harbor guard.

## P1-B — Civic Market / Shopping Street

Minimum scene identity:

- busy civic stone street plus narrower passage/alley;
- several distinct timber storefront silhouettes;
- open/closed shop variations;
- sign/noren/awning language;
- at least three vendor archetypes (food, textile, medicine/herb);
- readable merchandise and delivery clutter;
- one working shop interaction with currency/item flow;
- fully dressed player;
- merchant, food seller, courier, shopper/street youth, civic guard;
- foreground canopy/sign occlusion;
- player readability at full detail.

## P1-C — Residential / Canal Transition

Minimum scene identity:

- dense small homes/row housing;
- canal-side residence condition;
- narrow alley plus canal crossing;
- balcony/exterior stair/laundry elements;
- household storage/cooking/water clutter;
- plants and small domestic details;
- canal wall, narrow bridge, steps/railing, washing platform;
- civilian population;
- clear continuation toward Academy.

Priority NPC roles:

- civilian adult;
- elder;
- teen/youth;
- household worker or local shopkeeper.

## P1-D — Astro Fighter Academy Exterior

Minimum scene identity:

- ceremonial main gate and perimeter definition;
- dojo/training/admin architecture;
- training courtyard/earth and stone transitions;
- veranda/walkway/roof family;
- target/dummy/practice posts;
- weapon/practice equipment storage;
- banners/insignia/notices;
- students visibly training;
- multiple dressed Academy NPCs;
- foreground architecture/roof occlusion;
- clear readable paths.

Priority NPC roles:

- students;
- senior student;
- instructor;
- groundskeeper/attendant.

## P1-E — Academy Interior / Sensei Tutorial

This must be a real room/cutaway gameplay space, not a menu-only scene.

Minimum scene identity:

- dojo floor/corridor;
- paper screens and structural columns;
- authored back/side/front walls;
- room-based roof removal/cutaway;
- training/storage props;
- Sensei area;
- equipment/trap issue area;
- fully dressed Sensei/students;
- dialogue/combat teaching trigger;
- General/Trap unlock presentation;
- 100 mon grant;
- 3 trap types ×10 selection;
- inventory verification;
- tutorial completion state.

No per-cell visibility reveal.

---

# 6. Character/NPC production order

Do not produce every profession before the v0 route.

Order:

1. male and female player foundations;
2. short Afro plus at least one additional priority hairstyle;
3. benchmark player outfit and animations;
4. Harbor role set;
5. Market role set;
6. Residential civilian set;
7. Academy student/instructor/Sensei set.

Controlled modular reuse is allowed when role identity remains clear. Do not populate the city by palette-swapping one silhouette.

---

# 7. Gameplay-facing integration requirements

## Traversal

- correct eight-direction facing;
- no pivot drift;
- continuous movement;
- credible collision at doors, bridges, stairs, alleys, quay edges, and verandas;
- authored foreground fade/cutaway only where needed;
- no grid-shaped visibility behavior.

## Paper doll / equipment

- clothing layers remain registered in all directions;
- anatomical equipment side remains correct;
- inventory/equipment changes alter visible layers where supported;
- no coarse whole-body overlays hiding anatomy incorrectly.

## Interaction

- NPCs, shopkeepers, shipwright, Sensei, doors, notices, and other interactables read without generic glowing clutter.

## Live combat

- ready/combat state transitions from exploration naturally;
- attack/action silhouettes remain readable against city materials;
- tutorial combat space supports real-time movement;
- telegraphs do not expose the hidden grid as permanent scenery;
- foreground occlusion does not hide essential combat information.

## Day/night readiness

Early-route materials must survive both lighting conditions:

- readable daytime values;
- readable evening/night values;
- restrained warm sodium amber and weak cathode-green accents only where appropriate;
- dry/matte surfaces;
- no generic wet-reflective cyberpunk look.

---

# 8. Scene execution order

1. **Slice 0 — Foundation Courtyard**
2. **Slice 1 — Harbor Arrival**
3. **Slice 2 — Market Connection**
4. **Slice 3 — Residential / Canal Transition**
5. **Slice 4 — Academy Exterior**
6. **Slice 5 — Academy Interior / Tutorial**
7. **Slice 6 — Full Harbor-to-Academy Route Review**

Do not expand later districts while an upstream slice fails its critical gate.

---

# 9. Review gates

## Source gate

Before runtime derivation:

- reference target approved;
- source masters approved;
- modular assembly approved;
- isolation/anchor QA passes.

## Runtime-candidate gate

- correct target dimensions;
- manual target-pixel cleanup;
- hard alpha where required;
- no contamination;
- correct pivot/anchor;
- correct layer role;
- correct collision/occlusion metadata.

## Integrated gate

- works in Phaser, not only in isolation;
- continuous traversal works;
- character/world quality matches;
- hidden grid remains concealed;
- projection/depth work;
- district identity is clear;
- player/NPC silhouettes remain readable;
- zero automatic failures;
- all critical minimums pass.

## Completion gate

- **0–29:** rejected
- **30–36:** rework required
- **37–41:** internal candidate only; checklist remains open
- **42–45:** production approved; relevant checklist items may close
- **46–50:** lock-quality authority

---

# 10. Default production queue

This is the current execution order. It is not a second checklist.

### Queue A — Shared foundation

1. stone-clean
2. stone-cracked
3. stone-patched
4. stone-timber-transition
5. building-threshold
6. drainage-channel
7. drainage-grate
8. cracks
9. stains
10. cart-wear
11. timber-post
12. horizontal-beam
13. timber-plaster-wall
14. aged-stone-foundation
15. roof/eave/cutaway starter set
16. door/window/shutter starter set
17. sign/lantern/noren starter set
18. shared prop minimum set

### Queue B — Player benchmark

19. male base-underlayer turnaround
20. female base-underlayer turnaround
21. short Afro turnaround
22. dressed player benchmark turnaround
23. modular layer isolation
24. source QA
25. runtime 48×64 cleanup
26. idle animation
27. walk animation
28. ready animation
29. Phaser paper-doll integration

### Queue C — Harbor

30. quay/dock/water edge
31. warehouse/shipwright frontage
32. loading/cargo set
33. boat silhouettes
34. Harbor NPC clothing set
35. Harbor integrated test

### Queue D — Market

36. storefront family
37. signage family
38. three-stall family
39. merchandise set
40. Market NPC clothing set
41. shop interaction art support
42. Market integrated test

### Queue E — Residential / Canal

43. residence family
44. canal wall/bridge/steps
45. household clutter/laundry set
46. civilian clothing set
47. Residential integrated test

### Queue F — Academy

48. gate/wall/dojo exterior
49. training-ground surfaces/props
50. Academy branding
51. student/instructor/Sensei clothing sets
52. Academy exterior integrated test
53. dojo/interior cutaway kit
54. Sensei/equipment/trap-issue area
55. tutorial interaction integration
56. Academy interior integrated test

### Queue G — Final route

57. connect all zones
58. tune collision/occlusion
59. populate route
60. verify shops/dialogue/paper doll
61. verify day/night readability
62. verify live-combat readability
63. full-route rubric review
64. repair failures
65. re-score until 42+
66. update only verified checklist/manifest completion state

---

# 11. Scope guardrails

Before the Harbor-to-Academy route is coherent, do not derail production into:

- full Palace production;
- full industrial/infrastructure corridors;
- every shrine package;
- every shop profession;
- every boat class;
- every city NPC profession;
- remote crab-island/cave environments;
- complete wildlands/bandit zones;
- final late-game VFX;
- art for systems not visible in the early-player route.

---

# 12. Immediate next deliverable

**Slice 0 — Foundation Courtyard in the actual Phaser runtime.**

The next valid integrated preview must come from the running Phaser canvas after the minimum world refactor and source/runtime gates are satisfied.
