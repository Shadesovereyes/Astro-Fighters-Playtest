# Astro Fighters — Character Clothing & Accessory Production Checklist

**Status:** Production checklist  
**Scope:** Playable fighters, NPCs, guards, merchants, workers, students, instructors, officials, civilians, and hostile human characters.  
**Purpose:** Ensure every visible character reaches Astro Fighters production quality before integration into a testable gameplay scene.

---

# 1. Mandatory Character Completion Stack

Every presentation-quality character must include all required visible layers.

## Base Character
- [ ] Approved body / skin variant
- [ ] Approved face / eye treatment
- [ ] Approved hairstyle
- [ ] Correct feet anchor
- [ ] Correct contact shadow
- [ ] No exposed mannequin/base-body areas unless intentionally part of the outfit
- [ ] Silhouette remains readable at 48×64 runtime scale

## Core Clothing
- [ ] Inner top
- [ ] Outerwear where appropriate
- [ ] Pants / lower-body garment
- [ ] Footwear
- [ ] Belt / sash / waist treatment
- [ ] Sleeve / cuff treatment where applicable
- [ ] Collar / neckline treatment
- [ ] Garment closures, ties, wraps, cords, or fasteners
- [ ] Clothing folds remain readable at runtime scale

## Equipment
- [ ] Weapon if role requires one
- [ ] Scabbard / holster / sheath where applicable
- [ ] Equipment attachment point is believable
- [ ] Weapon does not float or clip through body
- [ ] Equipment routing changes correctly by facing direction
- [ ] Weapon silhouette remains readable against clothing

## Accessories
- [ ] Charm / talisman / tag
- [ ] Pouch or utility storage where appropriate
- [ ] Wrist wraps / bracelets where appropriate
- [ ] Neck cord / beads / pendant where appropriate
- [ ] Shoulder tie / cloth strip where appropriate
- [ ] Scabbard cord / weapon charm where appropriate
- [ ] Profession-specific accessory where appropriate
- [ ] Accessories enhance role identity instead of becoming visual noise

---

# 2. Eight-Direction Clothing Validation

Every clothing and accessory layer must be authored for:

- [ ] N
- [ ] NE
- [ ] E
- [ ] SE
- [ ] S
- [ ] SW
- [ ] W
- [ ] NW

For every direction confirm:

- [ ] Head and hairstyle silhouette changes appropriately
- [ ] Shoulder width and torso angle are correct
- [ ] Hips and leg spacing are correct
- [ ] Feet placement matches facing
- [ ] Inner top follows body rotation
- [ ] Outerwear changes silhouette by direction
- [ ] Sleeves overlap arms correctly
- [ ] Pants / hakama folds turn with the body
- [ ] Footwear orientation changes correctly
- [ ] Sash / belt wraps around the body correctly
- [ ] Scabbard moves to the correct visible side
- [ ] Weapon angle is direction-aware
- [ ] Charms / pouches / tags move to the correct front/back side
- [ ] No front-facing body reuse disguised by minor edits
- [ ] No mirrored-looking equipment errors
- [ ] No floating layers
- [ ] No broken front/back occlusion

---

# 3. Animation Coverage

Each approved fighter clothing stack must support:

## Idle
- [ ] 4 frames per direction
- [ ] Clothing remains anchored
- [ ] Hair has restrained secondary motion where appropriate
- [ ] Sash / cloth tails remain stable
- [ ] Weapon stays attached
- [ ] Accessories do not jitter

## Walk
- [ ] 6 frames per direction
- [ ] Pants move with leg cycle
- [ ] Coat / haori reacts to movement
- [ ] Hair movement is directionally believable
- [ ] Sash / cord motion is restrained
- [ ] Scabbard follows hip movement
- [ ] Footwear stays aligned to feet
- [ ] No garment popping between frames

## Ready
- [ ] 2 frames per direction
- [ ] Stance silhouette is clearly different from idle
- [ ] Weapon readiness is readable
- [ ] Clothing tension reflects combat stance
- [ ] Scabbard / weapon routing remains correct
- [ ] Accessories remain legible

---

# 4. Playable Fighter Clothing Families

