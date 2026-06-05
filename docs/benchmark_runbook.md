# Benchmark Runbook

This runbook describes how to run the shared 19-case manifest after the HARIBOSS expansion, contact-curation pass, and AptScout ligand-phosphate calibration split.

## 1. Validate Dataset Metadata

Run this from the dataset repo:

```sh
cd ~/Projects/aptamer-docking-benchmarks
python3 scripts/validate_manifest.py
```

Expected current result:

```text
Validated 19 benchmark case(s).
```

This checks JSON/schema/path contracts. It does not prove that AptScout or AptScout can parse every local ignored PDBQT file.

## 2. Validate AptScout Reader Compatibility

Run this from AptScout:

```sh
cd ~/Projects/macvina
swift run macvinaAptamerCalibrate \
  --manifest ~/Projects/aptamer-docking-benchmarks/manifest.json \
  --validate-only
```

Expected current result:

```text
Validation passed for 19 aptamer benchmark case(s).
Parsed 22 output pose(s) and 10 decoy pose(s).
Parsed 41 enrichment active pose(s) and 1423 enrichment decoy pose(s).
Reference aptamer-term coverage: phosphate 16/19, stacking 15/19, metal 2/19
```

The 13 output poses are:

- 4 T6 Vina output modes
- 1 reference pose for 4Q9R
- 1 reference pose for 1FMN
- 1 reference pose for 1FMN-Mg
- 6 riboswitch-panel reference poses
- 9 HARIBOSS-derived RNA/cofactor/fluorogenic-aptamer reference poses

The 10 decoy poses are the 4Q9R same-ligand 2ZY pose decoys.

The enrichment totals are different-ligand active/decoy ligand sets, not same-ligand pose decoys. They are counted during AptScout validation to catch stale `activeCount` and `decoyCount` metadata, but they should not be used for RMSD-to-reference pose metrics.

## 3. Generate AptScout Reports

Run this from AptScout:

```sh
cd ~/Projects/macvina
swift run macvinaAptamerCalibrate \
  --manifest ~/Projects/aptamer-docking-benchmarks/manifest.json \
  --csv ~/Projects/aptamer-docking-benchmarks/derived/macvina/19case-metrics.csv \
  --pose-csv ~/Projects/aptamer-docking-benchmarks/derived/macvina/19case-pose-report.csv \
  --enrichment-csv ~/Projects/aptamer-docking-benchmarks/derived/macvina/19case-enrichment.csv \
  --ablation-csv ~/Projects/aptamer-docking-benchmarks/derived/macvina/19case-ablation.csv
```

Use `19case-metrics.csv` for one-row-per-case summaries. Use `19case-pose-report.csv` for reference/output/decoy ranking, RMSD, clash counts, expected-contact hit fractions, and top aptamer interactions. Use `19case-enrichment.csv` for active-vs-decoy AUC. Use `19case-ablation.csv` to identify which aptamer term drives enrichment.

The current 19-case AptScout reference-pose and ablation snapshot is summarized in [`macvina_19case_snapshot.md`](macvina_19case_snapshot.md). The earlier 10-case snapshot remains in [`macvina_10_case_snapshot.md`](macvina_10_case_snapshot.md).

Interpretation rules:

- Treat `expected_contact_hit_fraction` as a pose-level diagnostic, not an affinity metric.
- Use 4Q9R for same-ligand reference-vs-decoy pose ranking.
- Use 1FMN-Mg as the current metal-coordination smoke test.
- Use the riboswitch panel for structural/contact breadth, not pose-decoy discrimination yet.
- Treat ligand-phosphate enrichment as a pharmacophore signal separate from receptor phosphate geometry.

To run the current aptamer weight sweep:

```sh
cd ~/Projects/macvina
swift run macvinaAptamerCalibrate \
  --manifest ~/Projects/aptamer-docking-benchmarks/manifest.json \
  --sweep-aptamer-weights \
  --sweep-csv ~/Projects/aptamer-docking-benchmarks/derived/macvina/19case-weight-sweep.csv
```

The current best sweep row is:

| Term | Weight |
| --- | ---: |
| receptor phosphate electrostatic | -0.320 |
| ligand phosphate | -1.000 |
| base stacking | -0.500 |
| metal coordination | -0.100 |

For a fast current-best check without repeating the full ligand-phosphate sweep
grid, run a one-row sweep:

