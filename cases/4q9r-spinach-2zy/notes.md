# Spinach RNA aptamer bound to 2ZY fluorophore analog

Seed benchmark case `4q9r-spinach-2zy`.

## Source

RCSB PDB 4Q9R / NAKB 4Q9R; Spinach RNA aptamer bound to ligand 2ZY in antibody-assisted crystal structure.

RCSB describes this entry as the crystal structure of an RNA aptamer bound to a trifluoroethyl ligand analog in complex with Fab. The experimental method is X-ray diffraction at 3.12 Angstrom resolution. The RCSB entry notes that Spinach RNA binds a GFP-like fluorophore and that the fluorophore binds in a planar conformation with extensive aromatic stacking and hydrogen-bond interactions with RNA.

## Inputs

Configured path:

```text
inputs/4q9r-conf.txt
```

Place local raw inputs under `inputs/` if needed. That directory is ignored by git.

## Curation Notes

- Extract RNA aptamer chain and ligand `2ZY` from 4Q9R.
- Decide whether to remove Fab chains before docking/calibration.
- Local ignored inputs have been generated from RCSB 4Q9R: RNA chain `R` plus K ion as receptor, ligand `2ZY` as ligand/reference pose, Fab chains excluded.
- Current MacVina reference-pose interaction report detects `baseStacking R:102:C16#4 -> R:54:C8#1138`.
- Expected contacts are seeded as receptor residue `R:54`, ligand atom `C16_4`, interaction kind `baseStacking`.
- Local ignored `inputs/decoys.pdbqt` contains 10 same-ligand 2ZY pose decoys; see `decoys.md` for pose-decoy counts and current diagnostics.
- Add affinity source if available; current case is structural/contact calibration only.