## Inner Tops
- [ ] Wrapped martial top
- [ ] Sleeveless fighter wrap
- [ ] Cropped fitted underlayer
- [ ] Hooded underlayer
- [ ] Banded chest-wrap top

## Outerwear
- [ ] Patterned haori
- [ ] Utility haori
- [ ] Short street jacket
- [ ] Split-tail street haori
- [ ] Sleeveless battle coat
- [ ] Scarf-collar fighter jacket

## Pants
- [ ] Loose fighter trousers
- [ ] Cuffed worker trousers
- [ ] Hakama-influenced combat pants
- [ ] Wrapped-shin trousers
- [ ] Reinforced street-martial slacks

## Footwear
- [ ] Wrapped boots
- [ ] Tabi-boot hybrid
- [ ] Sandal-boot hybrid
- [ ] Sneaker-hybrid martial shoe

## Waist Treatments
- [ ] Rope sash
- [ ] Cloth obi
- [ ] Charm-cord belt
- [ ] Pouch belt
- [ ] Bead-tie sash
- [ ] Weapon-support sash

## Fighter Accessories
- [ ] Charm tag
- [ ] Wrist wraps
- [ ] Neck cord
- [ ] Bead ties
- [ ] Shoulder cloth ties
- [ ] Talisman strips
- [ ] Utility pouch
- [ ] Scabbard cord
- [ ] Small field kit
- [ ] Academy insignia variant
- [ ] District / faction badge variant

---

# 5. Hairstyle Production Checklist

Priority Afro-descended hairstyles:

- [ ] Short Afro
- [ ] High Puff
- [ ] Short Freeform Locs
- [ ] Braided Twists
- [ ] Puff Undercut

For each hairstyle:

- [ ] Distinct silhouette in all 8 directions
- [ ] Front / side / back volume is believable
- [ ] Hair does not flatten into a generic helmet shape
- [ ] Hair reads clearly against dark backgrounds
- [ ] Hair reads clearly against light backgrounds
- [ ] Hair back/front routing is direction-sensitive
- [ ] Hairstyle remains recognizable at 48×64
- [ ] No arbitrary colors outside the approved palette

---

# 6. Weapon & Equipment Accessories

## Katana / Sword Set
- [ ] Katana
- [ ] Scabbard
- [ ] Scabbard cord
- [ ] Guard / hilt detail
- [ ] Weapon charm
- [ ] Direction-aware front/back routing
- [ ] Correct hand/hip relationship
- [ ] Correct ready-state positioning

## General Weapon Support
- [ ] Belt attachment
- [ ] Back carry if role requires it
- [ ] Hip carry if role requires it
- [ ] Strap / sling if role requires it
- [ ] Weapon never clips through outerwear
- [ ] Equipment silhouette remains readable

## Utility Equipment
- [ ] Trap pouch
- [ ] Tool pouch
- [ ] Scroll case
- [ ] Merchant satchel
- [ ] Courier bag
- [ ] Guard utility belt
- [ ] Engineer tool harness
- [ ] Dockworker rope/tool bundle
- [ ] Shrine charm bundle

---

# 7. District / Profession Clothing Sets

## Imperial Harbor / Docks
### Dockworker
- [ ] Wrapped work top
- [ ] Short utility outer layer
- [ ] Durable cuffed trousers
- [ ] Work boots
- [ ] Rope belt
- [ ] Gloves / wrist wraps
- [ ] Rope or cargo-handling accessory

### Fisher
- [ ] Weather-resistant outer layer
- [ ] Practical lower garment
- [ ] Water-safe footwear
- [ ] Net / hook / basket accessory
- [ ] Head wrap or practical hair treatment where appropriate

### Merchant
- [ ] Cleaner merchant top
- [ ] Layered outerwear
- [ ] Sash
- [ ] Satchel / money pouch
- [ ] Trade tag / ledger accessory

### Harbor Guard
- [ ] Guard jacket / haori
- [ ] Reinforced trousers
- [ ] Guard footwear
- [ ] Weapon
- [ ] Scabbard
- [ ] Belt
- [ ] Imperial identification accessory

---

## Civic Market / Shops
### General Merchant
- [ ] Shopkeeper top
- [ ] Civilian haori / outer layer
- [ ] Trousers
- [ ] Footwear
- [ ] Money pouch
- [ ] Shop-specific accessory

