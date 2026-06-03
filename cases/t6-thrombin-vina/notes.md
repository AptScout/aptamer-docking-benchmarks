# T6 Thrombin Vina Reference

Initial shared benchmark case derived from the user-provided traditional AutoDock/QuickVina-style run files originally stored in `~/Projects/macvina/1`.

## Files

The current case uses a self-contained local Vina config:

```text
inputs/confainaT6.txt
```

That config resolves:

```text
PROTEIN.pdbqt
T6_model1.pdbqt
outT6.pdbqt
logT6.txt
```

The `inputs/` directory is intentionally ignored by git. Restore it by copying the original T6 run files into this case directory when setting up the local benchmark workspace.

See `vina_outputs.md` for local file counts, QuickVina mode affinities, and current MacVina pose-level diagnostics.

## Current Reference Metrics

MacVina aptamer calibration harness, mode 1:

```text
Vina affinity: -17.200 kcal/mol
MacVina Vina-inspired score: -17.469
MacVina aptamer-interaction score: -17.651
Phosphate contribution: -0.181
Contact hit: 1.000
```

The `-17.2 kcal/mol` value is the best QuickVina output affinity from the local legacy run. It is a docking reference score for compatibility/regression checks, not a curated experimental binding affinity.

## Current Seed Contact

```text
phosphateElectrostatic A:6:P#134 -> I:667:HZ2#93
phosphateElectrostatic A:6:P#134 -> I:667:HZ3#94
phosphateElectrostatic A:6:P#134 -> I:667:NZ#91
```

This contact is a calibration seed, not yet a literature-validated ground truth annotation.
