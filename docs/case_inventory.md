# Case Inventory

This inventory summarizes the current benchmark cases and the calibration signal each one provides. Molecular inputs and generated reports remain local ignored artifacts; this page records the tracked interpretation of those files.

Expected-contact provenance is tracked separately in [`contact_review.md`](contact_review.md).
Affinity provenance is tracked separately in [`affinity_status.md`](affinity_status.md).
The expanded RNA-ligand riboswitch panel is described in [`riboswitch_panel.md`](riboswitch_panel.md).
MacDock's riboswitch-panel scoring audit is tracked in [`macdock_aptamer_scoring_audit.md`](macdock_aptamer_scoring_audit.md).

## Summary

| Case | System | Status | Primary calibration signal | Pose decoys | Enrichment set | Expected-contact terms |
| --- | --- | --- | --- | --- | --- | --- |
| `t6-thrombin-vina` | DNA aptamer-protein | `seed` | QuickVina reference/output agreement for a protein-bound aptamer | Vina output modes only | No | `phosphateElectrostatic` |
| `4q9r-spinach-2zy` | RNA-ligand | `seed` | Same-ligand pose discrimination for RNA base stacking | Yes, 10 local 2ZY pose decoys | No | `baseStacking` |
| `1fmn-fmn-riboswitch` | RNA-ligand | `parsed` | FMN base-stacking plus phosphate-contact specificity | No same-ligand pose decoys | Yes, 1 FMN active and 60 non-FMN decoys | `baseStacking`, `phosphateElectrostatic` |
| `1fmn-fmn-riboswitch-mg` | RNA-ligand | `parsed` | Crystallographic Mg-to-FMN phosphate contact | No | No | `metalCoordination` |
| `2g9c-purine-riboswitch` | RNA-ligand | `parsed` | High-resolution purine-riboswitch contact-review case | No | Yes, seed | `baseStacking` hypothesis |
| `4rzd-preq1-riboswitch` | RNA-ligand | `contact_reviewed` | Compact preQ1 pocket with stacking/phosphate contacts | No | No | `baseStacking`, `phosphateElectrostatic` |
| `2gdi-tpp-riboswitch` | RNA-ligand | `contact_reviewed` | TPP analog with stacked aminopyrimidine and phosphate tail | No | No | `baseStacking`, `phosphateElectrostatic` |
| `2ygh-sam-riboswitch` | RNA-ligand | `contact_reviewed` | SAM adenosine stacking plus charged-tail contacts | No | No | `baseStacking`, `phosphateElectrostatic` |
| `3b4b-glms-riboswitch` | RNA-ligand | `contact_reviewed` | GlcN6P phosphate-bearing cofactor specificity case | No | No | `baseStacking`, `phosphateElectrostatic` |
| `2hoj-tpp-riboswitch` | RNA-ligand | `contact_reviewed` | Native TPP complement to 2GDI | No | No | `baseStacking`, `phosphateElectrostatic` |
| `6c64-mango-ii-ekm` | RNA-ligand | `parsed` | Mango-II fluorogenic aptamer aromatic stacking case | No | No | `baseStacking` hypothesis |
| `5bjp-corn-dfho` | RNA-ligand | `parsed` | Corn fluorogenic aptamer DFHO aromatic stacking case | No | No | `baseStacking` hypothesis |
| HARIBOSS seed expansion | RNA-ligand | `seed` | Broaden future RNA-small-molecule structure coverage | No | No | Not curated; outside main manifest |

## Case Notes

### `t6-thrombin-vina`

T6 is the legacy AutoDock/QuickVina-style anchor case for the shared benchmark format. Its config is now self-contained under `cases/t6-thrombin-vina/inputs/confainaT6.txt`, avoiding dependencies on a local MacVina checkout.

Use this case to check that tools can load aptamer-protein PDBQT inputs, parse Vina output modes, and reproduce a stable reference/output ranking. The current expected contact is intentionally permissive and should be manually reviewed before being treated as scientific ground truth.

Tracked detail: [`../cases/t6-thrombin-vina/vina_outputs.md`](../cases/t6-thrombin-vina/vina_outputs.md).

### `4q9r-spinach-2zy`

4Q9R is the strongest current pose-ranking case for aptamer-aware calibration. It has a same-ligand local decoy file, `inputs/decoys.pdbqt`, with 10 alternate 2ZY poses. MacVina currently ranks the reference pose first against those decoys.

Use this case for base-stacking weight calibration, reference-vs-decoy margin checks, clash-aware pose diagnostics, and RMSD-aware same-ligand reports. One decoy shows stronger stacking than the reference but loses due to clash/geometry penalties, so it is useful for balancing attractive stacking rewards against physical penalties.

Tracked detail: [`../cases/4q9r-spinach-2zy/decoys.md`](../cases/4q9r-spinach-2zy/decoys.md).

### `1fmn-fmn-riboswitch`

The plain FMN case is a parsed 3F4E-derived RNA-ligand benchmark without the crystallographic Mg companion site. It exercises both base-stacking and phosphate-electrostatic expected contacts. The local enrichment set contains one FMN active/crystal pose and 60 non-FMN decoy ligands.

Use this case for contact specificity and ligand-enrichment experiments. Do not use its enrichment decoys as same-ligand pose decoys or RMSD-to-reference pose examples, because the decoys are different ligands.

Tracked detail: [`../cases/1fmn-fmn-riboswitch/enrichment.md`](../cases/1fmn-fmn-riboswitch/enrichment.md).

### `1fmn-fmn-riboswitch-mg`

The Mg companion case keeps crystallographic Mg `X:304`, which sits 2.54 A from FMN `O1P` in 3F4E. This case is intended to exercise the metal-coordination scoring term against a real receptor-metal/ligand-phosphate geometry.

