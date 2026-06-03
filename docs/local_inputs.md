# Local Input Inventory

Large molecular files and generated outputs are intentionally ignored by git. This page records the local input paths currently expected by the tracked metadata so another MacVina or MacDock workspace can restore the same benchmark layout.

## Ignored Path Policy

The repository keeps metadata, expected contacts, and notes in git. These paths stay local:

- `raw/`
- `derived/`
- `cases/*/inputs/`
- `cases/*/derived/`
- structure/docking files such as `.pdb`, `.pdbqt`, `.cif`, `.sdf`, `.mol2`
- generated `.csv`, `.tsv`, and `.log` files

## Required Local Paths By Case

### `t6-thrombin-vina`

Tracked metadata references `inputs/confainaT6.txt`. That config resolves the legacy Vina input/output files in the same directory.

| Path | Role |
| --- | --- |
| `cases/t6-thrombin-vina/inputs/confainaT6.txt` | Self-contained Vina config |
| `cases/t6-thrombin-vina/inputs/PROTEIN.pdbqt` | Receptor |
| `cases/t6-thrombin-vina/inputs/T6_model1.pdbqt` | Ligand/reference aptamer pose |
| `cases/t6-thrombin-vina/inputs/outT6.pdbqt` | QuickVina output poses |
| `cases/t6-thrombin-vina/inputs/logT6.txt` | QuickVina log |

The `-17.2 kcal/mol` value is from `logT6.txt`/`outT6.pdbqt` and is a docking reference score, not experimental affinity.

### `4q9r-spinach-2zy`

Tracked metadata references `inputs/4q9r-conf.txt` and `inputs/decoys.pdbqt`.

| Path | Role |
| --- | --- |
| `cases/4q9r-spinach-2zy/inputs/4q9r-conf.txt` | Vina config |
| `cases/4q9r-spinach-2zy/inputs/receptor.pdbqt` | RNA receptor used for docking/calibration |
| `cases/4q9r-spinach-2zy/inputs/ligand.pdbqt` | Ligand path referenced by the config |
| `cases/4q9r-spinach-2zy/inputs/reference_pose.pdbqt` | Reference output pose |
| `cases/4q9r-spinach-2zy/inputs/decoys.pdbqt` | Same-ligand 2ZY pose decoys |
| `cases/4q9r-spinach-2zy/inputs/4q9r.pdb` | Source structure |
| `cases/4q9r-spinach-2zy/inputs/receptor_rna.pdb` | Extracted RNA receptor precursor |
| `cases/4q9r-spinach-2zy/inputs/ligand_2zy.pdb` | Extracted 2ZY ligand precursor |
| `cases/4q9r-spinach-2zy/inputs/ligand_2zy.pdbqt` | Explicit 2ZY ligand PDBQT |

`decoys.pdbqt` is a true same-ligand pose-decoy file and can support RMSD-aware pose ranking.

### `1fmn-fmn-riboswitch`

Tracked metadata references `inputs/1fmn-conf.txt` and the enrichment set under `enrich_calib/`.

| Path | Role |
| --- | --- |
| `cases/1fmn-fmn-riboswitch/inputs/1fmn-conf.txt` | Vina config |
| `cases/1fmn-fmn-riboswitch/inputs/receptor.pdbqt` | RNA receptor used for docking/calibration |
| `cases/1fmn-fmn-riboswitch/inputs/ligand_fmn.pdbqt` | FMN ligand seed pose |
| `cases/1fmn-fmn-riboswitch/inputs/reference_pose.pdbqt` | Reference output pose |
| `cases/1fmn-fmn-riboswitch/inputs/3f4e.pdb` | Source structure |
| `cases/1fmn-fmn-riboswitch/inputs/1fmn.pdb` | Local source/working structure |
| `cases/1fmn-fmn-riboswitch/inputs/receptor_rna.pdb` | Extracted RNA receptor precursor |
| `cases/1fmn-fmn-riboswitch/inputs/ligand_fmn.pdb` | Extracted FMN ligand precursor |
| `cases/1fmn-fmn-riboswitch/enrich_calib/receptor.pdbqt` | Enrichment receptor |
| `cases/1fmn-fmn-riboswitch/enrich_calib/crystal.pdbqt` | Crystal FMN pose |
| `cases/1fmn-fmn-riboswitch/enrich_calib/actives.pdbqt` | Active ligand set, 1 FMN model |
| `cases/1fmn-fmn-riboswitch/enrich_calib/decoys.pdbqt` | Decoy ligand set, 60 non-FMN models |

