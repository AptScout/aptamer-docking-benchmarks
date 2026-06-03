# Fluoride Riboswitch Bound to Fluoride

Seed benchmark case `4enc-fluoride-riboswitch`.

## Source

- RCSB PDB: `4ENC`
- HARIBOSS candidate: RNA-small-molecule/ion complex
- Ligand: `F` fluoride
- Method/resolution: X-ray diffraction, 2.272 A

## Prep TODO

- Decide whether this should be a normal docking case, an ion-placement case, or a metal/ion-coordination special case.
- Preserve receptor `K`/`MG` ions if they define the binding site.
- Generate local inputs only after the ion policy is decided.
- Contact review should focus on ion coordination geometry rather than ordinary ligand-heavy-atom contacts.
