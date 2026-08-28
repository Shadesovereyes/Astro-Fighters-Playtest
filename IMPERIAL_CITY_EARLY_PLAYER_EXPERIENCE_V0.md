# Astro Fighters — Imperial City Early Player Experience v0

**Status:** Active production plan  
**Target game:** Open-world, real-time action-combat RPG  
**Runtime:** Phaser/browser playtest under `/docs`  
**Art authority:** `ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md`  
**World checklist:** `Astro Fighters — Imperial City Zone-by-Zone Asset Checklist.md`  
**Character checklist:** `ASTRO_FIGHTERS_CHARACTER_CLOTHING_ACCESSORY_CHECKLIST.md`  
**Review authority:** `Astro Fighters — Art Preview Review Rubric.md`  
**Production manifest:** `production/asset-manifest.json`

---

# 1. Purpose

This document defines the minimum world, city, character, and integration work required to turn the current browser prototype into a credible **Imperial City early-player experience**.

The goal is not to finish every Imperial City checklist item before testing. The goal is to finish one connected, representative early-game route at production quality, prove the art/runtime pipeline, and then expand from that proven slice.

The first playable route is:

> **SOUTHERN HARBOR ARRIVAL → DOCKS / SHIPWRIGHT → MARKET / SHOPPING STREET → RESIDENTIAL / CANAL TRANSITION → ASTRO FIGHTER ACADEMY EXTERIOR → ACADEMY INTERIOR / SENSEI TUTORIAL**

This route establishes the city, teaches traversal and interaction, introduces commerce and inventory, demonstrates the paper-doll character system in motion, and culminates in the Academy combat tutorial.

The early experience must support the already-defined tutorial intent:

- the player arrives through the Imperial Harbor;
- the player is guided toward the Astro Fighter Academy;
- the Sensei introduces combat and the General/Trap ability foundation;
- the Sensei grants **100 mon**;
- the player chooses **3 distinct trap types, 10 of each**;
- the player exits the tutorial with live-combat capability and a reason to return to the city world.

The harbor must also visually establish the shipwright / boat system that later connects the player to the crab-island / cave route. The city slice does not require those remote zones to be finished before the Imperial City v0 review.

---

# 2. Definition of Done

Imperial City Early Player Experience v0 is complete only when all of the following are true:

- the player can traverse the entire harbor-to-Academy route in the Phaser runtime;
- the route reads as one coherent Imperial City rather than disconnected test rooms;
- no visible 32×32 grid rhythm appears in the environment;
- the player character is fully dressed and production-quality in all required views;
- visible NPCs are fully dressed and role-specific rather than mannequin/base sprites;
- collision, walk-behind occlusion, cutaway behavior, and foreground layering work in live traversal;
- shops, signage, doors/thresholds, NPC dialogue targets, and Academy tutorial interactives are visibly represented;
- early combat can be entered and exited without changing to a turn-based presentation;
- the player remains readable against every major surface/material family;
- no automatic art-review failure is present;
- all critical rubric categories pass their minimums;
- the integrated early-player slice scores **42+** before checklist completion is recorded;
- **46+** is the lock-quality target for reference assets that will seed later city expansion.

A technically functional scene with placeholder art does not satisfy this milestone.

---

# 3. Production Priority Model

## P0 — Blocks all downstream production

P0 assets must be developed first because they are shared by multiple early-player zones or define the playable character benchmark.

### P0-A — `AF-IC-SHARED-FOUNDATION` world kit

The current manifest already contracts these assets. Complete them before district-specific duplication:

- [ ] `stone-clean` — Worn Imperial stone street — clean
- [ ] `stone-cracked` — Worn Imperial stone street — cracked
- [ ] `stone-patched` — Patched stone street
- [ ] `stone-timber-transition` — Stone-to-timber transitions
- [ ] `building-threshold` — Street-to-building threshold pieces
- [ ] `drainage-channel` — Drainage channels
- [ ] `drainage-grate` — Drainage grates
- [ ] `cracks` — Crack decals
- [ ] `stains` — Stain/grime decals
- [ ] `cart-wear` — Wheel/cart wear
- [ ] `timber-post` — Timber structural post
- [ ] `horizontal-beam` — Horizontal beam
- [ ] `timber-plaster-wall` — Timber-and-plaster wall
- [ ] `aged-stone-foundation` — Aged stone foundation

### P0-B — Shared architectural completion needed by the route

