# Animation development rules

These are the standing rules for every character animation. Christopher set them; the date of each ruling is given in brackets.

## Every fighter's own look (2026-11-03)

Anything that traces or copies the fighter must follow the fighter as it is actually dressed: its hairstyle, helmet, armour, shoulders and weapons. It must never follow the base body and gi.

- **Auras follow the outline of the hair (19:28).** Auras are never baked into `fx.png`. The clip's spec json and `animation.json` carry an `aura` record (`widths` per frame, `colors`), and the testbed grows it at runtime from the fighter's own composited silhouette. `tools/grstrikes.aura` does this by default; `AURA_BAKE=1` brings back the old baking for comparison only. Clips baked before this rule are cleaned with `tools/unbake_aura.py`.
- **Baked silhouette fx root outside every look.** Spiked eruptions, rays and glows (`burst`, `flare`, `rays`, `gather`, `nova` in `tools/astro.py`) start outside the union of every hair, helmet and armour layer (`OUTFIT_LAYERS`), so they never paint over a hairstyle.
- **Copies of the caster wear what the caster wears (19:22).** Clones, decoys and illusory copies are never baked. The spec carries `clones` (copies on the caster's own clip) or `legion` (copies round a target), and the testbed draws them from the caster's composited sprite.
- **Preview against other looks.** Before posting a candidate that has an aura or copies, check it with `astro_scene.py --outfit <clothing>,<shoulders>,<hair>,<eyes>`, which draws runtime auras and copies the way the testbed does.

## Targets react on the impact frame (2026-11-04)

Christopher made this a standing rule on 2026-11-04 16:51.

- **No reaction before the hit lands.** A target holds its plain guard until the caster's impact frame. That impact frame is the clip's active frame, or the frame a projectile, stream or zone actually reaches the target. The target state's frame 0 is the moment of impact, never anticipation: no flinch, no fx on the target, nothing closing in on it beforehand.
- **Fx that travels to the target stays with the caster until impact.** Up to the impact frame it belongs to the caster's clip or its spec record (projectile, stream, zone). It moves onto the target state only from the impact frame on.
- **Older clips need checking.** Clips approved before this rule have not been audited against it; review them when asked.

## Carried rules

- One state per ability. Every clip starts from and returns to the approved boxing guard.
- Rotations are quarter turns only. Fighters face their target automatically.
- Hands and wrists over the body get a 1 px outline.
- S/N is drafted against E/W using projection lines, which are never shown in candidates.
- Effects use the element's colours. Air is white and pale silver with a light touch of the System Crash green (#39e75f) so it reads on every terrain (2026-11-03).
- Every genjutsu marks its target with `genjutsuAfflicted`, recoloured for the element.
- Candidates are posted as attached file cards, each under a new versioned filename.