### Food Vendor
- [ ] Work wrap
- [ ] Apron
- [ ] Tied sleeves
- [ ] Practical footwear
- [ ] Towel / utensil accessory

### Textile Seller
- [ ] Cleaner layered clothing
- [ ] Cloth-measuring accessory
- [ ] Fabric sash / decorative trim
- [ ] Merchant pouch

### Courier
- [ ] Short jacket
- [ ] Cuffed trousers
- [ ] Running-friendly footwear
- [ ] Cross-body bag
- [ ] Message tag / delivery marker

### Civic Guard
- [ ] Guard uniform
- [ ] Sash
- [ ] Weapon
- [ ] Scabbard
- [ ] Guard insignia
- [ ] Reinforced footwear

---

## Artisan / Workshop Ward
### Carpenter
- [ ] Work top
- [ ] Work apron
- [ ] Cuffed trousers
- [ ] Durable footwear
- [ ] Tool belt
- [ ] Carpenter tools

### Smith
- [ ] Heat-safe work top
- [ ] Heavy apron
- [ ] Arm wraps / gloves
- [ ] Reinforced trousers
- [ ] Heavy footwear
- [ ] Hammer / tongs accessory
- [ ] Soot treatment

### Mechanic / Engineer
- [ ] Utility jacket
- [ ] Work trousers
- [ ] Tool harness
- [ ] Gloves
- [ ] Protective wrap / eyewear if stylistically approved
- [ ] Gauge / tool accessory

### Textile Worker
- [ ] Work wrap
- [ ] Apron
- [ ] Sleeve ties
- [ ] Cloth / spool accessory
- [ ] Practical footwear

### Apprentice
- [ ] Simplified worker outfit
- [ ] Basic belt
- [ ] Training / helper tool
- [ ] Less ornate than master craftsperson

---

## Astro Fighter Academy
### Student
- [ ] Academy inner top
- [ ] Academy outer layer
- [ ] Training trousers
- [ ] Martial footwear
- [ ] Academy sash
- [ ] Academy insignia
- [ ] Training equipment where appropriate

### Senior Student
- [ ] Distinct trim / sash
- [ ] More developed outerwear
- [ ] Rank indicator
- [ ] Weapon access where appropriate

### Instructor
- [ ] Senior martial outerwear
- [ ] Instructor sash
- [ ] Practical combat trousers
- [ ] Weapon
- [ ] Academy authority marker

### Sensei
- [ ] Distinct senior silhouette
- [ ] Premium but restrained garment treatment
- [ ] Strong sash / belt design
- [ ] Role-specific accessory
- [ ] High-readability silhouette at gameplay scale

### Groundskeeper / Attendant
- [ ] Workwear
- [ ] Academy identification
- [ ] Tool / maintenance accessory

---

## Residential / Canal Neighborhoods
### Civilian Adult
- [ ] Everyday inner top
- [ ] Optional light outerwear
- [ ] Civilian trousers / skirted equivalent where designed
- [ ] Footwear
- [ ] Small household accessory

### Elder
- [ ] Distinct age silhouette
- [ ] Layered civilian clothing
- [ ] Walking staff / household accessory where appropriate

### Household Worker
- [ ] Work wrap
- [ ] Apron / sash
- [ ] Practical footwear
- [ ] Bucket / broom / basket accessory

### Teen / Youth
- [ ] Simplified streetwear-martial mix
- [ ] Distinct youthful silhouette
- [ ] Small bag / charm where appropriate

---

## Shrine / Spiritual Areas
### Shrine Attendant
- [ ] Ritual inner layer
- [ ] Shrine outer garment
- [ ] Sash
- [ ] Appropriate footwear
- [ ] Charm / prayer accessory

### Priest / Monk Equivalent
- [ ] Distinct ceremonial silhouette
- [ ] Layered robes adapted to Astro Fighters pixel style
- [ ] Beads / talisman / ritual tool
- [ ] Restrained spiritual ornament

### Pilgrim / Worshipper
- [ ] Civilian layers
- [ ] Travel wrap
- [ ] Offering / prayer accessory

---

## Civic / Administrative Ward
### Clerk
- [ ] Formal civilian top
- [ ] Administrative outer layer
- [ ] Neat trousers
- [ ] Formal footwear
- [ ] Document case / scroll bundle