The enrichment decoys are different ligands, not alternate FMN poses. Keep them separate from same-ligand pose decoys and RMSD-to-reference metrics.

### `1fmn-fmn-riboswitch-mg`

Tracked metadata references `inputs/1fmn-mg-conf.txt`.

| Path | Role |
| --- | --- |
| `cases/1fmn-fmn-riboswitch-mg/inputs/1fmn-mg-conf.txt` | Vina config |
| `cases/1fmn-fmn-riboswitch-mg/inputs/receptor_mg.pdbqt` | RNA receptor with retained Mg `X:304` |
| `cases/1fmn-fmn-riboswitch-mg/inputs/ligand_fmn.pdbqt` | FMN ligand seed pose |
| `cases/1fmn-fmn-riboswitch-mg/inputs/reference_pose.pdbqt` | Reference output pose |
| `cases/1fmn-fmn-riboswitch-mg/inputs/3f4e.pdb` | Source structure |

This case should be restored alongside the plain 1FMN case so tools can compare scoring with and without the crystallographic Mg site.

### Riboswitch Panel

The six riboswitch-panel cases all use the same minimal ignored input layout:

```text
cases/<case-id>/inputs/conf.txt
cases/<case-id>/inputs/receptor.pdbqt
cases/<case-id>/inputs/ligand.pdbqt
cases/<case-id>/inputs/reference_pose.pdbqt
```

Current panel case IDs:

| Case | Config path | Receptor path | Ligand path | Reference pose path |
| --- | --- | --- | --- | --- |
| `2g9c-purine-riboswitch` | `inputs/conf.txt` | `inputs/receptor.pdbqt` | `inputs/ligand.pdbqt` | `inputs/reference_pose.pdbqt` |
| `4rzd-preq1-riboswitch` | `inputs/conf.txt` | `inputs/receptor.pdbqt` | `inputs/ligand.pdbqt` | `inputs/reference_pose.pdbqt` |
| `2gdi-tpp-riboswitch` | `inputs/conf.txt` | `inputs/receptor.pdbqt` | `inputs/ligand.pdbqt` | `inputs/reference_pose.pdbqt` |
| `2ygh-sam-riboswitch` | `inputs/conf.txt` | `inputs/receptor.pdbqt` | `inputs/ligand.pdbqt` | `inputs/reference_pose.pdbqt` |
| `3b4b-glms-riboswitch` | `inputs/conf.txt` | `inputs/receptor.pdbqt` | `inputs/ligand.pdbqt` | `inputs/reference_pose.pdbqt` |
| `2hoj-tpp-riboswitch` | `inputs/conf.txt` | `inputs/receptor.pdbqt` | `inputs/ligand.pdbqt` | `inputs/reference_pose.pdbqt` |

No riboswitch-panel case currently declares a same-ligand `decoyPosePath`.

The local `2ygh-sam-riboswitch` ligand and reference-pose PDBQT files are normalized to residue label `SAM A  96` for fixed-column PDBQT compatibility.

`2g9c-purine-riboswitch` also has a seed ligand-enrichment set under `enrich/`:

| Path | Role |
| --- | --- |
| `cases/2g9c-purine-riboswitch/enrich/receptor.pdbqt` | Enrichment receptor |
| `cases/2g9c-purine-riboswitch/enrich/crystal.pdbqt` | Crystal 3AY pose |
| `cases/2g9c-purine-riboswitch/enrich/actives.pdbqt` | Active ligand set, 7 models |
| `cases/2g9c-purine-riboswitch/enrich/decoys.pdbqt` | Decoy ligand set, 198 models |

### HARIBOSS Seed Expansion

`6c64-mango-ii-ekm` has been promoted into the runnable manifest. `5bjp-corn-dfho` has also been promoted. Their local ignored input layouts are:

#### `6c64-mango-ii-ekm`

