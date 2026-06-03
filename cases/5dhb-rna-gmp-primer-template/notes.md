# RNA Primer-Template Bound to GMP

Seed benchmark case `5dhb-rna-gmp-primer-template`.

## Source

- RCSB PDB: `5DHB`
- HARIBOSS example: RNA primer-template bound to ligand `5GP`
- Ligand: `5GP` guanosine-5'-monophosphate
- Method/resolution: X-ray diffraction, 1.8 A

## Prep TODO

- Choose one of the ligand-bearing chains `A`-`D` for the initial case.
- Generate local PDBQT inputs and `inputs/conf.txt`.
- Curate nucleotide-like base-stacking and phosphate-contact expectations after atom-label inspection.
- Decide whether this belongs in RNA-ligand calibration or in a separate RNA-replication/template subgroup.