```sh
cd ~/Projects/macvina
swift run macvinaAptamerCalibrate \
  --manifest ~/Projects/aptamer-docking-benchmarks/manifest.json \
  --phosphate-weights -0.32 \
  --ligand-phosphate-weights -1.0 \
  --stacking-weights -0.50 \
  --metal-weights -0.10 \
  --sweep-aptamer-weights \
  --sweep-csv ~/Projects/aptamer-docking-benchmarks/derived/macvina/19case-current-best-specificity-sweep.csv
```

The focused current-best sweep is the preferred quick regression check after
small objective-metric changes. Reserve the full 180-row sweep for weight-grid
changes or final release snapshots.

## 4. Validate AptScout Reader Compatibility

Run this from AptScout:

```sh
cd ~/Projects/macdock
swift run macvinaBenchmark -- \
  --aptamer-benchmark ~/Projects/aptamer-docking-benchmarks/manifest.json \
  --aptamer-benchmark-validate-only
```

This should parse the manifest, case files, configs, receptor/ligand PDBQT files, expected-contact files, optional output poses, and optional decoys without docking.

Expected current result:

```text
Validation passed for 19 shared aptamer benchmark case(s).
```

Current parsed local input counts:

| Case | Receptor atoms | Ligand models | Output/reference models | Decoy models |
| --- | ---: | ---: | ---: | ---: |
| `t6-thrombin-vina` | 3240 | 1 | 4 | 0 |
| `4q9r-spinach-2zy` | 1787 | 1 | 1 | 10 |
| `1fmn-fmn-riboswitch` | 2340 | 1 | 1 | 0 |
| `1fmn-fmn-riboswitch-mg` | 2341 | 1 | 1 | 0 |
| `2g9c-purine-riboswitch` | 1422 | 1 | 1 | 0 |
| `4rzd-preq1-riboswitch` | 2389 | 1 | 1 | 0 |
| `2gdi-tpp-riboswitch` | 1668 | 1 | 1 | 0 |
| `2ygh-sam-riboswitch` | 2033 | 1 | 1 | 0 |
| `3b4b-glms-riboswitch` | 417 | 1 | 1 | 0 |
| `2hoj-tpp-riboswitch` | 1636 | 1 | 1 | 0 |

Known AptScout build note: the current build emits an unused-local warning for `vinaWeights` in `macvinaBenchmark/main.swift`. That is a AptScout code cleanup item, not a dataset validation failure.

## 5. Run AptScout Aptamer Benchmark

For a quick smoke run:

```sh
cd ~/Projects/macdock
swift run macvinaBenchmark -- \
  --aptamer-benchmark ~/Projects/aptamer-docking-benchmarks/manifest.json
```

For a more meaningful post-fix riboswitch-panel run, use deeper search:

```sh
cd ~/Projects/macdock
swift run macvinaBenchmark -- \
  --aptamer-benchmark ~/Projects/aptamer-docking-benchmarks/manifest.json \
  --grid-screen-count 10000 \
  --grid-refine-count 10
```

AptScout writes aggregate output under:

```text
~/Projects/aptamer-docking-benchmarks/derived/macdock/
```

## 6. Read AptScout Results Carefully

After Claude's fix, AptScout aptamer terms should be case-specific. For each row:

- `macdock_aptamer_score - macdock_vina_score` should be consistent with the reported aptamer-term contributions.
- `phosphate_contribution` and `stacking_contribution` should depend on docked pose geometry.
- `ligand-P` or ligand-phosphate contribution may differentiate phosphate-bearing ligands even when pose-dependent terms are zero.
- A repeated identical delta across all riboswitch cases is a regression signal.
- Zero phosphate/stacking terms at low search depth may indicate poor pose recovery, not bad expected-contact metadata.

Known current limitation: AptScout metal coordination is still not implemented in the benchmark aptamer path, so cases with `metalCoordination` should not be used to calibrate AptScout metal scoring yet.

## 7. Calibration Gates

Before using a run for calibration, confirm:

- Dataset validation passes.
- AptScout and AptScout validate-only runs pass.
- Output scores include per-term aptamer breakdowns.
- Score deltas match the term breakdowns.
- Same-ligand pose-decoy claims use `decoyPosePath`, not ligand-enrichment decoys.
- Experimental affinity fitting uses only cases with reviewed affinity provenance.