These are not all yet contracted in the manifest but are required immediately by the early-player route:

- [ ] heavy timber door
- [ ] sliding door
- [ ] shopfront shutters
- [ ] lattice window
- [ ] paper window
- [ ] roof straight segment
- [ ] roof corner
- [ ] roof ridge
- [ ] roof eave
- [ ] roof cutaway version
- [ ] low foreground wall / cutaway version
- [ ] veranda
- [ ] railing
- [ ] exterior stairs
- [ ] raised platform
- [ ] narrow bridge connection module
- [ ] small gate
- [ ] shop-sign mount
- [ ] vertical signboard
- [ ] horizontal shop sign
- [ ] hanging noren-style curtain
- [ ] lantern wall mount
- [ ] hanging lantern
- [ ] wall notices / charm strips

### P0-C — Shared prop minimum

Author enough props to make every early zone feel inhabited without producing the entire global prop checklist:

- [ ] small / medium / open crate set
- [ ] barrel
- [ ] basket
- [ ] sack
- [ ] rope coil
- [ ] bucket
- [ ] stool
- [ ] bench
- [ ] small table
- [ ] handcart
- [ ] broom / cleaning-tool bundle
- [ ] fabric bundle
- [ ] notice board
- [ ] lantern pole
- [ ] debris/trash grouping
- [ ] potted plant
- [ ] shrub / grass clusters

### P0-D — Playable character benchmark

Complete the existing manifest benchmark before producing many NPC variants.

**Base-underlayer source masters:**

- [ ] N
- [ ] NE
- [ ] E
- [ ] SE
- [ ] S
- [ ] SW
- [ ] W
- [ ] NW

**Dressed benchmark source masters:**

- [ ] N
- [ ] NE
- [ ] E
- [ ] SE
- [ ] S
- [ ] SW
- [ ] W
- [ ] NW

**Benchmark outfit:**

- [ ] sleeveless fighter wrap
- [ ] short utility jacket
- [ ] loose fighter trousers
- [ ] sneaker-hybrid martial shoes
- [ ] cloth sash
- [ ] wrist wraps
- [ ] neck cord / charm
- [ ] contact shadow

**Character production gates:**

- [ ] shared body center `[240,600]`
- [ ] foot-contact line `y=600`
- [ ] hard alpha
- [ ] no neighboring-layer contamination
- [ ] correct near/far garment routing per direction
- [ ] no front-facing body reuse disguised as diagonal/back views
- [ ] runtime 48×64 target cleanup after source approval
- [ ] 4-frame idle per direction
- [ ] 6-frame walk per direction
- [ ] 2-frame ready per direction
- [ ] Phaser integration

### P0-E — Female base / paper-doll parity

The early player experience must not lock the runtime to one body presentation. Produce the corresponding female base-underlayer using the same lattice and canonical directions:

- [ ] body / skin
- [ ] hair / face
- [ ] base shorts
- [ ] sports bra
- [ ] all 8 canonical directions
- [ ] shared anchor / contact rules
- [ ] compatible with the same modular clothing contract

The female base is not a separate art style. It must share the same world-scale, palette, rendering discipline, and paper-doll routing rules.

---

# 4. P1 — Early Route World / City Production

P1 creates the actual connected player route. Build only the minimum production-quality composition required to establish each zone convincingly.

## P1-A — Imperial Harbor Arrival

### Required world assets

- [ ] weathered dock planks
- [ ] stone quay
- [ ] algae-stained quay edge
- [ ] canal/water edge animation
- [ ] water surface animation
- [ ] steps descending toward water
- [ ] dock-to-street transition
- [ ] small warehouse facade + roof
- [ ] harbor-office / shipwright frontage
- [ ] cargo awning
- [ ] timber pier support
- [ ] covered loading platform
- [ ] mooring post / ring
- [ ] rope bollard
- [ ] cargo crane **or** manual hoist
- [ ] winch / hook assembly
- [ ] cargo ramp
- [ ] fishing net set
- [ ] cargo sacks / produce crates
- [ ] merchant crate variants
- [ ] rope bundles
- [ ] folded tarp
- [ ] harbor lantern
- [ ] weighing / trade prop
- [ ] one production-quality small skiff / player-boat visual
- [ ] one larger docked merchant/fishing vessel silhouette

### Shipwright interaction shell

