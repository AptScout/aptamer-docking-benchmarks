# T6 Thrombin Vina Output Modes

Tracked metadata for local ignored QuickVina output files associated with `t6-thrombin-vina`.

## Purpose

This case provides a protein-DNA aptamer reference from an existing AutoDock/QuickVina-style run. The output models are multiple same-ligand docking modes, not an explicit hard-decoy set.

## Local Files

All paths are relative to `cases/t6-thrombin-vina/`.

| Path | Role | Models | Atom records | Notes |
| --- | --- | ---: | ---: | --- |
| `inputs/PROTEIN.pdbqt` | thrombin receptor | 1 | 3240 | chain `I` protein receptor |
| `inputs/T6_model1.pdbqt` | T6 aptamer input ligand | 1 | 770 | DNA aptamer chain `A` |
| `inputs/outT6.pdbqt` | QuickVina output modes | 4 | 3080 | 4 same-aptamer output modes |
| `inputs/logT6.txt` | QuickVina log | n/a | n/a | 2426 bytes |

## QuickVina Log Modes

From `inputs/logT6.txt`.

| Mode | Affinity kcal/mol | RMSD lower bound | RMSD upper bound |
| ---: | ---: | ---: | ---: |
| 1 | -17.2 | 0.000 | 0.000 |
| 2 | -15.6 | 7.324 | 26.554 |
| 3 | -15.1 | 2.967 | 4.391 |
| 4 | -14.4 | 7.387 | 30.056 |

## Current MacVina Diagnostics

Generated from `derived/macvina/shared-pose-report.csv`.

| Pose | Role | Rank | Aptamer score | RMSD to reference | Expected-contact hit | Clash count |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `mode:1` | reference | 1 | -17.651 | 0.000 | 1.000 | 15 |
| `mode:3` | Vina output | 2 | -16.695 | 4.384 | 0.750 | 14 |
| `mode:2` | Vina output | 3 | -15.783 | 26.606 | 0.500 | 12 |
| `mode:4` | Vina output | 4 | -13.756 | 30.172 | 0.500 | 12 |

## Curation Notes

- Mode 1 is the reference pose and matches the best QuickVina affinity.
- Mode 3 is geometrically closer to the reference than modes 2 and 4 by MacVina RMSD, despite its worse QuickVina affinity.
- This case is useful for preserving T6 compatibility and phosphate-electrostatic seed contacts.
- Expected contacts remain seed-level and should be reviewed before promoting this case beyond `seed`.
