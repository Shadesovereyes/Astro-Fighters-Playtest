# Astro Fighters — Art Preview Review Rubric

**Status:** Mandatory acceptance gate for gameplay-art previews  
**Machine authority:** `docs/data/art-review-rubric.json`

This document is the human-readable form of the machine rubric. The automatic-failure list, category minimums, and score thresholds must remain synchronized with `docs/data/art-review-rubric.json`.

An **integrated gameplay review is valid only from the running Phaser canvas**. Concept art, presentation boards, source assemblies, contact sheets, Python/PIL composites, and mock renderers may be reviewed as references or QA artifacts, but they cannot receive an integrated gameplay approval score.

---

## Automatic Failure Conditions

A preview is rejected immediately if any of the following is present:

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
- Anatomical weapon or equipment routing is wrong for one or more facings.
- Clothing layers incorrectly cover anatomy because of coarse overlay ordering.
- Modular isolates contain neighboring-item contamination or presentation artifacts.
- Automatically reduced or segmented assets are presented as pixel-final without target-level cleanup.
- Occluding scenery permanently hides the controlled character without an authored visibility solution.
- A preview is called production quality while still relying on known placeholder art.
- A non-Phaser preview, collage, source assembly, or mock renderer is presented as integrated gameplay.
- Fixed grid-step exploration is presented as the final open-world movement model.

Automatic failures cannot be offset by a high numeric total.

---

# Scored Review

Score each category from **0–5**.

- **0 — Missing / fundamentally incorrect**
- **1 — Placeholder quality**
- **2 — Partially developed but below target**
- **3 — Functional production candidate**
- **4 — Strong Astro Fighters quality**
- **5 — Reference-quality / locked target**

Maximum score: **50**

## 1. Character / World Style Homogeneity — Critical, minimum 4

Judge whether characters and scenery share the same pixel density, cluster language, outlines, shading, value grouping, texture density, and material treatment. A premium character placed over weaker scenery fails this category even if both pieces are individually attractive.

## 2. Character Completion & Clothing — Critical, minimum 4

Presentation characters must read as complete designed fighters or civilians, with appropriate body/skin, hair, clothing, footwear, waist treatment, role equipment/accessories, and contact shadow. Clothing must follow the Astro Fighters Edo + martial + hip-hop/streetwear language. Mannequin presentation is an automatic failure.

## 3. Environment Pixel-Art Quality — Critical, minimum 4

Judge the world at the same scrutiny as the character art: deliberate pixel clusters, controlled edges, material-specific shading, localized wear, readable silhouette, handcrafted variation, and clear top/front-face construction. Primitive geometry with decoration added on top is insufficient.

## 4. Astro Fighters World Identity — Critical, minimum 4

The scene should communicate Astro Fighters specifically: Edo daily-life structure, martial culture, hip-hop/streetwear social texture, restrained analog infrastructure, warm Japandi material discipline, inherited ancient civic construction, and a lived-in Imperial City identity. Generic Japanese fantasy is not enough.

## 5. Material Quality & Variety — Minimum 3

Relevant materials must behave differently through value, cluster pattern, edge treatment, wear, highlight/shadow response, and palette. Typical families include timber, plaster, civic stone, cloth, rope, paper, clean iron, patinated copper, rust, water, foliage, soot/grime, and restrained cathode elements.

## 6. Architectural Detail & Silhouette — Critical, minimum 4

Architecture must have believable construction and distinct silhouettes: timber framing, eaves, shutters, windows, retaining walls, verandas, railings, gates, service housings, signage, and district-specific details. Decorated boxes fail.

## 7. Lived-In Density & Environmental Storytelling — Minimum 3

Use readable evidence of habitation: crates, stools, baskets, tools, paper, rope, carts, lanterns, drainage, repaired surfaces, stored goods, household objects, trade displays, and role-specific clutter. Density must remain restrained enough for navigation and silhouette readability.

## 8. Projection, Depth & Occlusion — Critical, minimum 4