| Path | Role |
| --- | --- |
| `cases/6c64-mango-ii-ekm/inputs/conf.txt` | Vina config |
| `cases/6c64-mango-ii-ekm/inputs/receptor.pdbqt` | RNA chain A receptor |
| `cases/6c64-mango-ii-ekm/inputs/ligand.pdbqt` | EKM chain A ligand |
| `cases/6c64-mango-ii-ekm/inputs/reference_pose.pdbqt` | Crystal-derived EKM reference pose |
| `cases/6c64-mango-ii-ekm/inputs/6c64.pdb` | Downloaded RCSB source structure |
| `cases/6c64-mango-ii-ekm/inputs/receptor_rna_chain_a.pdb` | Extracted RNA receptor precursor |
| `cases/6c64-mango-ii-ekm/inputs/ligand_ekm_chain_a.pdb` | Extracted EKM ligand precursor |

#### `5bjp-corn-dfho`

| Path | Role |
| --- | --- |
| `cases/5bjp-corn-dfho/inputs/conf.txt` | Vina config |
| `cases/5bjp-corn-dfho/inputs/receptor.pdbqt` | RNA chain Y receptor |
| `cases/5bjp-corn-dfho/inputs/ligand.pdbqt` | 747 DFHO chain Y ligand |
| `cases/5bjp-corn-dfho/inputs/reference_pose.pdbqt` | Crystal-derived 747 reference pose |
| `cases/5bjp-corn-dfho/inputs/5bjp.pdb` | Downloaded RCSB source structure |
| `cases/5bjp-corn-dfho/inputs/receptor_rna_chain_y.pdb` | Extracted RNA receptor precursor |
| `cases/5bjp-corn-dfho/inputs/ligand_747_chain_y.pdb` | Extracted 747 ligand precursor |

The HARIBOSS cases `3sd3-thf-riboswitch`, `5dhb-gmp-primer-template`, and `6wzs-ztp-riboswitch` also use `inputs/reference_pose.pdbqt` as the crystal-derived output pose referenced by `inputs/conf.txt`.

The remaining HARIBOSS seed cases are tracked as metadata/prep targets only and are not yet listed in the main runnable manifest. Each currently references the same minimal future input layout:

```text
cases/<hariboss-case-id>/inputs/conf.txt
cases/<hariboss-case-id>/inputs/receptor.pdbqt
cases/<hariboss-case-id>/inputs/ligand.pdbqt
cases/<hariboss-case-id>/inputs/reference_pose.pdbqt
```

Current HARIBOSS seed case IDs:

| Case | Source structure | Ligand |
| --- | --- | --- |
| `4gxy-cobalamin-riboswitch` | `4GXY` | `B1Z` adenosylcobalamin |
| `3irw-c-di-gmp-riboswitch` | `3IRW` | `C2E` c-di-GMP |
| `3d0u-lysine-riboswitch` | `3D0U` | `LYS` lysine |
| `4enc-fluoride-riboswitch` | `4ENC` | `F` fluoride |
| `3oww-glycine-riboswitch` | `3OWW` | `GLY` glycine |
| `4qlm-c-di-amp-riboswitch` | `4QLM` | `2BA` c-di-AMP |
| `6wzs-ztp-riboswitch` | `6WZS` | `UG4` |
| `5dhb-rna-gmp-primer-template` | `5DHB` | `5GP` GMP |
| `3sd3-thf-riboswitch` | `3SD3` | `FFO` folate analog |

Missing `inputs/conf.txt` warnings are expected for these seed cases until local PDBQT preparation is done.

Use [`hariboss_promotion_sop.md`](hariboss_promotion_sop.md) before adding any of these cases to `manifest.json`.

## Restoration Notes

- Restore files at the exact case-relative paths above before running MacVina or other compatible benchmark consumers over the shared manifest.
- Treat `case.json` paths as the source of truth when duplicate local working directories exist.
- Keep `case.json` paths case-relative and self-contained. Do not use absolute paths or `..` escapes into a local tool checkout.
- Keep generated tool outputs under `derived/<tool>/` or `cases/<case-id>/derived/<tool>/`.
- Re-run `python3 scripts/validate_manifest.py` after metadata edits. On machines with the local ignored inputs restored, also run the relevant tool-level validate-only command.
