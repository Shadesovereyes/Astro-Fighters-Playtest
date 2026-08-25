# Astro Fighters — LOCKED MASTER ART DIRECTION PROMPT

**Status:** LOCKED  
**Purpose:** Top-level production prompt for all Astro Fighters character, environment, prop, district, VFX, and integrated gameplay-art development.

---

## Master Directive

Create **production-quality pixel-art assets for Astro Fighters**. The final art must match the detail density, silhouette quality, material rendering, and authored pixel craftsmanship of the approved Astro Fighters character reference sheets.

**The world art and the character art must feel like they belong to the exact same game, produced by the same studio, using the same pixel vocabulary and quality standard.**

The quality of the world must rise to the character standard. The character standard must never be lowered to make environment mismatch less obvious.

---

# 1. Core Style Requirements

All production art must follow these rules:

- 90s-anime-inspired pixel art
- hand-authored, high-detail pixel clusters
- strong silhouette readability at gameplay scale
- Edo-period Japanese daily-life foundation
- hip-hop / streetwear / martial-fantasy character identity
- warm, lived-in, analog material language
- Japandi-industrial visual restraint
- ancient-industrial / monumental infrastructure integrated into the city
- purposeful material-specific shading
- controlled detail density that remains readable at gameplay scale
- environment and characters rendered with equivalent craftsmanship

Do **not** use:

- sterile sci-fi chrome
- clean holographic cyberpunk language
- flat vector-looking rectangles
- placeholder geometry
- generic RPG Maker visual language
- clean minimalist tilemap styling
- low-detail world assets paired with premium characters
- smooth painted backgrounds pretending to be gameplay scenery
- baked full-screen world images in place of layered runtime assets
- obvious tile repetition that reveals the gameplay grid
- generic fantasy architecture lacking Astro Fighters identity

---

# 2. World Setting Requirements

The primary setting is **Imperial City**, a dense martial metropolis containing multiple distinct but visually unified districts.

The city should support:

- Imperial Harbor / Docks
- Civic Market / Shops
- Artisan / Workshop Ward
- Astro Fighter Academy exterior
- Astro Fighter Academy interiors
- Residential / canal neighborhoods
- Shrines / spiritual pockets
- Civic / administrative ward
- Imperial Palace exterior precinct
- Imperial Palace interiors
- Industrial / infrastructure corridors
- Fringe / outer ward
- Bridges / canal network
- Major district gates and transition spaces

Every district must feel like part of the same Imperial City while possessing its own material, architectural, occupational, and social identity.

---

# 3. Gameplay Structure Requirements

Astro Fighters uses:

- a **hidden 32×32 square gameplay grid**
- **8-direction movement**
- directional states: N, NE, E, SE, S, SW, W, NW
- smooth player-facing movement
- no visible permanent grid

The grid is structural, not graphical.

The environment must visually read as continuous natural space. The player should not be able to infer cell boundaries from:

- pavement seams
- floor-board repetition
- stone patterns
- wall segmentation
- prop spacing
- ground decals
- obvious 32-pixel rhythms
- checkerboarding

Temporary combat telegraphs or targeting overlays may expose spatial logic only when mechanically necessary. The ordinary world must not look like a board game.

---

# 4. Environment Construction Requirements

The playable world must be assembled from **modular layered runtime assets**, not a single flattened scene.

At minimum, maps must support independent layers or object groups for:

1. ground / street / floor surfaces
2. decals and surface wear
3. low props
4. architecture base volumes
5. architecture dressing
6. interactive objects
7. characters / NPCs / mobile objects
8. tall props / occluders
9. foreground elements
10. local shadows
11. restrained atmosphere / FX
12. optional distant decorative vista that never substitutes for playable geometry

The player and NPCs must be able to move:

- behind appropriate objects
- in front of appropriate objects
- through authored interior cutaways
- under roofs that can be removed by architectural region
- behind organic occluders that can fade when necessary