### Official
- [ ] Higher-status outerwear
- [ ] Imperial trim
- [ ] Formal sash
- [ ] Seal / badge accessory
- [ ] Refined footwear

### Inspector
- [ ] Utility-formal hybrid
- [ ] Identification marker
- [ ] Document / tool accessory
- [ ] Practical outerwear

---

## Imperial Palace
### Imperial Guard
- [ ] Elite guard inner layer
- [ ] Structured outerwear
- [ ] Reinforced trousers
- [ ] Elite footwear
- [ ] Guard sash
- [ ] Weapon
- [ ] Scabbard
- [ ] Imperial crest / badge

### Guard Officer
- [ ] Higher-status guard silhouette
- [ ] Distinct trim
- [ ] Command accessory
- [ ] Premium weapon fittings

### Court Official
- [ ] Formal high-status layers
- [ ] Refined sash
- [ ] Court marker / seal
- [ ] Restrained ornament

### Palace Attendant
- [ ] Formal service clothing
- [ ] Palace identification
- [ ] Tray / document / utility accessory

### Noble / Court Civilian
- [ ] Premium textiles
- [ ] Layered silhouette
- [ ] Controlled ornament
- [ ] High-status accessory

---

## Industrial / Infrastructure Corridors
### Engineer
- [ ] Utility coat / jacket
- [ ] Work trousers
- [ ] Heavy footwear
- [ ] Tool harness
- [ ] Gloves
- [ ] Maintenance accessory

### Rail / Utility Worker
- [ ] Work top
- [ ] Reinforced trousers
- [ ] Utility sash
- [ ] Work boots
- [ ] Tool / lantern / maintenance tag

### Utility Guard
- [ ] Guard-workwear hybrid
- [ ] Weapon
- [ ] Belt
- [ ] Infrastructure identification marker

---

## Fringe / Outer Ward
### Fringe Civilian
- [ ] Worn but authored civilian layers
- [ ] Patched outerwear
- [ ] Practical footwear
- [ ] Small personal utility accessory

### Salvager
- [ ] Layered workwear
- [ ] Salvage harness / belt
- [ ] Gloves / wraps
- [ ] Tool
- [ ] Bag / scrap carrier

### Local Fighter
- [ ] Improvised martial clothing
- [ ] Distinct street-fighter silhouette
- [ ] Sash
- [ ] Weapon / wraps as appropriate
- [ ] Worn accessories

### Hostile Street Fighter
- [ ] Full outfit
- [ ] Clear combat silhouette
- [ ] Role-appropriate equipment
- [ ] No generic bandit costume
- [ ] Still recognizably Astro Fighters

---

# 8. Palette Compliance

All clothing and accessory colors must use the approved Astro Fighters master palette.

For every layer:
- [ ] Base color comes from an approved palette family
- [ ] Shadow step is palette-compliant
- [ ] Highlight step is palette-compliant
- [ ] Trim color is palette-compliant
- [ ] Metallic accessories use approved metal ramps
- [ ] Leather / rope / cloth use appropriate material families
- [ ] Imperial vermilion is used as punctuation, not ambient fill
- [ ] No arbitrary browser RGB values
- [ ] Cosmetic variants use discrete approved swatches

---

# 9. Material Rendering Checklist

## Cloth
- [ ] Soft fold rhythm
- [ ] Different edge treatment from metal
- [ ] Readable seam / wrap / cuff where needed
- [ ] Not rendered like flat plastic

## Leather / Rope
- [ ] Distinct texture from cloth
- [ ] Believable wear
- [ ] Correct highlight restraint

## Metal
- [ ] Controlled highlight
- [ ] Clean or rusted family selected intentionally
- [ ] Weapon fittings remain readable

## Wood / Beads
- [ ] Small but readable material cue
- [ ] Does not visually merge with skin or cloth

## Paper / Talisman
- [ ] Light material read
- [ ] Dark ink/mark detail where appropriate
- [ ] Does not become a bright UI-like element

---

# 10. Silhouette & Readability Gate

At 48×64 runtime scale:

- [ ] Character role is readable before zooming
- [ ] Hairstyle is recognizable
- [ ] Outerwear silhouette is recognizable
- [ ] Pants silhouette is recognizable
- [ ] Footwear is visible
- [ ] Waist treatment is readable
- [ ] Weapon location is clear
- [ ] Main accessory is visible
- [ ] Character does not visually merge into world background
- [ ] Clothing detail does not become noisy
- [ ] Light/dark grouping supports pose readability

---

# 11. Environment Integration Gate

Before any outfit is accepted into a playable scene:

- [ ] Character lighting matches the environment
- [ ] Character pixel density matches scenery
- [ ] Contact shadow matches world projection
- [ ] Outfit colors remain readable against timber
- [ ] Outfit colors remain readable against stone
- [ ] Outfit colors remain readable against water
- [ ] Outfit colors remain readable against dark interiors
- [ ] Outfit colors remain readable against foliage
- [ ] Character can pass behind props without broken layering
- [ ] Character can pass in front of props without broken layering
- [ ] Tall occluders interact correctly
- [ ] Clothing does not clip through walls / counters / architecture during ordinary movement
- [ ] Equipment does not disappear incorrectly during Y-sorting

---

# 12. Character Variant Production Rule

Do not expand into large cosmetic libraries until one complete stack is approved.

First complete stack:

- [ ] 1 body / skin
- [ ] 1 Afro hairstyle
- [ ] 1 inner top
- [ ] 1 outerwear
- [ ] 1 pants
- [ ] 1 footwear
- [ ] 1 sash / belt
- [ ] 1 katana
- [ ] 1 scabbard
- [ ] 1 charm / accessory
- [ ] 1 shadow
- [ ] All 8 directions
- [ ] Idle complete
- [ ] Walk complete
- [ ] Ready complete
- [ ] Environment integration complete
- [ ] Rubric critical categories satisfied

Only after this stack passes should additional variants be expanded.

---

# 13. Presentation Preview Requirements

No character-focused gameplay preview may be presented as testable unless:

- [ ] Player is fully clothed
- [ ] NPCs are fully clothed
- [ ] All visible clothing is production-quality or near-production-quality
- [ ] Accessories are integrated
- [ ] No mannequin/base character is visible
- [ ] Directional anatomy is correct
- [ ] Character/world style homogeneity passes review
- [ ] Environment itself passes its critical art gates
- [ ] Integrated preview reaches required rubric threshold

---

# 14. Automatic Character Failure Conditions

A character asset is rejected immediately if:

- [ ] Bare mannequin/body is used in a presentation preview
- [ ] Clothing is represented by basic blocks
- [ ] Front-facing anatomy is reused across directions
- [ ] Equipment floats
- [ ] Weapon/scabbard routing is wrong
- [ ] Hair becomes a generic helmet silhouette
- [ ] Clothing pixel density is lower than the approved character references
- [ ] Arbitrary non-palette colors are introduced
- [ ] Character looks pasted over the world
- [ ] Character's clothing does not fit Astro Fighters' Edo + martial + hip-hop language
- [ ] Critical garment details disappear at 48×64
- [ ] Clothing or accessory layers visibly jitter during animation
- [ ] Contact shadow is missing in presentation gameplay

Any automatic failure requires further development before integration.

---

# 15. Character Review Scorecard

Score each integrated character from 0–5:

| Category | Score |
|---|---:|
| Character completion | /5 |
| Clothing design identity | /5 |
| Eight-direction quality | /5 |
| Animation stability | /5 |
| Hair silhouette quality | /5 |
| Equipment/accessory routing | /5 |
| Material rendering | /5 |
| Palette compliance | /5 |
| Runtime readability | /5 |
| World integration | /5 |
| **Total** | **/50** |

## Character-specific acceptance guidance
- **46–50:** lock-quality character target
- **42–45:** production approved
- **37–41:** conditional; refine before broad variant expansion
- **36 or below:** continue development
- Any automatic failure: continue development regardless of total

---

# 16. Final Character Approval Question

Before any clothing/accessory stack is approved, ask:

> **Does this look like a fully designed Astro Fighters character whose clothing, hair, equipment, and accessories were authored as carefully as the base sprite — or does it look like a good character sprite with costume pieces placed on top?**

If the second interpretation is reasonably possible, the character is not approved.
