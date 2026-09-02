# Astro Fighters — Source File Authority Rule

**Status:** LOCKED production rule  
**Scope:** all files explicitly designated as `SOURCE`, `SOURCE CANDIDATE`, `PIXEL SOURCE`, `SOURCE PASS`, canonical source sheets, source masters, modular source layers, and source manifests.  
**Purpose:** prevent generated or inferred art from silently redesigning details that are already defined by source material.

---

# 1. Governing Rule

When an Astro Fighters file is explicitly identified as a **source file**, every visible construction detail in that source is locked unless the user explicitly changes or supersedes it.

> **SOURCE DEFINES THE OBJECT. NEW WORK MAY COMPLETE MISSING INFORMATION; IT MAY NOT REDESIGN INFORMATION THE SOURCE ALREADY DEFINES.**

A missing direction, animation frame, hidden underlayer, or modular component may require new authored pixels. Those new pixels must preserve the source-defined design and solve only the genuinely missing viewpoint / motion / hidden geometry.

---

# 2. Details That Must Be Preserved From Source

Unless explicitly changed by the user, source-defined details include, but are not limited to:

- body proportions and anatomical build;
- head size and facial construction;
- skin treatment;
- hair silhouette, texture, mass, hairline, tied sections, and major strand grouping;
- underwear / base-garment topology and coverage;
- sports-bra strap count, strap attachment points, back-band construction, neckline, and coverage;
- shorts / briefs shape, waistband height, leg openings, and coverage;
- wrist, ankle, chest, leg, or other wraps;
- footwear or deliberately bare-foot treatment;
- garment seams, hems, openings, collars, sleeves, cuffs, and panels;
- equipment type, mount, attachment point, and anatomical side;
- accessory placement;
- palette/material relationships;
- silhouette proportions;
- established anchor / registration relationships;
- any other repeated construction feature clearly visible in the source.

Changing one of these details in a generated or inferred direction is a **source-fidelity failure**, not an acceptable interpretation.

---

# 3. Missing-Direction Rule

When a source sheet provides some directions but not others:

- existing source directions are the construction authority;
- missing directions must be independently authored for the new viewpoint;
- new viewpoints may alter foreshortening, visible side, overlap, and perspective only as required by rotation;
- they may not introduce alternate garment designs, alternate hair construction, different strap topology, changed coverage, different wrap placement, or different anatomy;
- mirroring, duplication, relabeling, or interpolation may be used only as diagnostic/reference aids, never as automatic approval of a missing direction;
- any generated proposal that conflicts with a source-defined detail must be rejected or corrected before promotion.

The correct question is always:

> **What does this same source-defined object look like from the missing direction?**

not:

> **What is another plausible version of this object?**

---

# 4. Source vs Reference Priority

When source and non-source reference material disagree:

1. explicit user instruction wins;
2. current canonical `SOURCE PASS` / locked source authority wins;
3. current source candidate / canonical source sheet governs construction unless superseded;
4. illustrative `REFERENCE PASS` guides only details not contradicted by source;
5. generated exploratory material has no authority over source-defined construction.

A polished generated image may remain useful as `REFERENCE ONLY`, but it may not silently overwrite source-defined details.

---

# 5. QA Requirement — Source-Fidelity Check

Before a newly authored direction, animation frame, or modular layer can pass source QA, compare it against the relevant source authorities and verify:

- same character identity;
- same anatomy/proportion family;
- same hair construction;
- same base-garment construction and coverage;
- same wrap/accessory/equipment rules;
- same palette/material family;
- no invented alternate seams, straps, openings, or attachments;
- only viewpoint/motion/occlusion differences that are physically required.

`PIXEL SOURCE PASS`, `COMPONENT INTEGRITY PASS`, and clean alpha do **not** excuse source-fidelity drift.

> **Technically clean pixels + redesigned source detail = SOURCE FAIL.**

---

# 6. Player Paper-Doll Immediate Application

For the current player paper-doll base sheets:

## Male base

The existing male source sheet is authority for the base model. New diagonals must preserve the same character build, hair construction, coverage, wraps, proportions, and base-garment treatment visible in the populated source directions.

## Female base

The existing female source sheet is authority for the base model. New diagonals must preserve the same body proportions, hair construction, wraps, shorts, coverage, and sports-bra construction visible in the populated source directions.

The female sports bra is therefore locked as the **same garment across all directions**. In particular, generated diagonals may not invent a racerback, Y-back, crossed-back, center-back vertical strap, changed strap count, or alternate back topology when the source establishes two shoulder straps feeding into the same horizontal back band.

Any previously generated female diagonal that changes this construction is **invalid as source material** and must be corrected or discarded.

---

# 7. Handoff Rule

A new session or agent must treat the word **source** as a production-authority designation, not merely a filename/location.

Before authoring from a source file:

1. inspect the source closely;
2. enumerate construction details that must remain invariant;
3. distinguish those invariants from viewpoint-dependent details;
4. author only the missing information;
5. run source-fidelity QA before calling the result a source candidate/pass.

Do not rely on a generative model to remember these invariants implicitly. State them explicitly in the active asset contract when working on missing directions or animation frames.

---

## Locked summary

> **IF IT IS SOURCE, ITS VISIBLE DETAILS ARE LOCKED.**  
> **NEW ART COMPLETES MISSING INFORMATION; IT DOES NOT REDESIGN EXISTING SOURCE INFORMATION.**  
> **VIEWPOINT MAY CHANGE. CONSTRUCTION MAY NOT, UNLESS THE USER CHANGES IT.**  
> **TECHNICALLY CLEAN PIXELS THAT DRIFT FROM SOURCE ARE STILL A SOURCE FAILURE.**