- [ ] identifiable shipwright work area
- [ ] boat-repair tool grouping
- [ ] repair-material stack
- [ ] dialogue/interact marker location
- [ ] visual place for boat durability / repairs / cargo services to exist later without rebuilding the quay

### Minimum NPC roster

- [ ] shipwright
- [ ] dockworker
- [ ] merchant or fisher
- [ ] harbor guard

### Harbor integrated composition gate

The live scene must visibly include:

- [ ] fully dressed player
- [ ] at least 3 dressed NPCs
- [ ] warehouse / shipwright frontage
- [ ] quay + dock
- [ ] crane/hoist
- [ ] cargo clutter
- [ ] walk-behind foreground object
- [ ] water animation
- [ ] restrained industrial/analog element
- [ ] obvious route into the city
- [ ] no visible grid rhythm

---

## P1-B — Civic Market / Shopping Street

The market is the first proof that the city supports ordinary RPG interaction rather than functioning only as a combat map.

### Required world assets

- [ ] busy stone street variant
- [ ] narrow alley surface
- [ ] shop threshold
- [ ] market stain / food-spill decals
- [ ] merchant/chalk markings
- [ ] narrow timber storefront
- [ ] two-story storefront
- [ ] corner shop
- [ ] open-front market shop
- [ ] closed-shutter variant
- [ ] side-alley facade
- [ ] storefront roof variants
- [ ] hanging shop sign
- [ ] vertical sign
- [ ] painted wood sign
- [ ] cloth banner sign
- [ ] licensing / civic plaque
- [ ] minimum 3 stall archetypes: food, textile, medicine/herb
- [ ] stall canopy variants
- [ ] produce baskets / food display
- [ ] tea jars / bowls / bottles
- [ ] cloth bolts / folded clothing
- [ ] tools / herbs / medicine packets
- [ ] charms / beads
- [ ] merchant boxes
- [ ] merchant table / stool grouping
- [ ] delivery crates
- [ ] fabric hanging rack
- [ ] awning support poles

### Shop/inventory presentation requirement

At least one early shop must have enough art support to test:

- [ ] merchant dialogue
- [ ] shop inventory opening
- [ ] player currency display/use
- [ ] item acquisition
- [ ] visible environmental merchandise that corresponds to the role of the shop

### Minimum NPC roster

- [ ] general merchant
- [ ] food seller
- [ ] courier
- [ ] shopper / street youth
- [ ] civic guard

### Market integrated composition gate

- [ ] fully dressed player
- [ ] at least 5 NPCs
- [ ] at least 3 distinct storefront silhouettes
- [ ] at least 3 vendor stalls
- [ ] dense but readable merchandise
- [ ] signage
- [ ] foreground canopy occlusion
- [ ] narrow alley
- [ ] larger street opening
- [ ] player remains readable at full detail

---

## P1-C — Residential / Canal Transition

This zone prevents the harbor-to-Academy route from reading as one long commercial corridor and establishes the city as inhabited.

### Required world assets

- [ ] small residence
- [ ] two-story residence
- [ ] canal-side home
- [ ] row-house section
- [ ] narrow-alley house
- [ ] small balcony
- [ ] exterior stair
- [ ] laundry platform
- [ ] residential roof variants
- [ ] laundry line + hanging clothing
- [ ] shoe rack
- [ ] cooking-pot / water-bucket grouping
- [ ] family storage boxes
- [ ] potted plants
- [ ] small shrine shelf
- [ ] food-drying rack
- [ ] small canal wall
- [ ] narrow bridge
- [ ] residential canal steps
- [ ] drain outlet
- [ ] canal-side railing
- [ ] laundry/washing platform
- [ ] small canal boat

### Minimum NPC roster

- [ ] civilian adult
- [ ] elder
- [ ] teen/youth
- [ ] household worker or local shopkeeper

### Residential integrated composition gate

- [ ] narrow alley
- [ ] canal crossing
- [ ] dense vertical housing
- [ ] household clutter
- [ ] civilians
- [ ] readable player-scale architecture
- [ ] strong lived-in quality
- [ ] route continues visibly toward Academy

---

## P1-D — Astro Fighter Academy Exterior

The Academy must feel like a distinct institution inside the same city, not a detached dojo tileset.

### Required grounds

- [ ] swept courtyard stone
- [ ] packed training earth
- [ ] stepping stones
- [ ] garden strip
- [ ] practice-ring surface
- [ ] drainage
- [ ] path transitions

