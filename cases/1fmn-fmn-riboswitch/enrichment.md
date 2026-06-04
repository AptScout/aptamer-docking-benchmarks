# 1FMN FMN Riboswitch Enrichment Set

Tracked metadata for local ignored enrichment files associated with `1fmn-fmn-riboswitch`.

## Set ID

`fmn-enrich-calib`

## Purpose

This set is intended for active-vs-decoy ligand enrichment and contact-specificity calibration. It is not a same-ligand pose-decoy set.

## Local Files

All paths are relative to `cases/1fmn-fmn-riboswitch/`.

| Path | Role | Models | Atom records | Ligand/residue labels |
| --- | --- | ---: | ---: | --- |
| `enrich_calib/receptor.pdbqt` | RNA receptor | 1 | 2340 | chains X/Y RNA receptor |
| `enrich_calib/crystal.pdbqt` | crystallographic active pose | 1 | 31 | `FMN Y 200` |
| `enrich_calib/actives.pdbqt` | active ligand set | 1 | 31 | `FMN Y 200` |
| `enrich_calib/decoys.pdbqt` | ligand decoy set | 60 | 1895 | `UNL 1` |

## Curation Notes

- `crystal.pdbqt`, `actives.pdbqt`, and `inputs/ligand_fmn.pdbqt` share the FMN atom layout used by the reference pose.
- `decoys.pdbqt` contains different `UNL` ligands. These should be evaluated as ligand-set decoys, not as alternate FMN poses.
- Do not use this set for RMSD-to-reference pose metrics unless a future enrichment reader first separates active FMN poses from non-FMN ligand decoys.
- The active and decoy identities remain seed-level metadata until manually traced to the source generation protocol.

## Expected Use

Use this enrichment set to test whether aptamer-aware scoring ranks/contact-matches FMN-like active signal ahead of unrelated ligand decoys in the 3F4E riboswitch pocket.
