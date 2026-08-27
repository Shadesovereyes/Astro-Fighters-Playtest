# Astro Fighters — LOCKED MASTER ART DIRECTION PROMPT

**Status:** LOCKED  
**Purpose:** Top-level production prompt for all Astro Fighters character, environment, prop, district, VFX, and integrated gameplay-art development.

---

## Master Directive

Create **production-quality pixel-art assets for Astro Fighters**. Final art must match the detail density, silhouette quality, material rendering, and authored pixel craftsmanship of the approved Astro Fighters character reference sheets.

**The world art and character art must feel like they belong to the exact same game, produced by the same studio, using the same pixel vocabulary and quality standard.**

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

The city must support:

- Imperial Harbor / Docks
- Civic Market / Shops
- Artisan / Workshop Ward
- Astro Fighter Academy exterior and interiors
- Residential / canal neighborhoods
- Shrines / spiritual pockets
- Civic / administrative ward
- Imperial Palace exterior precinct and interiors
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
- **canonical facing convention: S = front / toward camera; N = back / away from camera**
- smooth player-facing movement
- no visible permanent grid

The grid is structural, not graphical. The ordinary world must read as continuous natural space. Players must not be able to infer cell boundaries from pavement seams, floor boards, stones, wall segmentation, prop spacing, decals, checkerboarding, or repeated 32-pixel rhythms.

Temporary combat telegraphs or targeting overlays may expose spatial logic only when mechanically necessary.

---

# 4. Environment Construction Requirements

The playable world must be assembled from **modular layered runtime assets**, not a single flattened scene.

Maps must support independent layers or object groups for:

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

The player and NPCs must be able to move behind and in front of appropriate objects, through authored interior cutaways, under roofs removed by architectural region, and behind organic occluders that can fade when necessary.

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

## Base Underlayer Standard

The interchangeable paper-doll base is **never nude**.

- **Male base:** body / skin + hair / face + **base shorts**.
- **Female base:** body / skin + hair / face + **base shorts + sports bra**.
- Chest wraps, wrist wraps, leg wraps, footwear, clothing, weapons, scabbards, charms, pouches, and other equipment are separate removable layers unless a specific locked design says otherwise.

Do not use crude recolor-only clothing, pasted rectangular garments, generic fantasy tunics, incomplete paper-doll stacks, or placeholder outfits in production previews.

---

# 6. Character Direction Requirements

Every visible character module must be authored for all eight directions:

- `N` = back / away from camera
- `NE` = back-right 3/4
- `E` = right profile
- `SE` = front-right 3/4
- `S` = front / toward camera
- `SW` = front-left 3/4
- `W` = left profile
- `NW` = back-left 3/4

Reference sheets or legacy source files that use a different direction-label convention must be remapped in metadata. Correct artwork must not be rotated, mirrored, or repainted merely to change a source-slot name. Runtime / Phaser facing state and final asset names always use the canonical convention above.

Direction must affect the whole silhouette, including head, neck, shoulders, torso, hips, arms, hands, legs, feet, clothing, hair volume, sash, scabbard, weapon, accessories, shadow, and overlap order. A front-facing body with only facial pixels shifted is invalid.

## Anatomical-Side Rule

Equipment placement is defined relative to the **character's anatomy**, not screen-left / screen-right.

Example: when a sword is mounted on the character's **left hip**, that left-hip mount must remain anatomically correct in all eight facings. In `S` / front, the mount root and hilt must read in the correct left-arm / torso relationship rather than being placed outside the wrong arm merely because that is convenient in screen coordinates.

Direction-sensitive draw-order overrides must be supported wherever clothing or equipment crosses the body.

---

# 7. Character Production Workflow

Character production uses a **contract-first, shared-lattice, source-approval, target-pixel-cleanup** workflow.

## 7.1 Lock the Character Asset Contract Before Generation

Before generating or drawing a character package, record:

- canonical direction convention
- source canvas size
- shared body center
- shared foot-contact line
- base-underlayer contents
- hairstyle / head authority
- anatomical equipment mount side
- layer family names
- front / back / near / far routing rules
- draw-order overrides per facing where needed
- source palette authority
- runtime frame size
- required animation states

Do not ask the image generator to rediscover these relationships independently for every garment or accessory.

## 7.2 Shared Source Lattice

1. Author an approved master silhouette / proportion system at **480×640 source resolution**.
2. Author eight distinct directional body masters on that exact shared canvas.
3. All body, hair, clothing, weapon, equipment, and accessory modules must use the same source lattice and anchors.
4. A layer must not be independently centered or bottom-justified if doing so changes its anatomical relationship to the body.
5. Source art must contain materially more authored information than runtime art.

## 7.3 Source Authorities Must Be Created as a Set

For a playable fighter, create and approve:

1. **base-underlayer turnaround** — eight directions on the shared lattice
2. **fully dressed benchmark turnaround** — the visual / silhouette authority
3. **modular source component set** — garments, weapons, charms, and equipment authored for the same poses and anchors

The fully dressed benchmark is a quality authority; it is **not** a substitute for properly authored modular layers.

## 7.4 Modular Character Layer Standard

Garments that cross the body may require decomposition into direction-aware pieces such as:

- back mass
- far sleeve
- far/front panel
- near sleeve
- near/front panel
- sash back / front
- weapon behind-body / front-body portions

Whole-garment overlays are invalid when they cover anatomy that should remain visible. Near/far routing is direction-specific and must follow the dressed benchmark.

## 7.5 Source Approval Before Runtime Reduction

Do not derive 48×64 runtime art until all eight source directions pass:

- anatomy
- direction labeling
- foot placement
- garment registration
- weapon / equipment mount placement
- near / far occlusion
- source isolation cleanliness
- palette / hard-alpha requirements
- complete dressed-composite comparison against the approved benchmark

Fix source problems at source scale. Do not multiply errors by reducing unstable source art.

## 7.6 Runtime Derivation and Final Pixel Accuracy

After the source masters pass:

1. derive **48×64 runtime frames**
2. use nearest-neighbor reduction where the source is authored as integer-scalable pixel art
3. treat the reduction as a starting candidate, not automatic final art
4. manually correct target-resolution pixels for silhouette, clusters, hands, hair, hems, footwear, weapon contours, and material boundaries
5. validate exact palette, hard alpha, anchor, direction, and draw-order data
6. only then mark the runtime sprite as pixel-final

A mechanically reduced image is **not** final production art merely because it loads in Phaser.

Required animation counts per direction:

- Idle: 4
- Walk: 6
- Ready: 2

Forbidden workflow:

- drawing a low-information 48×64 frame, enlarging it, and calling the enlargement source art
- repeatedly reducing unapproved source art while the source design is still changing
- using automatic template matching, broad color segmentation, procedural healing, or similar image-analysis operations as the authority for final production pixels

Automatic image analysis may be used diagnostically to locate alignment or contamination problems; final pixels remain authored and reviewed.

---

# 7A. Reference-First Asset Development & Autonomous Package Workflow

All Astro Fighters art development must follow a **reference-first → modular-source → source-QA → runtime-derivation → Phaser-integration** pipeline.

This applies to characters, clothing / equipment, environment materials, architecture, props, district dressing, occluders, VFX, and integrated gameplay-art scenes.

## Required Production Sequence

For each development package:

1. **Select and contract the package.**
   - Select the next dependency from the active checklists.
   - Group related dependencies into a coherent package.
   - Lock names, dimensions, anchors, layer roles, collision / occlusion role, palette family, and runtime destination before generating assets.

2. **Create a production-quality reference target first.**
   - Examples: character turnaround, clothing / equipment benchmark, environment benchmark slice, facade study, material study, prop family, or district-identity composition.
   - A weak reference is refined at the source stage; never shrink weak art and hope runtime cleanup will create the missing quality.