Do not reveal interiors by individual grid cell.

---

# 5. Character Requirements

Characters shown in presentation-quality gameplay previews must be **finished clothed fighters or civilians**, never naked or base-body mannequins.

A complete playable fighter presentation must include, where appropriate:

- body / skin
- hairstyle
- eyes
- inner top
- outerwear
- pants
- footwear
- belt / sash
- weapon
- scabbard
- accessory / charm / tag
- contact shadow

Clothing and equipment must be authored at the same quality level as the approved character reference sheets.

Do not use:

- crude recolor-only clothing
- pasted rectangular garments
- generic fantasy tunics
- incomplete paper-doll stacks
- placeholder outfits in production previews

---

# 6. Character Direction Requirements

Every visible character module must be authored for all eight directions:

- N
- NE
- E
- SE
- S
- SW
- W
- NW

Direction must affect the whole silhouette, including:

- head
- neck
- shoulders
- torso
- hips
- arms
- hands
- legs
- feet
- inner top
- outerwear
- pants
- footwear
- hair back/front/side volume
- sash / belt
- scabbard
- weapon
- charm / tag / accessory
- direction-sensitive shadow
- any directional clothing overlap

A front-facing body with only facial pixels shifted is invalid.

Direction-sensitive draw-order overrides must be supported where equipment crosses the body.

---

# 7. Character Production Workflow

Required workflow:

1. Author an approved master silhouette/proportion system at **480×640 source resolution**.
2. Author eight distinct directional master poses at 480×640.
3. Validate anatomy, foot placement, equipment placement, and occlusion.
4. Derive animation frames from the directional masters.
5. Author all clothing/equipment layers against shared anchors.
6. Derive **48×64 runtime frames** by nearest-neighbor reduction only after source art passes review.

Required animation counts per direction:

- Idle: 4
- Walk: 6
- Ready: 2

Forbidden workflow:

- drawing at 48×64
- enlarging that frame
- calling the enlargement “source art”
- reducing it again

Source art must contain materially more authored information than runtime art.

---

# 7A. Reference-First Asset Development & Autonomous Package Workflow

All Astro Fighters art development must follow a **reference-first, modular-derivation, Phaser-integration** pipeline.

This rule applies to:

- characters
- clothing and equipment
- environment materials
- architecture
- props
- district dressing
- occluders
- VFX
- integrated gameplay-art scenes

## Required Production Sequence

For each new development package:

1. **Select the next dependency package from the active checklists.**
   - Advance world and character needs in parallel where practical.
   - Group related dependencies into a coherent package rather than waiting for one checklist item at a time.
   - Prefer shared/global dependencies before unnecessary district-specific duplication.

2. **Create production-quality pixel-art reference targets first.**
   - Reference targets may include:
     - character master poses
     - clothing/equipment design targets
     - environment benchmark slices
     - architecture/facade studies
     - material studies
     - prop-family studies
     - district-identity compositions
   - These references must already meet the locked Astro Fighters quality direction before they are used as the basis for runtime production.
   - A weak reference image must be refined at the source stage; do not reduce low-quality source art and attempt to repair it only at runtime scale.

3. **Use the approved reference target as the quality anchor.**
   - It establishes:
     - silhouette quality
     - authored pixel-cluster language
     - material rendering
     - palette behavior
     - district identity
     - clothing/equipment language
     - character/world style homogeneity
   - Compare new reference work directly against the approved Astro Fighters character sheets, Imperial City reference, Master Palette, and this master direction.

