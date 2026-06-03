# Cobalamin Riboswitch Bound to Adenosylcobalamin

Seed benchmark case `4gxy-cobalamin-riboswitch`.

## Source

- RCSB PDB: `4GXY`
- HARIBOSS candidate: RNA-small-molecule complex
- Ligand: `B1Z` adenosylcobalamin
- Method/resolution: X-ray diffraction, 3.05 A

## Prep TODO

- Extract RNA receptor and adenosylcobalamin ligand into local `inputs/`.
- Decide whether crystallographic `MG` and `IRI` ions should be retained, ignored, or split into companion metal cases.
- Generate `inputs/receptor.pdbqt`, `inputs/ligand.pdbqt`, `inputs/reference.pdbqt`, and `inputs/conf.txt`.
- Review expected contacts against local coordinates and the source paper before promotion beyond `seed`.