3. **Create modular source art specifically for extraction and reuse.**
   - Do not rely on cutting every production module out of a single fully composed illustration.
   - Where interchangeability matters, create clean component sources against the same locked lattice / projection / material authority.
   - Reference and modular source art must agree on silhouette, palette behavior, scale, and attachment points.

4. **Perform immediate isolation and anchor QA.**
   Every isolated module must pass before registration or integration:
   - no neighboring-item pixels
   - no clipped pieces from adjacent cells
   - no labels, borders, presentation shadows, or checkerboard / paper background
   - transparent unused pixels
   - hard alpha where required
   - correct source palette
   - correct bounding box and anchor class

   Default world-prop anchor rules:
   - floor-hosted: horizontal center + bottom-pixel justification to the shared ground-contact line
   - hanging: horizontal center + hook / top-mount anchor
   - wall-mounted: attachment-line anchor
   - character paper-doll layers: shared anatomical lattice overrides generic centering / bottom justification

5. **Approve the source composite / source assembly before runtime reduction.**
   - Characters: compare all eight modular composites against the approved dressed turnaround.
   - World: assemble a representative modular source slice to verify material, scale, seams, occlusion, and hidden-grid concealment.
   - Fix bad isolation, scale, direction, attachment, or overlap here—not after multiple downstream conversions.

6. **Derive target-resolution assets once the source is stable.**
   - Preserve authored pixel clusters.
   - Perform manual target-resolution pixel cleanup.
   - Validate palette, alpha, anchors, silhouettes, and modular seams.

7. **Integrate the accepted runtime assets into the actual Phaser runtime.**
   - Production gameplay-art integration must occur in the established **Phaser-based Astro Fighters runtime**.
   - A custom Canvas renderer, mock renderer, baked background, or isolated technical demo may be used only as a temporary diagnostic tool and may **not** substitute for Phaser integration or acceptance.
   - Validate movement, collision, depth sorting, occlusion, cutaways, LOS behavior, interaction readability, hidden-grid concealment, and eight-direction routing.

8. **Review representative integrated Phaser gameplay with the mandatory rubric.**
   - Reference approval does not complete a checklist item.
   - Isolated PNG approval does not complete a checklist item.
   - Source-composite approval does not complete a checklist item.
   - Checklist completion occurs only after representative integrated gameplay passes the required review gate.

## Benchmark Image Rule

Required:

> **high-quality reference target → approved benchmark → purpose-built modular source assets → clean source assembly → target-resolution pixel cleanup → Phaser integration → integrated rubric review**

Forbidden:

> **pretty image → shrink / crop it → call it finished game art**

---

# 7B. Iteration Control, QA Scope & Repository Hygiene

The production process must actively minimize avoidable iterations.

## Narrow QA Scope

Development QA images should be the smallest image that answers the current question.

Prefer:

- one asset
- one asset family
- a compact 8-direction contact sheet
- a compact `source / registered / benchmark` strip
- an actual Phaser screenshot for integration QA

Do **not** create large infographic-style development boards, decorative dashboards, fake status panels, palette presentations, or explanatory text-heavy images unless the user explicitly requests them or the visual comparison genuinely requires them. Status, reasoning, scores, and notes belong in Markdown / JSON, not baked into art.

## One Gate at a Time

Do not proceed downstream while an upstream gate is visibly failing. Typical order:

`CONTRACT → REFERENCE → MODULAR SOURCE → ISOLATION QA → SOURCE REGISTRATION / ASSEMBLY → SOURCE APPROVAL → RUNTIME DERIVATION → TARGET PIXEL CLEANUP → PHASER → RUBRIC`

If isolation is contaminated, fix isolation before registration. If registration is wrong, fix source registration before runtime reduction. If source direction is wrong, do not create animation frames from it.

## Single-Current-State Repository Rule

Git history is the version archive. The active repository must not be filled with sequential package-version files.

