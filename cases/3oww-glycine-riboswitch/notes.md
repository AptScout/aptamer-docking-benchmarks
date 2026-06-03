# Glycine Riboswitch Bound to Glycine

Seed benchmark case `3oww-glycine-riboswitch`.

## Source

- RCSB PDB: `3OWW`
- HARIBOSS candidate: RNA-small-molecule complex
- Ligand: `GLY` glycine
- Method/resolution: X-ray diffraction, 2.802 A

## Prep TODO

- Choose a single receptor/ligand instance from chains `A` or `B`, or split into companion cases.
- Preserve or document `MG` ions if they stabilize the pocket.
- Generate local PDBQT inputs and `inputs/conf.txt`.
- Review cooperative/tandem-aptamer caveats before using enrichment or pose reproduction metrics.