4. **Derive modular runtime assets from the approved reference target.**
   - Do not treat a single attractive reference composition as the finished playable asset.
   - Break the approved visual target into gameplay-appropriate modular pieces such as:
     - ground/surface variants
     - decals
     - walls/foundations
     - roofs/eaves
     - doors/windows/shutters
     - gates/bridges/railings
     - signs/lanterns/pipes/hardware
     - props and clutter
     - foreground/occluder layers
     - character body layers
     - clothing/equipment/accessory layers
     - animation sheets
     - VFX layers
   - Where a runtime asset is directly reduced from higher-resolution source pixel art, use nearest-neighbor reduction and preserve authored cluster relationships.
   - Runtime assets must remain modular, layerable, direction-aware, and compatible with the hidden-grid gameplay structure.

5. **Integrate the derived assets into the actual Phaser runtime.**
   - Production gameplay-art integration must occur in the established **Phaser-based Astro Fighters runtime**.
   - A separate custom Canvas renderer, mock renderer, baked background, or isolated technical demo may be used only as a temporary diagnostic tool and may **not** substitute for Phaser integration or gameplay-art acceptance.
   - Validate movement, collision, depth sorting, occlusion, cutaways, LOS behavior, interaction readability, and eight-direction character routing in Phaser.

6. **Review the integrated Phaser result with the mandatory rubric.**
   - Benchmark/reference approval does not complete a checklist item.
   - Isolated PNG approval does not complete a checklist item.
   - A checklist item is complete only when the relevant asset is demonstrated in representative integrated gameplay and passes the required review gate.
   - If the result fails an automatic condition, misses a critical minimum, or remains below the required completion threshold, continue development automatically.

## Benchmark Image Rule

The required workflow is:

> **high-quality pixel-art reference target → approved visual benchmark → modular asset derivation → Phaser integration → integrated rubric review**

The forbidden shortcut is:

> **pretty image → shrink/crop it → call it finished game art**

Reference images are **design and quality authorities**. Runtime assets are purpose-built derivatives that must preserve the reference's craftsmanship while satisfying gameplay, layering, collision, direction, and occlusion requirements.

## Autonomous Package Rule

Unless the user explicitly pauses or redirects development, the production agent should continue through the active art checklists **autonomously by dependency package**.

During an active development run:

- do not wait for the user to request each checklist item individually
- do not interrupt for routine asset selection, naming, sequencing, or refinement decisions already governed by this prompt
- select the next logical package
- build/refine its reference target
- derive its modular assets
- integrate them into Phaser
- review them
- continue automatically when the gate is not met
- update the development handoff/status as packages advance

Pause for user approval only when a **major art-direction decision** is genuinely unresolved by:

- this locked master prompt
- approved reference images
- the Master Palette
- the world/character checklists
- the art review rubric
- existing approved production assets

Examples of major approval points include a new visual language, a major silhouette-family change, a new district identity that conflicts with established references, or a proposed change to a locked rule.

Routine failures are **not** approval points. They trigger more development.

---

# 8. Character Clothing Direction

Clothing must express Astro Fighters' **Edo + martial + hip-hop / streetwear** design language.

Appropriate clothing families include:

## Inner Tops
- wrapped martial top
- sleeveless fighter wrap
- cropped fitted underlayer
- hooded underlayer
- banded chest-wrap top

## Outerwear
- patterned haori
- short utility jacket
- split-tail street haori
- sleeveless battle coat
- scarf-collar fighter jacket

## Pants
- loose fighter trousers
- cuffed worker pants
- hakama-influenced combat pants
- wrapped shin trousers
- reinforced street-martial slacks

## Footwear
- wrapped boots
- tabi-boot hybrid
- sandal-boot hybrid
- sneaker-hybrid martial shoe

## Belts / Waist
- rope sash
- cloth obi
- charm cord belt
- pouch belt
- bead-tie sash

## Accessories
- charm tag
- wrist wraps
- neck cord
- bead ties
- shoulder cloth ties
- talisman strips
- pouch
- scabbard cord details

## Hair Priorities
- short afro
- high puff
- freeform locs
- twists / braids
- puff undercut

These are real authored layers, not cosmetic afterthoughts.

---

# 9. World Material Language

Environment materials must be visually distinguishable without labels.

Primary material families include:

- pristine timber
- weathered timber
- plaster
- stone
- roof tile
- paper
- rope
- cloth
- brass
- clean iron / metal
- rusted metal
- patina
- soot
- water
- damp masonry
- moss
- foliage

Different materials must not appear as the same flat shape with different colors.

Material identity should be communicated through:

- pixel clustering
- edge treatment
- highlight behavior
- shadow behavior
- wear patterns
- texture frequency
- material-specific color ramps

---

# 10. Imperial City Environment Identity

Imperial City must communicate:

- Edo daily life at human scale
- martial culture
- dense lived-in urban activity
- analog industrial infrastructure
- ancient monumental civic construction
- canals and water infrastructure
- workshops and handcraft
- civic hierarchy
- spiritual spaces
- market commerce
- residential life
- formal Imperial precincts
- rougher outer/fringe zones

Appropriate recurring materials and visual motifs include:

- warm wood
- aged plaster
- stone
- roof tile
- rope
- cloth
- paper lanterns
- brass
- iron
- rust
- patina
- soot
- steam
- water
- Imperial vermilion accents
- restrained cathode glow

The city must not look like a generic Japanese fantasy village.

---

# 11. World Asset Categories

Environment production should be built from modular asset families including:

## Ground
- stone streets
- damp stone
- dirt
- timber walkways
- dock planks
- training-yard earth
- palace paving
- interior timber
- tatami
- industrial walkways

## Decals
- cracks
- stains
- puddles
- drainage
- soot
- moss
- algae
- paper
- leaves
- cloth scraps
- wheel/cart wear

## Architecture
- timber frames
- plaster walls
- stone foundations
- paper-panel walls
- doors
- shutters
- windows
- roof tiles
- eaves
- balconies
- verandas
- railings
- retaining walls
- stairs
- gates
- bridges

## Architectural Dressing
- signs
- banners
- lanterns
- pipes
- vents
- chimneys
- cables
- rope lines
- brackets
- gauges
- cathode devices
- wall notices
- charm strips

## Props
- crates
- barrels
- baskets
- sacks
- jars
- rope
- buckets
- stools
- benches
- tables
- carts
- tools
- fabric bundles
- firewood
- storage
- workshop clutter

## Tall Occluders
- roofs
- large trees
- gantries
- elevated rail elements
- awnings
- towers
- arches
- large machinery

## Atmosphere
- steam
- smoke
- incense
- dust
- rain
- water ripple
- lantern flicker
- cloth movement
- leaf movement
- cathode flicker

---

# 12. Architectural Projection Rules

Use the locked **flat-faced 3/4 cabinet projection**.

Architecture should communicate depth through:

- overlap
- vertical placement
- top/front face separation
- shadows
- Y-sorting
- scale consistency
- material contrast
- occlusion

Do not rely on photographic perspective or dramatic vanishing-point convergence.

Major architecture should be allowed to dwarf 48×64 fighters.

Do not artificially shorten structures merely to preserve visibility.

Use authored cutaways, roof removal, layering, and occlusion logic instead.

---

# 13. Occlusion Rules

Environment art must support three practical height classes.

## Low
Examples:
- crates
- benches
- curbs
- small machinery

Behavior:
- may cover feet or lower legs
- remains visible
- does not auto-fade

## Mid
Examples:
- counters
- fences
- workbenches
- machinery

Behavior:
- may cover a meaningful portion of the fighter
- normally remains visible
- should not permanently obscure the fighter's head/silhouette

## Tall
Examples:
- buildings
- roofs
- trees
- towers
- gantries
- elevated infrastructure

Behavior:
- must support dynamic occlusion
- architecture uses cutaways / roof removal
- organic/decorative elements may fade where necessary
- solid LOS-blocking structures must never reveal enemies the player cannot legitimately see

Never fade the player as the primary solution.

---

# 14. Interior Cutaway Rules

When the player enters an interior:

- roof disappears by architectural region
- back / north wall can retain full height
- side walls may taper toward the foreground
- front / south wall becomes a low cutaway
- interior visibility must be room-based or region-based
- never reveal square cells one at a time

The player should perceive:

> “The room became visible.”

Not:

> “The game uncovered tiles.”

---

# 15. Lighting Rules

Default exterior lighting direction:

**upper-left / northwest**

General material behavior:

- upper-left highlight
- local-color midtone
- lower-right shadow
- darkest value in cavities/contact edges

Local sources may override nearby lighting:

- lanterns
- furnaces
- fires
- cathode devices
- spiritual effects

Avoid heavy full-screen color grading that destroys palette relationships.

---

# 16. Palette Requirements

The **Astro Fighters Master Palette** is the canonical color authority.

Do not invent arbitrary cosmetic colors unless the palette is formally revised.

Use material-specific ramps for:

- skin
- timber
- stone
- clean metal
- rusted metal
- cloth
- biome/foliage
- Imperial vermilion
- trim/accent
- elemental VFX
- Yin
- Yang
- Spirit
- cathode glow
- patina
- UI

Individual runtime assets should use restrained portions of a ramp rather than every available shade.

---

# 17. District-Specific Development Requirement

Each Imperial City district must receive its own authored asset family and may not simply reuse the same generic buildings with superficial prop swaps.

Districts must be visually differentiated through:

- architecture
- materials
- signage
- clutter
- occupations
- NPC clothing
- infrastructure
- spatial organization
- social function

while remaining part of the same city-wide art language.

---

# 18. Required District Families

## Imperial Harbor / Docks
Include:
- quay
- piers
- warehouses
- cranes
- hoists
- rope systems
- boats
- cargo
- nets
- merchant infrastructure
- wet surfaces
- water interaction

## Civic Market / Shops
Include:
- storefronts
- signs
- awnings
- stalls
- merchandise
- carts
- narrow streets
- commercial clutter
- merchant/civilian population

## Artisan / Workshops
Include:
- workbenches
- tools
- furnaces
- racks
- machinery
- pipes
- materials
- active labor clutter
- cutaway interiors

## Academy
Include:
- ceremonial gates
- dojos
- training courtyards
- practice equipment
- weapon racks
- banners
- student/instructor clothing
- furnished interiors

## Residential
Include:
- dense housing
- canal homes
- alleys
- laundry
- household clutter
- civilian life
- small bridges
- neighborhood shrines

## Shrines
Include:
- shrine gates
- offerings
- incense
- paper charms
- stone lanterns
- sacred trees
- restrained spiritual atmosphere

## Civic / Administrative
Include:
- formal offices
- official signage
- records
- guards
- controlled plazas
- administrative props

## Palace
Include:
- monumental gates
- refined stone
- formal courtyards
- Imperial ornament
- guard infrastructure
- premium materials
- court interiors

## Industrial Infrastructure
Include:
- elevated rail
- gantries
- pipes
- pumps
- utility towers
- lifts
- gauges
- cathode devices
- maintenance spaces

## Fringe Ward
Include:
- broken paving
- patched construction
- improvised shops
- salvaged materials
- damaged infrastructure
- combat spaces
- worn but still high-quality art

---

# 19. Presentation Preview Rules

Every preview presented for review must show an **integrated gameplay view**, not isolated asset sheets unless specifically requested.

Reference sheets, benchmark compositions, material studies, and source-scale asset studies are expected development artifacts under Section 7A, but they are **reference-stage reviews**, not evidence that a gameplay checklist item is complete. Production acceptance still requires the derived modular assets to be integrated into the Phaser runtime.

A presentation-quality preview must contain:

- fully clothed player character
- appropriately dressed NPCs
- final-quality or near-final-quality world assets
- layered architecture
- district-specific clutter
- props
- occlusion
- material variety
- contact/cast shadows
- hidden-grid-friendly surfaces
- coherent lighting
- equivalent character/world pixel-art quality