- use stable canonical filenames and paths
- replace the current asset / manifest in place when it improves
- do not commit `v12`, `v13`, `v14`, etc. copies merely to preserve history
- keep failed generations, temporary QA boards, extraction experiments, and disposable diagnostics outside the repository
- commit only current source authorities, accepted runtime candidates / finals, required metadata, and concise current status / handoff material
- maintain one current manifest per system where practical instead of multiplying overlapping direction / anchor / layer-order / position manifests
- use Git commits / branches / tags to recover historical iterations
- prefer stable Phaser asset paths so art can improve without runtime code churn

A development package is a workflow unit, not a reason to permanently create another directory tree or status document.

## Machine-Readable Registration Contract

Where modular assets depend on placement, keep concise metadata recording the current authority, such as:

- canonical direction
- source-slot remap if legacy labels differ
- canvas dimensions
- character center and foot contact
- anatomical mount side
- layer / draw order
- anchor pixel or anchor class
- top-left placement / bounding box when required
- missing-source flags
- collision / occlusion role for world modules
- runtime approval state

The manifest stores current production facts; Git stores its history.

---

# 7C. Autonomous Package Rule

Unless the user explicitly pauses or redirects development, continue through the active art checklists **autonomously by dependency package**.

During active development:

- do not wait for the user to request every checklist item individually
- do not interrupt for routine naming, sequencing, extraction, refinement, or integration decisions already governed by this prompt
- select the next logical package
- build / refine its reference target
- derive clean modular source assets
- run immediate QA
- derive target-resolution assets only after source approval
- integrate them into Phaser
- review them
- continue automatically when a gate is not met
- update the concise current handoff / status instead of spawning versioned status files

Pause for user approval only when a **major art-direction decision** is genuinely unresolved by this prompt, approved references, Master Palette, checklists, rubric, or accepted production assets.

Routine failures are **not** approval points. They trigger more development.

---

# 8. Character Clothing Direction

Clothing must express Astro Fighters' **Edo + martial + hip-hop / streetwear** design language.

Appropriate families include:

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

Primary material families include pristine timber, weathered timber, plaster, stone, roof tile, paper, rope, cloth, brass, clean iron / metal, rusted metal, patina, soot, water, damp masonry, moss, and foliage.

Material identity must be communicated through pixel clustering, edge treatment, highlight behavior, shadow behavior, wear patterns, texture frequency, and material-specific color ramps. Different materials must not appear as the same flat shape with different colors.

---

# 10. Imperial City Environment Identity

Imperial City must communicate Edo daily life at human scale, martial culture, dense lived-in activity, analog industrial infrastructure, ancient monumental civic construction, canals, workshops, civic hierarchy, spiritual spaces, market commerce, residential life, formal Imperial precincts, and rougher outer / fringe zones.

Recurring materials and motifs include warm wood, aged plaster, stone, roof tile, rope, cloth, paper lanterns, brass, iron, rust, patina, soot, steam, water, Imperial vermilion accents, and restrained cathode glow.

The city must not look like a generic Japanese fantasy village.

---

# 11. World Asset Categories

Environment production should be built from modular families including:

- **Ground:** stone streets, damp stone, dirt, timber walkways, dock planks, training-yard earth, palace paving, interior timber, tatami, industrial walkways
- **Decals:** cracks, stains, puddles, drainage, soot, moss, algae, paper, leaves, cloth scraps, wheel / cart wear
- **Architecture:** timber frames, plaster walls, stone foundations, paper-panel walls, doors, shutters, windows, roof tiles, eaves, balconies, verandas, railings, retaining walls, stairs, gates, bridges
- **Architectural dressing:** signs, banners, lanterns, pipes, vents, chimneys, cables, rope lines, brackets, gauges, cathode devices, wall notices, charm strips
- **Props:** crates, barrels, baskets, sacks, jars, rope, buckets, stools, benches, tables, carts, tools, fabric bundles, firewood, storage, workshop clutter
- **Tall occluders:** roofs, large trees, gantries, elevated rail elements, awnings, towers, arches, large machinery
- **Atmosphere:** steam, smoke, incense, dust, rain, water ripple, lantern flicker, cloth movement, leaf movement, cathode flicker

---

# 12. Architectural Projection Rules

