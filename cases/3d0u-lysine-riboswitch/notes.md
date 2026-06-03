# Lysine Riboswitch Bound to Lysine

Seed benchmark case `3d0u-lysine-riboswitch`.

## Source

- RCSB PDB: `3D0U`
- HARIBOSS candidate: RNA-small-molecule complex
- Ligand: `LYS` lysine
- Method/resolution: X-ray diffraction, 2.8 A

## Prep TODO

- Extract chain `A` receptor and ligand `LYS`.
- Confirm protonation/charge handling for lysine before PDBQT generation.
- Generate local PDBQT inputs and `inputs/conf.txt`.
- Review expected hydrogen-bond and electrostatic contacts before promotion beyond `seed`.
