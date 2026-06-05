# AptScout 19-Case Calibration Snapshot

Date: 2026-06-04

This snapshot records the current AptScout aptamer-calibration baseline after
splitting the ligand-phosphate prior out of receptor phosphate electrostatics
and adding an enrichment ablation report.

## Inputs

- Manifest: `manifest.json`
- Cases: 19
- Output poses parsed by AptScout validate-only: 22
- Same-ligand decoy poses parsed: 10
- Enrichment active poses parsed: 41
- Enrichment decoy poses parsed: 1423
- Latest generated reports:
  - `derived/macvina/19case-metrics.csv`
  - `derived/macvina/19case-pose-report.csv`
  - `derived/macvina/19case-enrichment.csv`
  - `derived/macvina/19case-weight-sweep.csv`
  - `derived/macvina/19case-ablation.csv`
  - `derived/macvina/19case-current-best-specificity-sweep.csv`

## Best Current Sweep

Best objective row from `19case-weight-sweep.csv` before the contact-specificity
metric was corrected:

| Term | Weight |
| --- | ---: |
| receptor phosphate electrostatic | -0.320 |
| ligand phosphate | -1.000 |
| base stacking | -0.500 |
| metal coordination | -0.100 |

Aggregate metrics:

| Metric | Value |
| --- | ---: |
| objective | 2.496 |
| mean enrichment AUC | 0.726 |
| mean best-active/decoy margin | -0.395 |
| mean expected contact hit fraction | 0.562 |
| mean expected contact specificity | 0.000 |
| top-1 reference accuracy | 1.000 |
| mean active aptamer term count | 2.158 |

The new ligand-phosphate axis improves the calibration objective mainly through
score separation and active term coverage. Mean AUC changes only slightly, but
the best-active/decoy margin improves substantially relative to the previous
combined-phosphate baseline.

After the contact-specificity calculation was corrected to compare the
reference pose against the mean same-ligand pose-decoy contact hit fraction,
a one-row current-best sweep was run instead of repeating the full 180-row
grid. That focused run is stored at
`derived/macvina/19case-current-best-specificity-sweep.csv`.

| Metric | Current-best focused value |
| --- | ---: |
| objective | 2.383 |
| mean enrichment AUC | 0.726 |
| mean best-active/decoy margin | -0.395 |
| mean expected contact hit fraction | 0.562 |
| mean expected contact specificity | 0.150 |
| top-1 reference accuracy | 1.000 |
| mean active aptamer term count | 2.158 |

## Ablation Result

Mean AUC over the 8 enrichment sets in `19case-ablation.csv`:

| Mode | Mean AUC | Mean best-active/decoy margin |
| --- | ---: | ---: |
| Vina only | 0.637 | -0.975 |
| receptor phosphate only | 0.638 | -0.951 |
| ligand phosphate only | 0.722 | -0.840 |
| ligand phosphate, AptScout-like weight | 0.723 | -0.225 |
| base stacking only | 0.637 | -0.912 |
| metal coordination only | 0.637 | -0.975 |
| phosphate terms only | 0.723 | -0.816 |
| all default terms | 0.723 | -0.753 |
| all terms, best current weights | 0.724 | -0.096 |

Interpretation: current RNA-ligand enrichment lift is dominated by the
ligand-phosphate pharmacophore term. Receptor phosphate, stacking, and metal
terms remain important for pose-level interpretation and contact calibration,
but they do not drive most of the current active-vs-decoy AUC signal.

Largest ligand-phosphate gains versus Vina-only:

| Case | Enrichment set | AUC delta |
| --- | --- | ---: |
| `3b4b-glms-riboswitch` | `glms-enrich` | +0.250 |
| `2hoj-tpp-riboswitch` | `tpp-enrich` | +0.214 |
| `2hoj-tpp-riboswitch` | `tpp-enrich-filtered` | +0.214 |
| `2gdi-tpp-riboswitch` | `tpp-enrich-filtered` | +0.006 |

Cases without phosphate-bearing active/decoy separation, such as purine,
PreQ1, and SAM, do not benefit materially from ligand phosphate.

## Current Weak Spots

- `4rzd-preq1-riboswitch` is near random in enrichment (`AUC 0.500`) and its
  local `enrich/decoys.pdbqt` currently contains 74 decoys, not the older
  272-count metadata value.
- `2gdi-tpp-riboswitch` remains margin-limited despite being above random; the
  prepared Mg geometry does not currently trigger AptScout metal coordination.
- Metal coordination coverage is still thin: only 2 of 19 reference cases have
  active metal terms.
- Contact specificity is now nonzero in the focused current-best sweep
  (`0.150`), driven by 4Q9R same-ligand pose decoys. It is still supported by
  only one pose-decoy case, so broader same-ligand decoy coverage remains a
  production-readiness gap.

## Verification

Last commands run after this snapshot:

```sh
cd /Users/khoon-sengtan/Projects/aptamer-docking-benchmarks
python3 scripts/validate_manifest.py

cd /Users/khoon-sengtan/Projects/macvina
swift run macvinaAptamerCalibrate \
  --manifest /Users/khoon-sengtan/Projects/aptamer-docking-benchmarks/manifest.json \
  --validate-only

swift test
```

Results:

- Dataset validation: `Validated 19 benchmark case(s).`
- AptScout validate-only: passed for 19 cases.
- AptScout tests: 310 tests, 0 failures.