Use the locked **flat-faced 3/4 cabinet projection**.

Architecture communicates depth through overlap, vertical placement, top/front face separation, shadows, Y-sorting, scale consistency, material contrast, and occlusion. Do not rely on photographic perspective or dramatic vanishing-point convergence.

Major architecture may dwarf 48×64 fighters. Do not artificially shorten structures merely to preserve visibility; use authored cutaways, roof removal, layering, and occlusion logic instead.

---

# 13. Occlusion Rules

Environment art supports three practical height classes:

- **Low:** crates, benches, curbs, small machinery. May cover feet / lower legs; remains visible; does not auto-fade.
- **Mid:** counters, fences, workbenches, machinery. May cover a meaningful portion of the fighter but should not permanently obscure the head / silhouette.
- **Tall:** buildings, roofs, trees, towers, gantries, elevated infrastructure. Must support dynamic occlusion; architecture uses cutaways / roof removal; organic / decorative elements may fade where necessary; solid LOS-blockers never reveal enemies the player cannot legitimately see.

Never fade the player as the primary solution.

---

# 14. Interior Cutaway Rules

When the player enters an interior:

- roof disappears by architectural region
- back / north wall can retain full height
- side walls may taper toward the foreground
- front / south wall becomes a low cutaway
- interior visibility is room-based or region-based
- never reveal square cells one at a time

The player should perceive **“the room became visible,”** not **“the game uncovered tiles.”**

---

# 15. Lighting Rules

Default exterior lighting direction is **upper-left / northwest**.

General material behavior:

- upper-left highlight
- local-color midtone
- lower-right shadow
- darkest value in cavities / contact edges

Local lanterns, furnaces, fires, cathode devices, and spiritual effects may override nearby lighting. Avoid heavy full-screen color grading that destroys palette relationships.

---

# 16. Palette Requirements

The **Astro Fighters Master Palette** is the canonical color authority. Do not invent arbitrary cosmetic colors unless the palette is formally revised.

Use material-specific ramps for skin, timber, stone, clean metal, rusted metal, cloth, biome / foliage, Imperial vermilion, trim / accent, elemental VFX, Yin, Yang, Spirit, cathode glow, patina, and UI.

Individual runtime assets should use restrained portions of a ramp rather than every available shade.

---

# 17. District-Specific Development Requirement

Each Imperial City district must receive its own authored asset family and may not simply reuse generic buildings with superficial prop swaps.

Differentiate districts through architecture, materials, signage, clutter, occupations, NPC clothing, infrastructure, spatial organization, and social function while maintaining one city-wide art language.

---

# 18. Required District Families

## Imperial Harbor / Docks
Quay, piers, warehouses, cranes, hoists, rope systems, boats, cargo, nets, merchant infrastructure, wet surfaces, water interaction.

## Civic Market / Shops
Storefronts, signs, awnings, stalls, merchandise, carts, narrow streets, commercial clutter, merchant / civilian population.

## Artisan / Workshops
Workbenches, tools, furnaces, racks, machinery, pipes, materials, active labor clutter, cutaway interiors.

## Academy
Ceremonial gates, dojos, training courtyards, practice equipment, weapon racks, banners, student / instructor clothing, furnished interiors.

## Residential
Dense housing, canal homes, alleys, laundry, household clutter, civilian life, small bridges, neighborhood shrines.

## Shrines
Shrine gates, offerings, incense, paper charms, stone lanterns, sacred trees, restrained spiritual atmosphere.

## Civic / Administrative
Formal offices, official signage, records, guards, controlled plazas, administrative props.

## Palace
Monumental gates, refined stone, formal courtyards, Imperial ornament, guard infrastructure, premium materials, court interiors.

## Industrial Infrastructure
Elevated rail, gantries, pipes, pumps, utility towers, lifts, gauges, cathode devices, maintenance spaces.

## Fringe Ward
Broken paving, patched construction, improvised shops, salvaged materials, damaged infrastructure, combat spaces, worn but still high-quality art.

---

# 19. Presentation & Development QA Rules

