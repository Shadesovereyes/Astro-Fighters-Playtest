# Astro Fighters — Art Preview Review Rubric

**Status:** Mandatory acceptance gate for all future gameplay-art previews.

This rubric exists to prevent placeholder-quality scenery, incomplete characters, mismatched art sources, and technically functional scenes from being mistaken for acceptable Astro Fighters art.

A preview is reviewed as a **single integrated game image**. Character art, clothing, architecture, props, terrain, lighting, effects, and UI-visible world elements must appear to belong to the same production.

---

## Automatic Failure Conditions

A preview is **REJECTED immediately** if any of the following are present:

- World art is visibly lower quality than the approved character pixel art.
- Environment primarily consists of flat rectangles, primitive geometry, or blockout assets.
- Bare or mannequin-like player/NPC bodies are used in a presentation-quality preview.
- Characters lack appropriate clothing, footwear, hair, equipment, or accessories.
- Characters look pasted over scenery rather than integrated into it.
- Buildings are represented by generic boxes rather than authored architecture.
- A baked full-screen image substitutes for layered playable world assets.
- The hidden 32×32 grid is visible through lines, checkerboarding, repeated seams, or obvious tile rhythm.
- Different elements visibly use different pixel-art styles or pixel densities.
- Environment art resembles generic RPG Maker, vector art, clean modern tilesets, or generic cyberpunk.
- Eight-direction movement is represented using obviously incorrect directional character bodies.
- Occluding scenery permanently hides the controlled character without an authored visibility solution.
- A preview is called “production quality” while still relying on known placeholder art.

Automatic-fail items cannot be compensated for by scoring highly elsewhere.

---

# Scored Review

Each category receives a score from **0–5**.

**0 — Missing / fundamentally incorrect**  
**1 — Placeholder quality**  
**2 — Partially developed but below target**  
**3 — Functional production candidate**  
**4 — Strong Astro Fighters quality**  
**5 — Reference-quality / locked target**

Maximum score: **50**

---

## 1. Character / World Style Homogeneity — 10% Critical

### 5
Characters and scenery appear to have been created by the same pixel artist or studio. Pixel density, outlines, shading, value grouping, texture density, and material rendering are coherent.

### 3
Generally compatible, but differences in detail density or rendering language remain noticeable.

### 1
Premium character sprites are visibly placed over lower-quality environment assets.

### 0
Character and world clearly belong to different visual styles.

**Minimum acceptable score: 4**

---

## 2. Character Completion & Clothing — 10% Critical

Characters appearing in presentation previews must include appropriate:

- skin/body
- hair
- inner top
- outerwear where appropriate
- pants
- footwear
- belt/sash
- equipment
- accessories
- contact shadow

Clothing must follow the **Edo + martial + hip-hop/streetwear** Astro Fighters language.

### 5
Character reads as a complete designed fighter with layered clothing, equipment, silhouette, and direction-aware details.

### 3
Character is dressed but lacks some distinctive Astro Fighters identity or accessory detail.

### 1
Basic clothing blocks or incomplete layers.

### 0
Bare/mannequin character.

**Minimum acceptable score: 4**

---

## 3. Environment Pixel-Art Quality — 10% Critical

Judge the scenery at the same scrutiny applied to the character sprites.

Look for:

- deliberate pixel clusters
- controlled edges
- material-specific shading
- readable wear
- localized texture
- meaningful silhouettes
- proper top/front face separation
- handcrafted variation

### 5
Environment art equals or exceeds character-art craftsmanship.

### 3
Good game art, but noticeably simpler than the character assets.

### 1
Mostly geometric shapes with decoration added on top.

### 0
Blockout.

**Minimum acceptable score: 4**

---

## 4. Astro Fighters World Identity — 10%

The scene should express:

- Edo daily-life influence
- martial culture
- hip-hop/streetwear cultural texture
- analog industrial infrastructure
- warm Japandi-industrial materials
- ancient monumental urban construction
- lived-in Imperial City density

### 5
The location is immediately recognizable as Astro Fighters.

### 3
Japanese/fantasy setting is apparent but could belong to another game.

### 1
Generic historical/fantasy environment.

### 0
No recognizable Astro Fighters identity.

**Minimum acceptable score: 4**

---

## 5. Material Quality & Variety — 10%

Materials should visually behave differently.

Required families include, when relevant:

- timber
- plaster
- stone
- cloth
- rope
- paper
- brass
- iron
- rust
- patina
- water
- foliage
- soot / grime

### 5
Material identity is clear without needing labels.

### 3
Materials are distinguishable but somewhat simplified.

### 1
Most surfaces appear as differently colored versions of the same flat shape.

### 0
No meaningful material rendering.

**Minimum acceptable score: 3**

---

## 6. Architectural Detail & Silhouette — 10%

Architecture should use:

- timber framing
- roof structures
- eaves
- shutters
- windows
- vents
- conduits
- signage
- balconies
- retaining walls
- gates
- railings
- structural hardware
- district-specific ornament

### 5
Buildings have distinctive silhouettes and believable construction.

### 3
Architecture works but still uses repetitive forms.

### 1
Decorated rectangles.

### 0
Placeholder boxes.

**Minimum acceptable score: 4**

---

## 7. Lived-In Density & Environmental Storytelling — 10%

A finished Imperial City location should contain evidence of human activity.

Possible elements:

- crates
- stools
- baskets
- tools
- signage
- cloth
- paper
- ropes
- carts
- lanterns
- drainage
- patched surfaces
- stains
- stored goods
- market displays
- workshop debris
- hanging objects
- personal belongings

### 5
Dense but readable; every area feels inhabited.

### 3
Some good clutter, but large areas still feel staged or empty.

### 1
A few props scattered over empty terrain.

### 0
Empty blockout.

**Minimum acceptable score: 3**

---

## 8. Projection, Depth & Occlusion — 10%

Must obey the locked cabinet-style 3/4 world projection.

Depth should come from:

- overlap
- top/front face separation
- Y-sorting
- contact shadows
- cast shadows
- architecture height
- walk-behind objects
- foreground elements
- authored cutaways

### 5
World feels layered and spatial while remaining readable.

### 3
Depth mostly works with a few flat or ambiguous areas.

### 1
Objects appear pasted onto a flat floor.

### 0
Projection is inconsistent or mechanically unusable.

**Minimum acceptable score: 4**

---

## 9. Hidden-Grid Concealment & Movement Readability — 5%

The game uses a **hidden 32×32 square grid with eight-direction movement**.

The player must not perceive the grid from ordinary art.

### 5
Space feels continuous and natural while supporting clear movement.

### 3
Minor modular repetition is noticeable but not distracting.

### 1
Tile rhythm strongly suggests the underlying grid.

### 0
Grid/cell construction is plainly visible.

**Minimum acceptable score: 4**

---

## 10. Gameplay Screenshot Readiness — 5%

Final question:

> **Could this image be shown publicly as a representative Astro Fighters gameplay screenshot without needing an explanation that the art is temporary?**

### 5
Yes.

### 4
Yes, with only minor polish remaining.

### 3
Good internal production preview.

### 2
Clearly unfinished.

### 1
Prototype.

### 0
Blockout.

**A public-facing benchmark must score at least 4.**

---

# District-Specific Identity Check

Every scene must also clearly communicate its district.

### Imperial Harbor / Docks
Expected cues include docks, cargo, ropes, cranes/hoists, warehouses, wet stone, mooring infrastructure, boats/barge elements, nets, harbor trade clutter.

### Civic Market / Shops
Expected cues include storefronts, signs, awnings, merchandise, carts, food/textile stalls, pedestrians, narrow dense commercial streets.

### Academy
Expected cues include ceremonial gate, dojo architecture, training courtyard, weapon racks, target posts, scrolls/notices, banners, martial-training equipment.

### Workshops
Expected cues include workbenches, tools, furnaces, racks, ventilation, material storage, unfinished goods, repair clutter.

### Shrines
Expected cues include shrine gates, offerings, prayer plaques, incense, stone lanterns, ropes/bells, moss/foliage, ritual objects.

### Palace / Administrative Precinct
Expected cues include larger architectural scale, refined stone, controlled symmetry, banners, monumental gates, ceremonial fixtures, guard infrastructure and high-status materials.

A district should not merely be the same environment with a few props swapped.

---

# Character Integration Check

For every character visible in a review image, confirm:

- [ ] Character is fully clothed.
- [ ] Clothing fits Astro Fighters fashion language.
- [ ] Hair is production quality.
- [ ] Footwear is present and readable.
- [ ] Belt/sash or equivalent waist treatment is present.
- [ ] Equipment is correctly positioned.
- [ ] Accessories are integrated.
- [ ] Character has a believable contact shadow.
- [ ] Character shares the environment's lighting.
- [ ] Character pixel density matches nearby scenery.
- [ ] Character does not look pasted over the scene.
- [ ] Directional anatomy is appropriate for current facing.

---

# Environment Integration Check

- [ ] Ground contains authored variation.
- [ ] Architecture is not primitive geometry.
- [ ] Props are individually authored.
- [ ] Materials are visually distinguishable.
- [ ] Signs and fixtures are integrated into buildings.
- [ ] Tall objects support occlusion.
- [ ] Foreground elements reinforce depth where useful.
- [ ] Major buildings dwarf the fighter appropriately.
- [ ] Repetition does not expose hidden grid construction.
- [ ] Scene contains district-appropriate clutter.
- [ ] World contains no inappropriate clean holographic sci-fi language.
- [ ] Character remains readable in the fully detailed environment.

---

# Score Thresholds

**46–50 — LOCK QUALITY**  
Approved as a visual target for subsequent assets.

**42–45 — PRODUCTION APPROVED**  
Suitable for integration; minor polish may continue.

**37–41 — CONDITIONAL**  
Promising, but requires another review pass.

**30–36 — REWORK REQUIRED**  
Major visual deficiencies remain.

**Below 30 — REJECTED**  
Does not represent Astro Fighters production art.

Regardless of total score:

- Character/World Homogeneity must be **4+**
- Character Completion must be **4+**
- Environment Pixel Quality must be **4+**
- World Identity must be **4+**
- Architecture must be **4+**
- Projection/Depth must be **4+**

Failure of any critical minimum prevents approval.

---

# Final Approval Question

Before accepting any scene, answer:

> **Does this look like premium Astro Fighters character art inhabiting a premium Astro Fighters world — or does it look like premium character art placed inside a cheaper environment?**

If the second interpretation is reasonably possible, the scene is **not approved**.

The quality of the world must rise to the character standard. The character standard must never be lowered to make the environment mismatch less obvious.