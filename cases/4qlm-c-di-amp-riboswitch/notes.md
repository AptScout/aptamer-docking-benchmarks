# ydaO c-di-AMP Riboswitch

Seed benchmark case `4qlm-c-di-amp-riboswitch`.

## Source

- RCSB PDB: `4QLM`
- HARIBOSS candidate: RNA-small-molecule complex
- Ligand: `2BA` c-di-AMP
- Method/resolution: X-ray diffraction, 2.721 A

## Prep TODO

- Extract chain `A` receptor and ligand `2BA`.
- Decide whether `SO4` and `MG` should remain in the receptor.
- Generate local PDBQT inputs and a self-contained config.
- Curate expected contacts for both nucleotide-like bases and phosphate/ribose groups.