**Production-acceptance previews** must show an integrated gameplay view. Isolated source sheets are not evidence that a gameplay checklist item is complete.

**Development QA**, however, should intentionally remain compact and narrowly scoped. Use isolated assets or contact sheets when the specific question is contamination, anchor placement, direction, garment overlap, silhouette, or source quality.

A presentation-quality gameplay preview must contain fully clothed characters, near-final world assets, layered architecture, district-specific clutter, props, occlusion, material variety, contact / cast shadows, hidden-grid-friendly surfaces, coherent lighting, and equivalent character / world quality.

Do not present mannequin characters, blockout architecture, generic rectangles, low-detail placeholder trees, temporary composites, or asset tests as finished scenes.

Do not turn routine development QA into large decorative presentation boards. Keep explanatory text and progress reporting outside the artwork.

---

# 20. Mandatory Art Review Gate

All assets and integrated scenes must be reviewed against the **Astro Fighters Art Preview Review Rubric** before production acceptance.

Reference targets should be reviewed at source / benchmark stage before modular derivation, but **checklist completion is determined only by representative integrated Phaser gameplay**.

Development behavior:

- **Below 36:** continue development automatically
- **Automatic failure:** continue development automatically
- **Critical category below minimum:** continue development automatically
- **36–41:** internal test candidate only, provided all critical requirements pass
- **42–45:** production approved
- **46–50:** lock-quality visual target

A high aggregate score may not override a critical-category failure.

Critical minimum categories include Character / World Style Homogeneity, Character Completion & Clothing, Environment Pixel-Art Quality, Astro Fighters World Identity, Architectural Detail & Silhouette, and Projection / Depth / Occlusion.

---

# 21. Automatic Failure Conditions

A preview or asset pass fails immediately if:

- world art is visibly lower quality than character art
- environment primarily consists of primitive geometry
- characters are naked / mannequin-like
- clothing is incomplete or placeholder quality
- characters look pasted onto the environment
- buildings are generic boxes
- a baked image substitutes for layered playable world construction
- the hidden grid is visible
- pixel density / styles visibly clash
- environment resembles generic RPG Maker / vector / cyberpunk art
- directional bodies are obviously incorrect
- anatomical weapon / equipment routing is wrong
- clothing layers incorrectly cover anatomy because of coarse overlay ordering
- modular isolates contain neighboring-item contamination or presentation artifacts
- automatically reduced / segmented assets are presented as pixel-final without target-level cleanup
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

> Create production-quality pixel-art assets for Astro Fighters that match the approved character reference sheets in style, detail density, silhouette quality, material rendering, and craftsmanship. Lock the asset contract before generation, including canonical direction, dimensions, anchors, anatomical mount sides, layer roles, draw order, palette family, and runtime destination. Follow the required workflow: **reference target → purpose-built modular source assets → immediate isolation / anchor QA → source assembly / registration approval → target-resolution derivation → manual pixel cleanup → Phaser integration → integrated rubric review**. Do not treat a pretty reference image, crop, mechanical shrink, automatic segmentation, or template match as finished game art. Character source modules share the 480×640 anatomical lattice; runtime characters are 48×64 only after source approval and target-level pixel cleanup. S is front / toward camera and N is back / away from camera; legacy labels must be remapped in metadata. Equipment follows anatomical side, not screen side. Male paper-doll bases include shorts; female bases include shorts and a sports bra; other clothing / wraps / weapons / accessories remain modular. Keep QA images narrow and functional rather than producing large presentation boards. Keep failed experiments and temporary QA outside the repository, maintain stable canonical asset paths, and use Git history instead of accumulating `v##` package files. Build Imperial City as modular layered Phaser scenery for a hidden 32×32 square grid with smooth 8-direction movement. Proceed autonomously through world and character checklists by dependency package unless a major art-direction decision genuinely requires user approval. The world must equal the character models in pixel-art quality. If any source gate, runtime gate, automatic-failure condition, critical rubric minimum, or integrated score fails, continue refining automatically rather than lowering the target.