The world must obey the locked flat-faced 3/4 cabinet projection and create depth through overlap, top/front-face separation, Y/depth sorting, contact/cast shadows, walk-behind elements, foreground occluders, architecture height, and authored cutaways. The player must be able to move in front of and behind appropriate objects in Phaser.

## 9. Hidden-Grid Concealment & Movement Readability — Minimum 4

The internal 32×32 logic must not be visible through pavement joints, checkerboarding, floorboards, prop spacing, architecture rhythm, or persistent overlays. Normal exploration must feel continuous even when hidden spatial quantization is used internally.

## 10. Gameplay Screenshot Readiness — Public minimum 4

Ask: **Could this running Phaser frame be shown publicly as representative Astro Fighters gameplay without explaining that the art is temporary?** A score below 4 is not public-ready.

---

# District Identity Checks

These are cues, not prompt-token lists. Always interpret them through the locked Master Art Direction.

- **Imperial Harbor / Docks:** quay, piers, cargo, rope systems, warehouses/shipwright frontage, matte waterline-darkened stone, boats, nets, restrained hoist/loading infrastructure.
- **Civic Market / Shops:** storefronts, signs, awnings, merchandise, carts, vendor stalls, narrow commercial passages, merchants/civilians.
- **Residential / Canal:** dense housing, canal edges, laundry, household clutter, small bridges, plants, neighborhood life.
- **Academy:** gates, dojo construction, training courtyard, practice equipment, banners/insignia, students/instructors, furnished cutaway interiors.
- **Workshops:** workbenches, hand tools, material racks, repair stock, sealed service housings, practical ventilation, active labor clutter.
- **Shrines / spiritual pockets:** offerings, prayer plaques, ropes/bells, stone lanterns, moss/foliage, restrained ritual objects.
- **Palace / administrative precinct:** larger civic scale, refined stone, controlled symmetry, banners, ceremonial fixtures, guard infrastructure, high-status materials.

A district may not be differentiated only by swapping props on otherwise generic buildings.

---

# Character Integration Check

For every visible review character confirm:

- fully clothed and role-appropriate;
- production-quality hair;
- readable footwear and waist treatment;
- accessories/equipment integrated without clipping;
- correct anatomical equipment side and facing-specific routing;
- believable contact shadow and shared lighting;
- runtime pixel density matches nearby scenery;
- directional anatomy is correct;
- the character does not appear pasted onto the environment.

# Environment Integration Check

Confirm:

- authored ground variation without visible grid cadence;
- architecture is not primitive geometry;
- props and dressing are individually authored;
- materials are distinguishable;
- tall objects support live occlusion/depth behavior;
- the player remains readable at full environment detail;
- collision/traversal space is believable;
- no inappropriate clean holographic, cyberpunk, wet-reflective, or steampunk visual language is present.

---

# Score Thresholds

| Score | Classification | Required behavior |
|---|---|---|
| **46–50** | **LOCK QUALITY** | Approved as a visual authority for subsequent assets. |
| **42–45** | **PRODUCTION APPROVED** | Relevant integrated checklist items may be marked complete. |
| **37–41** | **CONDITIONAL** | Internal candidate only; checklist remains open. |
| **30–36** | **REWORK REQUIRED** | Continue development. |
| **0–29** | **REJECTED** | Does not represent production art. |

Regardless of total score, approval also requires:

- zero automatic failures;
- Character / World Style Homogeneity **4+**;
- Character Completion & Clothing **4+**;
- Environment Pixel-Art Quality **4+**;
- Astro Fighters World Identity **4+**;
- Architectural Detail & Silhouette **4+**;
- Projection, Depth & Occlusion **4+**.

Checklist completion begins at **42**, never at 36 or 37.

---

# Final Approval Question

> **Does this look like premium Astro Fighters character art inhabiting a premium Astro Fighters world, rendered as a real layered Phaser scene — or does it look like premium character art placed inside a cheaper or flattened environment?**

If the second interpretation is reasonably possible, the scene is not approved.
