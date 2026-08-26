# Kairo — Package 07 Progress Update

## Active source gates

### Clothing

- 40 direction-specific clothing source candidates isolated across inner top, haori, trousers, footwear and sash.
- Active body/clothing registration QA: **v4**.
- Body and dressed benchmarks are on the shared **480×640** lattice with body center `x = 240` and foot-contact `y = 560`.
- Runtime reduction remains blocked until direction-by-direction seam correction reproduces the approved dressed Kairo benchmark.

### Hair

The approved eight-direction hair sheet has been isolated direction-by-direction.

- v1/v2 were rejected because lower-row crops retained detached label/border fragments.
- active hair isolation QA: **v3**.
- v3 keeps the primary hair silhouette and rejects shallow detached components above it.
- hair is registered to the same crown/body lattice for all eight directions.
- a true hairless body master is still required before interchangeable hair can be promoted to runtime.

### Equipment and accessories

The equipment sheet has been isolated into direction-specific source candidates for:

- katana in hand
- scabbard at waist
- scabbard cord / belt knot
- hanging charm tag
- necklace / charm
- pouch
- gourd flask
- shoulder tie / cloth strip
- wrist wraps
- utility belt trinket

v1/v2 were rejected because they retained direction labels, rule lines or neighboring-item fragments. The active equipment isolation QA is **v3**, which keeps the primary object silhouette and immediately overlapping legitimate components while rejecting detached labels/rules/fragments.

Known source coverage gaps remain intentionally unresolved:

- katana in hand — NW missing
- scabbard at waist — NW missing
- scabbard cord / belt knot — NW missing
- shoulder tie / cloth strip — NW missing

These missing directions will be authored from the approved Kairo visual language rather than mirrored automatically because facing-dependent asymmetry matters for weapon and accessory routing.

## Anchor policy

World props may use host-specific center/bottom/top mount justification. Character paper-doll layers do not. Every Kairo body, clothing, hair, face, equipment and accessory layer must inherit the same anatomical body lattice.

## Current gate

No character checklist item is complete. Package 07 remains a **source-registration candidate** until clothing seams, hairless-body separation, equipment routing and the missing NW source directions are resolved before 48×64 runtime derivation.
