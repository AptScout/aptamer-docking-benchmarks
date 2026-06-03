# c-di-GMP Riboswitch

Seed benchmark case `3irw-c-di-gmp-riboswitch`.

## Source

- RCSB PDB: `3IRW`
- HARIBOSS candidate: RNA-small-molecule complex
- Ligand: `C2E` c-di-GMP
- Method/resolution: X-ray diffraction, 2.7 A

## Prep TODO

- Extract chain `R` receptor and ligand `C2E`.
- Decide ion policy for crystallographic `MG` and `IRI`.
- Generate local PDBQT inputs and a self-contained Vina config.
- Review base-stacking and phosphate-contact labels before using for calibration.
