# HARIBOSS Prep Queue

This page tracks HARIBOSS/RCSB RNA-small-molecule cases that have seed metadata in `cases/` but are not yet included in the runnable `manifest.json`.

Promotion rules are defined in [`hariboss_promotion_sop.md`](hariboss_promotion_sop.md).

Keep these cases outside the main manifest until each has:

- local ignored `inputs/receptor.pdbqt`, `inputs/ligand.pdbqt`, `inputs/reference_pose.pdbqt`, and `inputs/conf.txt`;
- one explicitly chosen receptor/ligand instance when the PDB has multiple copies;
- a documented ion-retention policy;
- expected contacts curated from local coordinates and source literature.

## Seed Cases

| Case | PDB | Ligand | Why it matters | First prep decision |
| --- | --- | --- | --- | --- |
| ~~`4gxy-cobalamin-riboswitch`~~ ⏸ deferred (MW 1300+, too large) | `4GXY` | `B1Z` adenosylcobalamin | Large cofactor and ion-rich pocket | Decide Mg/IRI retention |
| ~~`3irw-c-di-gmp-riboswitch`~~ ✅ promoted | `3IRW` | `C2E` c-di-GMP | Cyclic dinucleotide with phosphate/base signal | Decide Mg/IRI retention |
| ~~`3d0u-lysine-riboswitch`~~ ✅ promoted | `3D0U` | `LYS` lysine | Small charged amino-acid ligand | Confirm ligand protonation/charge |
| ~~`4enc-fluoride-riboswitch`~~ ❌ not_applicable (single F⁻ ion, undockable) | `4ENC` | `F` fluoride | Ion-recognition stress test | Decide whether it is dockable as PDBQT |
| ~~`3oww-glycine-riboswitch`~~ ✅ promoted | `3OWW` | `GLY` glycine | Tandem aptamer/cooperative binding | Choose chain A or B instance |
| ~~`4qlm-c-di-amp-riboswitch`~~ ✅ promoted | `4QLM` | `2BA` c-di-AMP | Cyclic dinucleotide complement to 3IRW | Decide SO4/Mg retention |
| ~~`6c64-mango-ii-ekm`~~ ✅ promoted (Codex) | `6C64` | `EKM` | Fluorogenic aptamer, likely stacking-rich | Promoted to parsed/runnable with chain A; contact review remains |
| ~~`5bjp-corn-dfho`~~ ✅ promoted | `5BJP` | `747` DFHO | Fluorogenic aptamer, aromatic ligand | Promoted to parsed/runnable with chain Y; contact review remains |
| ~~`6wzs-ztp-riboswitch`~~ ✅ promoted | `6WZS` | `UG4` | Heteroaromatic riboswitch ligand | Choose chain A or B instance |
| ~~`5dhb-gmp-primer-template`~~ ✅ promoted | `5DHB` | `5GP` GMP | High-resolution nucleotide-like ligand | Choose one ligand-bearing chain |
| ~~`3sd3-thf-riboswitch`~~ ✅ promoted | `3SD3` | `FFO` folate analog | High-resolution larger polar ligand | Decide IRI retention |

## Promotion Order

Start with:

1. `3irw-c-di-gmp-riboswitch` or `4qlm-c-di-amp-riboswitch` for cyclic nucleotide phosphate/base behavior.
2. `3d0u-lysine-riboswitch` for charged small-ligand behavior.
3. `3oww-glycine-riboswitch` for tandem aptamer binding.

Hold `4enc-fluoride-riboswitch` until the benchmark has an explicit ion-docking policy.

## Metadata Fields To Fill Before Promotion

Each seed `case.json` may use these optional fields before it enters the runnable manifest:

- `preparationStatus`
- `primaryLigandID`
- `selectedReceptorChains`
- `selectedLigandChains`
- `retainedIonLigands`
- `removedIonLigands`
- `preparationNotes`