### Required architecture

- [ ] main ceremonial gate
- [ ] side gate
- [ ] perimeter wall
- [ ] main dojo exterior
- [ ] training hall
- [ ] administration frontage
- [ ] veranda
- [ ] raised timber walkway
- [ ] Academy roof set
- [ ] bell/gong structure
- [ ] banner mounts

### Required training / identity props

- [ ] straw target
- [ ] wooden training dummy
- [ ] practice posts
- [ ] weapon rack
- [ ] training mats
- [ ] sparring markers
- [ ] conditioning stones
- [ ] practice swords/staves
- [ ] Academy banners
- [ ] Astro Fighter insignia
- [ ] notice board / scroll posting
- [ ] lantern
- [ ] water basin
- [ ] shoe rack
- [ ] bench
- [ ] landscaping

### Minimum NPC roster

- [ ] student masculine silhouette
- [ ] student feminine silhouette
- [ ] senior student
- [ ] instructor
- [ ] groundskeeper / attendant

### Academy exterior integrated composition gate

- [ ] clear main-gate establishing view
- [ ] player
- [ ] multiple students
- [ ] visible active training
- [ ] Academy branding
- [ ] foreground veranda/roof occlusion
- [ ] clear walkable paths
- [ ] no visible grid rhythm

---

## P1-E — Academy Interior / Sensei Tutorial Space

This is the culmination of the v0 route and must be a real room/cutaway gameplay space rather than a separate menu screen.

### Required architecture

- [ ] dojo floor
- [ ] timber corridor
- [ ] sliding paper screens
- [ ] interior columns
- [ ] back walls
- [ ] cutaway side walls
- [ ] cutaway foreground wall
- [ ] roof-removal set
- [ ] storage-room wall variant

### Required tutorial props

- [ ] weapon racks
- [ ] scroll shelves
- [ ] teacher / Sensei area
- [ ] training mats
- [ ] scrolls
- [ ] storage chest
- [ ] lanterns
- [ ] wall banners / Academy notices
- [ ] equipment-issue rack
- [ ] trap pouch display
- [ ] trap stock crates
- [ ] curriculum display
- [ ] Academy foundation emblem

### Required tutorial interactions

- [ ] Sensei dialogue target
- [ ] combat teaching trigger
- [ ] General/Trap ability unlock presentation
- [ ] 100 mon grant presentation
- [ ] trap selection interaction: 3 distinct trap types ×10 each
- [ ] inventory verification after issue
- [ ] tutorial completion state

### Interior integration gate

- [ ] roof disappears by room / authored cutaway
- [ ] no per-cell visibility reveal
- [ ] foreground wall cuts away correctly
- [ ] player remains readable
- [ ] Sensei and students fully dressed
- [ ] interior feels furnished and used
- [ ] interior matches Academy exterior material language

---

# 5. P1 — Character / NPC Production Roster

Do not produce every profession in the full checklist before the v0 slice. Produce the roles that are visible on the route, then reuse the modular system for controlled variation.

## P1-CHAR-01 — Player character foundation

- [ ] male base-underlayer complete
- [ ] female base-underlayer complete
- [ ] short Afro complete in 8 directions
- [ ] at least one additional priority hairstyle complete in 8 directions
- [ ] benchmark street-fighter outfit complete
- [ ] paper-doll layers isolated and removable
- [ ] visible equipment attachment points validated
- [ ] idle / walk / ready complete
- [ ] movement integration complete

## P1-CHAR-02 — Harbor set

### Dockworker
- [ ] wrapped work top
- [ ] short utility outer layer
- [ ] cuffed trousers
- [ ] work boots
- [ ] rope belt
- [ ] wrist wraps/gloves
- [ ] rope/tool accessory

### Shipwright

Use the dockworker/craft modular family with a stronger repair identity:

- [ ] work top / utility jacket
- [ ] durable trousers
- [ ] tool belt/harness
- [ ] gloves or wraps
- [ ] boat-repair tool accessory
- [ ] trade/shipwright identifier

### Harbor merchant/fisher
- [ ] one merchant or fisher stack sufficient for route population

### Harbor guard
- [ ] guard jacket/haori
- [ ] reinforced trousers
- [ ] guard footwear
- [ ] sash/belt
- [ ] Imperial identification
- [ ] weapon/scabbard if role requires it

## P1-CHAR-03 — Market set