Do not present:

- mannequin characters
- blockout architecture
- generic rectangles
- low-detail placeholder trees
- temporary environment composites
- asset tests pretending to be finished scenes

---

# 20. Mandatory Art Review Gate

All assets and integrated scenes must be reviewed against the **Astro Fighters Art Preview Review Rubric** before they are placed in the game or presented as testable.

Reference targets should be reviewed at source/benchmark stage before modular derivation, but **checklist completion is determined only by representative integrated Phaser gameplay**.

Development behavior:

- **Below 36:** continue development automatically.
- **Automatic failure:** continue development automatically.
- **Critical category below its minimum:** continue development automatically.
- **36–41:** internal test candidate only, provided all critical requirements pass.
- **42–45:** production approved.
- **46–50:** lock-quality visual target.

A high aggregate score may not override a critical-category failure.

In particular, these categories must meet their rubric minimums:

- Character / World Style Homogeneity
- Character Completion & Clothing
- Environment Pixel-Art Quality
- Astro Fighters World Identity
- Architectural Detail & Silhouette
- Projection, Depth & Occlusion

---

# 21. Automatic Failure Conditions

A preview or asset pass fails immediately if:

- world art is visibly lower quality than the character art
- environment primarily consists of primitive geometry
- characters are naked/mannequin-like
- clothing is incomplete or placeholder quality
- characters look pasted onto the environment
- buildings are generic boxes
- a baked image substitutes for layered playable world construction
- the hidden grid is visible
- pixel density/styles visibly clash
- environment resembles generic RPG Maker/vector/cyberpunk art
- directional bodies are obviously incorrect
- occlusion permanently hides the controlled fighter without an authored solution
- known placeholder assets are presented as production-quality art

---

# 22. Final Acceptance Standard

Before approving any asset or scene, ask:

> **Does this look like premium Astro Fighters character art inhabiting a premium Astro Fighters world — or does it look like premium character art placed inside a cheaper environment?**

If the second interpretation is reasonably possible, the asset or scene is **not approved** and development continues.

The finished result must look like **one coherent game**.

---

# 23. Compact Reusable Production Prompt

> Create production-quality pixel-art assets for Astro Fighters that match the approved character reference sheets in style, detail density, silhouette quality, material rendering, and craftsmanship. Follow the locked reference-first workflow: create and approve high-quality source/benchmark pixel-art references first, derive modular gameplay assets from those benchmarks, integrate the derived assets into the established Phaser runtime, then evaluate the representative integrated gameplay result with the mandatory rubric. Do not treat a pretty reference image as a finished gameplay asset, and do not substitute a custom Canvas renderer, baked scene, or isolated technical demo for Phaser integration. Proceed autonomously through the active world and character checklists by dependency package unless a major art-direction decision genuinely requires user approval. Do not create placeholder blockout art, flat rectangle-based scenery, naked mannequin characters, generic RPG tiles, or baked gameplay backgrounds. Build Imperial City as a modular layered world for a hidden 32×32 square grid with smooth 8-direction movement. Characters must be fully clothed and accessorized in an Edo + hip-hop martial style, with complete direction-aware paper-doll layers. Environment districts must include the Imperial Harbor, Civic Market, Workshops, Academy, Residential canals, Shrines, Civic Ward, Palace, Industrial infrastructure, Fringe Ward, bridges, and gates. Use dense lived-in detail, handcrafted pixel clusters, warm analog materials, signage, clutter, shadow, depth, occlusion, monumental architecture, and restrained cathode/spiritual effects. The world must equal the character models in pixel-art quality. If a benchmark, runtime asset, or integrated scene misses the locked standard, continue refining automatically rather than lowering the target. If the integrated rubric score is below 36, an automatic failure is present, or a critical-category minimum is missed, continue development automatically rather than presenting the scene as testable.
