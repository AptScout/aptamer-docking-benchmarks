# Riboswitch Panel

The dataset now includes a six-case RNA-ligand riboswitch panel in addition to the original T6, 4Q9R, and 1FMN cases. These cases broaden aptamer-aware calibration beyond one fluorophore aptamer and one FMN riboswitch.

The current AptScout 10-case reference-pose metrics are summarized in [`macvina_10_case_snapshot.md`](macvina_10_case_snapshot.md).

## Cases

| Case | Ligand/system | Resolution | Expected terms | Intended calibration use |
| --- | --- | ---: | --- | --- |
| `2g9c-purine-riboswitch` | Adenine/purine riboswitch with 3AY | 1.70 A | `baseStacking` hypothesis | High-resolution contact-review case |
| `4rzd-preq1-riboswitch` | PreQ1 riboswitch with PRF analog | 2.75 A | `baseStacking`, `phosphateElectrostatic` | Compact deep-pocket RNA-ligand case |
| `2gdi-tpp-riboswitch` | TPP riboswitch with CCC analog | 2.05 A | `baseStacking`, `phosphateElectrostatic` | TPP analog, two-domain fold |
| `2ygh-sam-riboswitch` | SAM-I riboswitch with SAM | 2.60 A | `baseStacking`, `phosphateElectrostatic` | Larger ligand with stacked adenosine and charged tail |
| `3b4b-glms-riboswitch` | glmS riboswitch/ribozyme with GlcN6P | 2.70 A | `baseStacking`, `phosphateElectrostatic` | Phosphate-bearing cofactor and stacking-specificity check |
| `2hoj-tpp-riboswitch` | TPP riboswitch with native TPP | 2.50 A | `baseStacking`, `phosphateElectrostatic` | Native TPP complement to 2GDI |

Each case currently has:

- `case.json`
- `expected_contacts.json`
- `inputs/conf.txt`
- `inputs/receptor.pdbqt`
- `inputs/ligand.pdbqt`
- `inputs/reference_pose.pdbqt`

The `inputs/` files are intentionally ignored by git, but they exist locally for the current benchmark workspace. The current `reference_pose.pdbqt` files mirror the crystallographic ligand PDBQT and are exposed through `out = reference_pose.pdbqt` so AptScout and AptScout can parse a mode-1 reference pose.

Compatibility note: the local `2ygh-sam-riboswitch` ligand/reference PDBQT records use residue label `SAM A  96` instead of the source-style packed `SAM A1096`, because the latter overflows fixed-column PDBQT residue parsing in AptScout.

## AptScout Snapshots

Claude initially reported the following AptScout processing snapshot:

| Case | Vina | Aptamer | Delta | Time |
| --- | ---: | ---: | ---: | ---: |
| `2g9c-purine-riboswitch` | -6.31 | -6.52 | -0.21 | 7 s |
| `4rzd-preq1-riboswitch` | -7.06 | -7.27 | -0.21 | 11 s |
| `2gdi-tpp-riboswitch` | -5.30 | -5.51 | -0.21 | 5 s |
| `2ygh-sam-riboswitch` | -11.06 | -11.27 | -0.21 | 18 s |
| `3b4b-glms-riboswitch` | -2.76 | -2.97 | -0.21 | 2 s |
| `2hoj-tpp-riboswitch` | -7.51 | -7.72 | -0.21 | 18 s |

The constant `-0.21` aptamer delta was useful as a diagnostic, not as a calibration result. These cases have different ligands, pockets, expected-contact annotations, and intended interaction profiles, so a mature aptamer-aware scoring path should not collapse all six to the same aptamer contribution.

Claude traced that flat delta to placeholder benchmark-path scoring in AptScout and reports that it has been replaced with pose-geometry-based grid scoring. See [`macdock_aptamer_scoring_audit.md`](macdock_aptamer_scoring_audit.md).

Post-fix, the current reported AptScout aptamer-term breakdown is case-specific:

| Case | Ligand-P | Phosphate | Stacking | Notes |
| --- | ---: | ---: | ---: | --- |
| `2g9c-purine-riboswitch` | 0 | -0.13 | 0 | 3AY has no P; N atoms happen near receptor phosphate grid |
| `4rzd-preq1-riboswitch` | 0 | 0 | 0 | Docked pose misses crystal contacts |
| `2gdi-tpp-riboswitch` | -1.70 | 0 | 0 | CCC pyrophosphate contributes ligand-P |
| `2ygh-sam-riboswitch` | 0 | 0 | 0 | Current pose misses contacts |
| `3b4b-glms-riboswitch` | -0.85 | 0 | 0 | GLP has one phosphate |
| `2hoj-tpp-riboswitch` | -1.42 | 0 | 0 | TPP pyrophosphate contributes ligand-P |
 
Most pose-dependent phosphate/stacking terms remain zero at the reported low search depth, so deeper search and pose-level reports are still needed before using the panel for calibration.

## Dataset Interpretation

- Treat the riboswitch panel as structural/contact calibration coverage, not affinity calibration.
- Treat `2g9c-purine-riboswitch` as pending contact review for AptScout/AptScout stacking calibration; its local close contacts do not currently produce a AptScout base-stacking term.
- Treat the 2G9C enrichment set as seed-level: local files contain 7 active models and 198 decoy models, but active/decoy identities and provenance still need review.
- Keep all current affinity fields as `not curated` until experimental sources are reviewed.
- Use the panel to check whether AptScout and AptScout read expected contacts and compute case-specific aptamer terms.
- Use `3b4b-glms-riboswitch` carefully: its notes describe phosphate-bearing GlcN6P and stacking contacts, making it a useful specificity check rather than a simple negative control.
- Do not infer same-ligand pose-decoy performance from this panel yet; no panel case currently declares `decoyPosePath`.

## Review Priorities

1. Confirm that each `expected_contacts.json` label matches source coordinates and the local PDBQT atom naming.
2. Add per-case pose reports from AptScout and AptScout once both tools emit case-specific aptamer term breakdowns.
3. Add same-ligand pose decoys for at least one TPP case and one non-TPP case.
4. Curate experimental affinity sources separately from docking scores.
5. Investigate any scoring run where all riboswitch cases receive the same aptamer delta.