Use this case as a metal-term smoke test and as a comparison point against the plain FMN case. It does not yet provide metal-site decoys, so it should not be the only source of metal-weight calibration signal.

Tracked detail: [`../cases/1fmn-fmn-riboswitch-mg/metal_coordination.md`](../cases/1fmn-fmn-riboswitch-mg/metal_coordination.md).

### Riboswitch Panel

The six-case riboswitch panel adds purine, preQ1, TPP, SAM, and glmS RNA-ligand systems. These cases are useful for checking whether aptamer-aware scoring produces case-specific contributions across varied ligands and RNA pockets.

`2g9c-purine-riboswitch` is currently downgraded to `parsed`: local atom contacts are present, but MacVina reports zero base-stacking contribution and two previous ligand atom labels were not present in the local 3AY PDBQT. See [`../cases/2g9c-purine-riboswitch/contact_review.md`](../cases/2g9c-purine-riboswitch/contact_review.md).

Its local enrichment set is also seed-level: 7 active models and 198 decoy models are present, but ligand identities and generation provenance still need review. See [`../cases/2g9c-purine-riboswitch/enrichment.md`](../cases/2g9c-purine-riboswitch/enrichment.md).

### `5bjp-corn-dfho`

5BJP is the second fluorogenic aptamer case promoted from the HARIBOSS seed queue, following 6C64. It features the Corn RNA aptamer bound to DFHO (747), a heteroaromatic dye-like ligand similar in spirit to Mango-II.

Chain Y of the dimeric 5BJP structure contains the only DFHO molecule. All crystallographic ions (IR, K, MG, DMS) were removed for this first parsed version. The ligand has two aromatic regions: a fluorophenyl ring and an imidazolone-oxime conjugated system. Six RNA residues (A:11, G:12, G:15, G:22, A:24, G:25) have atoms within 4.0 A of the ligand, with G:22 forming the tightest contact (2.90 A N1-O14).

Use this case alongside 6C64 for fluorogenic aptamer base-stacking calibration. Contacts are hypothesis-level; source-paper review is needed before promoting beyond `parsed`.

### Riboswitch Panel

Claude's initial MacDock snapshot reported the same `-0.21` aptamer delta for all six panel cases. That exposed placeholder benchmark-path scoring and has been recorded as a diagnostic. Claude reports that MacDock now uses pose-geometry-based aptamer grids, but deeper searches and per-term reports are still needed before calibration.

Tracked detail: [`riboswitch_panel.md`](riboswitch_panel.md).

### HARIBOSS Seed Expansion

The HARIBOSS seed expansion adds 11 tracked prep targets from RCSB/HARIBOSS metadata. They live under `cases/`, but they are intentionally outside the main runnable `manifest.json` until local inputs are prepared:

| Case | Ligand | Current prep note |
| --- | --- | --- |
| `4gxy-cobalamin-riboswitch` | `B1Z` adenosylcobalamin | Large cofactor; review Mg/IRI ion handling |
| `3irw-c-di-gmp-riboswitch` | `C2E` c-di-GMP | Cyclic dinucleotide; review Mg/IRI ion handling |
| `3d0u-lysine-riboswitch` | `LYS` lysine | Small charged ligand; confirm protonation |
| `4enc-fluoride-riboswitch` | `F` fluoride | Ion-recognition stress test; may need special handling |
| `3oww-glycine-riboswitch` | `GLY` glycine | Tandem aptamer; choose one binding-site instance |
| `4qlm-c-di-amp-riboswitch` | `2BA` c-di-AMP | Cyclic dinucleotide complement to 3IRW |
| `6c64-mango-ii-ekm` | `EKM` dye-like ligand | Promoted to parsed/runnable with chain A; contact review remains |
| `6wzs-ztp-riboswitch` | `UG4` m-1-pyridinyl AICA | Heteroaromatic riboswitch ligand |
| `5dhb-rna-gmp-primer-template` | `5GP` GMP | High-resolution nucleotide-like ligand |
| `3sd3-thf-riboswitch` | `FFO` folate analog | High-resolution larger polar ligand |

`6c64-mango-ii-ekm` has been promoted to the runnable manifest as a parsed stacking case. The remaining HARIBOSS cases are intentionally `seed`: they have no local ignored PDBQT inputs yet and their expected-contact files are empty. Use them as the next HARIBOSS prep queue, not as MacVina/MacDock calibration rows. Promotion order is tracked in [`hariboss_prep_queue.md`](hariboss_prep_queue.md).

## Calibration Coverage

Current coverage is useful but uneven:

| Calibration objective | Current support | Gap |
| --- | --- | --- |
| PDBQT/config compatibility | Runnable manifest cases | Prepare HARIBOSS seed inputs before including them in tool validation runs |
| Base stacking | 4Q9R, 1FMN, and the riboswitch panel | Confirm reviewed labels against local PDBQT atom names |
| Phosphate electrostatics | T6, 1FMN, and five riboswitch panel cases | Need term-specific pose reports and more same-ligand decoys |
| Metal coordination | 1FMN-Mg | Need metal-site decoys or additional metal-containing benchmark cases |
| Same-ligand pose ranking | 4Q9R | Need same-ligand pose decoys for FMN and riboswitch panel cases |
| Ligand enrichment | 1FMN enrichment set | Need traced decoy-generation provenance |
| HARIBOSS breadth | 6C64 parsed plus remaining seed metadata cases | Generate inputs, choose ligand instances, and curate contacts |
| Experimental affinity calibration | No reviewed experimental affinities yet | Need curated experimental affinity sources |
