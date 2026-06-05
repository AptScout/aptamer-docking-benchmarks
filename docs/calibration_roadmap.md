# Calibration Roadmap

This roadmap describes how to move the dataset from seed/parser coverage toward calibration-ready AptScout and AptScout benchmarks. It is intentionally dataset-focused: the actions below add or review cases, contacts, decoys, and provenance rather than adding new tooling.

The current run sequence is tracked in [`benchmark_runbook.md`](benchmark_runbook.md).

## Current Baseline

The dataset currently has runnable manifest cases plus HARIBOSS seed prep directories:

| Case | Current role |
| --- | --- |
| `t6-thrombin-vina` | Legacy aptamer-protein Vina compatibility anchor |
| `4q9r-spinach-2zy` | RNA-ligand same-ligand pose-decoy and base-stacking benchmark |
| `1fmn-fmn-riboswitch` | RNA-ligand FMN contact-specificity and enrichment benchmark |
| `1fmn-fmn-riboswitch-mg` | Metal-coordination companion benchmark for 1FMN |
| Six-case riboswitch panel | Purine, preQ1, TPP, SAM, and glmS RNA-ligand structural/contact benchmarks |
| HARIBOSS parsed expansion | 3SD3, 5DHB, 6WZS, 6C64, and 5BJP are manifest-visible parsed/contact-review cases |
| HARIBOSS seed expansion | Remaining RNA-small-molecule prep targets with metadata only, outside the main manifest |

The strongest current discriminating signal is 4Q9R, because it has true same-ligand pose decoys. The strongest current breadth signal is the riboswitch panel, because it spans several ligand chemotypes and RNA pockets. The strongest current metal signal is 1FMN-Mg, but it is a smoke test rather than a weight-calibration set because it has no metal-site decoys.

Part of the HARIBOSS expansion is now in the runnable manifest. The remaining seed cases are deliberately tracked as case directories so the prep queue is shared, but each one still needs local receptor/ligand/reference PDBQT files, a self-contained config, instance selection, and contact review before it is added to `manifest.json`.

## Near-Term Dataset Priorities

1. Promote 4Q9R contact annotation toward `contact_reviewed`.
   - Review the 4Q9R crystal contacts around ligand `2ZY`.
   - Confirm whether `R:54` is the best stable receptor residue label for the base-stacking annotation.
   - Confirm or replace ligand atom label `C16_4` with the most reproducible ligand atom label.
   - Keep `inputs/decoys.pdbqt` as same-ligand pose decoys for RMSD-aware calibration.

2. Add same-ligand FMN pose decoys.
   - Keep these under `cases/1fmn-fmn-riboswitch/inputs/`.
   - Add them as `decoyPosePath` only if they are alternate FMN poses with the same ligand identity and atom layout.
   - Keep the existing `enrichmentSets` entry separate because those decoys are non-FMN ligands.

3. Add metal-site discriminating examples.
   - Either add metal-aware decoys for `1fmn-fmn-riboswitch-mg` or add one or more additional crystallographic metal-containing RNA-ligand cases.
   - Record whether decoys disrupt Mg geometry, ligand placement, or both.
   - Preserve the plain 1FMN versus 1FMN-Mg comparison as a paired scoring sanity check.

4. Tighten T6 provenance.
   - Record the upstream biological/source structure or original benchmark origin if available.
   - Confirm the aptamer/protein residue mapping behind expected contact `I:667`.
   - Keep the QuickVina `-17.2 kcal/mol` score marked as docking reference only.

5. Use the riboswitch panel to expose flat aptamer scoring.
   - Track AptScout/AptScout per-term pose reports for all six panel cases.
   - Treat identical aptamer deltas across the panel as a scoring-path diagnostic.
   - Add same-ligand pose decoys to at least one TPP case and one non-TPP case.

6. Curate experimental affinity sources.
   - Do not use current docking scores as experimental targets.
   - Add affinity only when the source, assay type, units, and caveats are known.
   - Promote cases to `affinity_reviewed` only after that information is recorded.

7. Promote HARIBOSS seed cases into runnable parsed cases.
   - Continue with `3irw-c-di-gmp-riboswitch`, `4qlm-c-di-amp-riboswitch`, and `3d0u-lysine-riboswitch` because they are likely to exercise base stacking, phosphate-aware, and charged-ligand terms.
   - Choose exactly one receptor/ligand instance per case unless a structure clearly requires companion cases.
   - Record ion-retention decisions in notes before generating PDBQT.
   - Keep `4enc-fluoride-riboswitch` separate from ordinary small-molecule docking until the ion-docking policy is explicit.

## Calibration Objectives

| Objective | Good current case | Needed dataset addition |
| --- | --- | --- |
| Vina-compatible loading | All current cases | Keep configs self-contained and path-stable |
| Reference-vs-decoy pose ranking | `4q9r-spinach-2zy` | Add same-ligand FMN, riboswitch-panel, and metal-site decoys |
| Base-stacking calibration | `4q9r-spinach-2zy`, `1fmn-fmn-riboswitch`, riboswitch panel | Confirm local PDBQT atom labels and collect per-term reports |
| Phosphate-electrostatic calibration | `t6-thrombin-vina`, `1fmn-fmn-riboswitch`, riboswitch panel | Reviewed residue/atom contacts and more decoy examples |
| Metal-coordination calibration | `1fmn-fmn-riboswitch-mg` | Metal-site decoys or additional metal cases |
| Ligand enrichment | `1fmn-fmn-riboswitch` | Decoy provenance and additional active/decoy sets |
| RNA-ligand breadth | HARIBOSS parsed and seed expansion | Convert remaining seed metadata to parsed PDBQT cases |
| Experimental affinity fitting | None yet | Reviewed affinity sources |

## Promotion Path

Use the curation statuses as gates:

| Status | Dataset meaning |
| --- | --- |
| `seed` | Metadata is useful for exploratory runs, but structure/contact/affinity claims are provisional |
| `parsed` | Inputs parse reproducibly and receptor/ligand roles are identified |
| `contact_reviewed` | Expected contacts have been manually reviewed against source coordinates or literature |
| `affinity_reviewed` | Experimental affinity source, unit, assay, and caveats have been reviewed |
| `validated` | Case is ready for shared AptScout/AptScout calibration and regression reporting |

## Recommended Next Dataset Work

The highest-value next dataset additions are:

1. Same-ligand FMN pose decoys for `1fmn-fmn-riboswitch`.
2. Same-ligand pose decoys for one TPP riboswitch case and one non-TPP riboswitch case.
3. A metal-site decoy set or second metal-containing RNA-ligand case.
4. Manual contact review notes for 4Q9R, 3F4E, and the six-case riboswitch panel, starting with the 2G9C atom-label/ring-plane mismatch.
5. Experimental affinity provenance for any case where a trustworthy source is available.
6. HARIBOSS case prep, continuing with one fluorogenic aptamer (`5bjp`) and one cyclic dinucleotide riboswitch (`3irw` or `4qlm`).