- [ ] general merchant
- [ ] food vendor
- [ ] courier
- [ ] street youth / shopper civilian
- [ ] civic guard variant

## P1-CHAR-04 — Residential set

- [ ] civilian adult
- [ ] elder
- [ ] household worker
- [ ] teen/youth

## P1-CHAR-05 — Academy set

### Student
- [ ] Academy inner top
- [ ] Academy outer layer
- [ ] training trousers
- [ ] martial footwear
- [ ] Academy sash
- [ ] Academy insignia

### Senior student
- [ ] distinct trim/sash
- [ ] rank indicator
- [ ] stronger outerwear variation

### Instructor
- [ ] senior martial outerwear
- [ ] instructor sash
- [ ] combat trousers
- [ ] Academy authority marker

### Sensei
- [ ] distinct senior silhouette
- [ ] premium restrained garment treatment
- [ ] strong sash/belt design
- [ ] role-specific accessory
- [ ] high readability at gameplay scale

### Groundskeeper / attendant
- [ ] workwear
- [ ] Academy identification
- [ ] maintenance accessory

---

# 6. Character Variation Rules for v0

The v0 route must feel populated without requiring dozens of unique sprite sheets.

Use controlled modular variation:

- body/skin variants within the approved palette;
- priority Afro-descended hairstyle set;
- top/outerwear/pants/footwear recombination only where role identity remains believable;
- district-specific sash, badge, pouch, tool, or trade accessory;
- restrained palette variations rather than arbitrary recolors;
- faction/role markings on garments where appropriate;
- no mannequin/base-body NPCs in presentation views;
- no entire NPC population created by palette-swapping one silhouette.

Minimum visible population target for the complete route should be enough to make the city feel inhabited while maintaining frame-rate and readability. Reuse is acceptable only when spacing, role, silhouette, and clothing variation prevent obvious duplication.

---

# 7. P2 — Gameplay-Facing Art Integration

P2 does not require every gameplay system to be final. It requires the art to be tested against the systems that will visibly affect it.

## Traversal

- [ ] eight-direction movement uses correct facing sprites
- [ ] walk animation does not drift from pivot
- [ ] player passes correctly in front of / behind architecture
- [ ] bridge, doorway, stair, alley, quay, and veranda collision feel credible
- [ ] foreground props fade/cut away only when authored
- [ ] no grid-shaped visibility behavior

## Paper doll / equipment

- [ ] clothing layers remain aligned through all directions
- [ ] weapon/equipment routing stays on the correct anatomical side
- [ ] inventory changes can visibly alter equipped layers where supported
- [ ] no coarse whole-body overlay hides anatomy incorrectly

## Dialogue / interaction

- [ ] interactable NPC readability
- [ ] shopkeeper interaction
- [ ] shipwright interaction shell
- [ ] Academy/Sensei interaction
- [ ] doors / entrances / notice boards visibly read as interactable without generic glowing UI clutter

## Live combat presentation

The early build is an action RPG. Combat testing must occur in real-time movement.

- [ ] ready state transitions from exploration correctly
- [ ] attack/action silhouettes remain readable against city backgrounds
- [ ] collision and movement space around tutorial combat area is adequate
- [ ] combat telegraphs do not expose the hidden movement grid
- [ ] foreground occlusion does not hide important combat information
- [ ] starting weapon, unarmed state, and/or trap equipment render consistently with the paper-doll rules

## Day / night readiness

The first art pass does not require every atmospheric variation to be final, but all early-route materials must survive both lighting conditions.

- [ ] daytime readability
- [ ] evening/night readability
- [ ] warm sodium/analog light treatment only where appropriate
- [ ] weak cathode-green accents remain restrained
- [ ] dry/matte surface treatment; no generic wet-reflective cyberpunk look
- [ ] characters remain readable in local pools of light

---

# 8. Scene Assembly Order

Build the runtime in this order so every step produces a useful integrated test rather than isolated asset accumulation.

## Slice 0 — Foundation courtyard test

Purpose: prove character/world homogeneity before district production.

- P0 shared stone
- timber/plaster wall
- threshold
- post/beam
- drainage
- one foreground occluder
- dressed benchmark player

**Gate:** no automatic failures; critical style/environment/character/projection minimums pass before expanding.

## Slice 1 — Harbor arrival

- full Harbor P1-A minimum composition
- player + 3 harbor NPCs
- shipwright shell
- route exit toward city

