# 4Q9R 2ZY Pose-Decoy Set

Tracked metadata for local ignored same-ligand pose decoys associated with `4q9r-spinach-2zy`.

## Purpose

This set is intended for reference-vs-decoy pose ranking, contact-specificity, clash, and RMSD-aware calibration. Unlike the 1FMN enrichment set, these decoys are alternate poses of the same ligand rather than different ligands.

## Local Files

All paths are relative to `cases/4q9r-spinach-2zy/`.

| Path | Role | Models | Atom records | Ligand/residue labels |
| --- | --- | ---: | ---: | --- |
| `inputs/receptor.pdbqt` | RNA receptor | 1 | 1787 | RNA chain `R` plus retained ion records |
| `inputs/ligand_2zy.pdbqt` | input ligand | 1 | 22 | `2ZY R 102` |
| `inputs/reference_pose.pdbqt` | crystallographic reference pose | 1 | 22 | `2ZY R 102` |
| `inputs/decoys.pdbqt` | same-ligand pose decoys | 10 | 220 | `2ZY R 102` |

## Current MacVina Diagnostics

Generated from `derived/macvina/shared-pose-report.csv`.

| Pose | Role | Rank | Score | RMSD to reference | Expected-contact hit | Clash count |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `mode:1` | reference | 1 | -10.535 | 0.000 | 1.000 | 54 |
| `decoy:6` | decoy | 2 | 16.169 | 8.224 | 0.750 | 78 |
| `decoy:2` | decoy | 3 | 17.290 | 1.400 | 0.000 | 85 |
| `decoy:1` | decoy | 4 | 27.025 | 1.400 | 1.000 | 84 |
| `decoy:3` | decoy | 5 | 32.136 | 1.000 | 0.250 | 97 |
| `decoy:7` | decoy | 6 | 78.135 | 7.091 | 0.250 | 124 |
| `decoy:4` | decoy | 7 | 101.611 | 2.933 | 0.500 | 130 |
| `decoy:9` | decoy | 8 | 143.910 | 8.000 | 0.250 | 97 |
| `decoy:8` | decoy | 9 | 144.530 | 2.000 | 0.250 | 141 |
| `decoy:5` | decoy | 10 | 269.926 | 5.411 | 0.250 | 189 |
| `decoy:10` | decoy | 11 | 271.285 | 8.000 | 0.000 | 188 |

## Curation Notes

- The reference pose currently ranks first against the 10 local decoys.
- `decoy:1` preserves the expected contact hit fraction but ranks below the reference because of worse geometry and clashes.
- `decoy:6` is the best-scoring decoy and keeps partial contact signal; this is useful for calibrating contact specificity without over-rewarding any stacking-like contact.
- This case is suitable for pose-decoy calibration, but expected contacts remain seed-level until manually reviewed against the 4Q9R structure/literature.