**Gate:** Harbor composition can be traversed and scored in the actual runtime.

## Slice 2 — Market connection

- connect Harbor to Market with no scene-style discontinuity
- add shop interaction
- add 5-NPC market population
- verify player readability under awnings/signage

## Slice 3 — Canal / residential transition

- add canal crossing and narrow housing corridor
- test foreground/vertical occlusion
- add civilian population

## Slice 4 — Academy exterior

- establish gate, training grounds, students, and branding
- verify route arrival reads clearly

## Slice 5 — Academy interior / tutorial

- implement room cutaway
- add Sensei and issue/trap area
- connect tutorial interactions

## Slice 6 — Full early-player route review

Walk the entire route without editor intervention:

1. Harbor arrival
2. Shipwright encounter/readability
3. Market/shop interaction
4. Canal/residential transition
5. Academy approach
6. Academy interior
7. Sensei tutorial
8. inventory/trap issue verification
9. live combat/tutorial state

Then perform the integrated rubric review.

---

# 9. Review Gates

## Source gate

Before runtime derivation:

- [ ] reference approved
- [ ] source master approved
- [ ] modular assembly approved
- [ ] isolation / anchor QA passes

## Runtime candidate gate

- [ ] correct target dimensions
- [ ] manual target-pixel cleanup completed
- [ ] hard alpha where required
- [ ] no unintended neighboring pixels
- [ ] correct pivot / anchor
- [ ] correct layer assignment
- [ ] correct collision / occlusion metadata

## Integrated gate

- [ ] asset works in Phaser, not only in isolation
- [ ] character/world quality matches
- [ ] no visible hidden-grid rhythm
- [ ] projection and depth read correctly
- [ ] district identity is clear
- [ ] player/NPC silhouette remains readable
- [ ] no automatic failure
- [ ] critical categories meet minimums

## Completion gate

- **37–41:** internal test candidate only; checklist remains open
- **42–45:** production approved; relevant checklist items may be struck
- **46–50:** lock quality; use as reference quality for subsequent districts

---

# 10. Asset Production Queue

This is the default next-work order unless a newly discovered runtime blocker forces a dependency change.

### Queue A — Shared foundation

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
15. roof/eave/cutaway starter set
16. door/window/shutter starter set
17. sign/lantern/noren starter set
18. shared prop minimum set

### Queue B — Player benchmark

19. male base-underlayer turnaround
20. female base-underlayer turnaround
21. short Afro turnaround
22. dressed player benchmark turnaround
23. modular player-layer isolation
24. source QA
25. runtime 48×64 cleanup
26. idle animation
27. walk animation
28. ready animation
29. Phaser paper-doll integration

### Queue C — Harbor

30. quay/dock/water edge
31. warehouse/shipwright frontage
32. crane/hoist/cargo set
33. boat silhouettes
34. harbor NPC clothing set
35. Harbor integrated test

### Queue D — Market

36. storefront family
37. signage family
38. 3-stall family
39. merchandise set
40. market NPC clothing set
41. shop interaction art support
42. Market integrated test

### Queue E — Residential/canal

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
61. verify day/night material readability
62. verify live-combat readability
63. full-route rubric review
64. repair failures
65. re-score until 42+
66. strike only verified checklist items

---

# 11. Scope Guardrails

Do not allow the following work to derail this milestone before the harbor-to-Academy route is coherent:

- full Imperial Palace production;
- full industrial corridor production;
- every shrine package;
- every shop profession;
- every boat class;
- every Imperial City NPC profession;
- remote crab-island/cave environment production;
- complete wildlands/bandit-zone production;
- final late-game ability VFX;
- art for systems not visible in the early-player route.

Those remain valid game requirements. They are deferred only so the first city experience can become genuinely testable sooner.

---

# 12. Immediate Next Deliverable

The next visual milestone is **Slice 0 — Foundation Courtyard Test**:

- shared Imperial stone surface;
- timber/plaster architectural wall;
- aged stone foundation;
- timber post + horizontal beam;
- street/building threshold;
- drainage element;
- one sign/lantern/noren dressing element;
- one foreground occluder;
- fully dressed benchmark player character.

This is intentionally small. It must prove that the environment reaches the character standard, the character holds up at gameplay scale, the hidden grid stays invisible, and the locked projection/occlusion rules work before the project multiplies the asset count.

After Slice 0 passes its critical gates, production proceeds directly into **Imperial Harbor Arrival**.