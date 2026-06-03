# MacVina 10-Case Snapshot

This snapshot records the current MacVina reference-pose metrics for the expanded 10-case manifest.

Generated with:

```sh
cd ~/Projects/macvina
swift run macvinaAptamerCalibrate \
  --manifest ~/Projects/aptamer-docking-benchmarks/manifest.json \
  --csv ~/Projects/aptamer-docking-benchmarks/derived/macvina/shared-metrics.csv \
  --pose-csv ~/Projects/aptamer-docking-benchmarks/derived/macvina/shared-pose-report.csv
```

Current generated files:

```text
derived/macvina/shared-metrics.csv
derived/macvina/shared-pose-report.csv
```

## Summary Metrics

| Case | Vina-inspired | Aptamer | Phosphate | Stacking | Metal | Contact hit | Clash |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `t6-thrombin-vina` | -17.469 | -17.651 | -0.181 | 0.000 | 0.000 | 1.000 | 15 |
| `4q9r-spinach-2zy` | -10.327 | -10.535 | -0.003 | -0.204 | 0.000 | 1.000 | 54 |
| `1fmn-fmn-riboswitch` | -8.716 | -9.230 | -0.314 | -0.200 | 0.000 | 1.000 | 35 |
| `1fmn-fmn-riboswitch-mg` | -8.047 | -8.818 | -0.413 | -0.200 | -0.158 | 1.000 | 38 |
| `2g9c-purine-riboswitch` | -4.527 | -4.527 | 0.000 | 0.000 | 0.000 | 0.000 | 22 |
| `4rzd-preq1-riboswitch` | -3.894 | -4.244 | -0.113 | -0.237 | 0.000 | 0.333 | 37 |
| `2gdi-tpp-riboswitch` | 5.102 | 4.838 | -0.098 | -0.166 | 0.000 | 0.562 | 19 |
| `2ygh-sam-riboswitch` | -11.409 | -11.619 | 0.000 | -0.210 | 0.000 | 0.175 | 24 |
| `3b4b-glms-riboswitch` | -1.923 | -2.332 | -0.153 | -0.257 | 0.000 | 0.375 | 6 |
| `2hoj-tpp-riboswitch` | -7.848 | -8.431 | -0.118 | -0.464 | 0.000 | 0.500 | 26 |

This snapshot was refreshed after the 2G9C expected-contact label correction and MacVina base-stacking near-miss reporting. `2g9c-purine-riboswitch` remains at zero MacVina aptamer contribution and zero expected-contact hit fraction. Its pose report now shows near misses that pass plane distance and angle but fail lateral overlap, confirming that the remaining issue is the local stacking geometry rather than only the removed `N4`/`N9` labels.

## Readout

- The original four-case set remains healthy: T6, 4Q9R, 1FMN, and 1FMN-Mg all show the expected aptamer-aware terms on reference poses.
- 1FMN-Mg is the only current case with a nonzero MacVina `metalCoordination` term.
- The riboswitch panel is case-specific under MacVina reference-pose scoring: 4RZD, 2GDI, 2YGH, 3B4B, and 2HOJ all show nonzero aptamer terms.
- `2g9c-purine-riboswitch` currently shows zero MacVina aptamer-term contribution and zero expected-contact hit fraction despite literature/source stacking notes. Its closest stacking candidates fail the current lateral-overlap cutoff. It has been downgraded to `parsed`; see `cases/2g9c-purine-riboswitch/contact_review.md`.
- The generated CSV parses correctly with Python's `csv` module; case names containing commas are quoted.

## Calibration Implications

- Use this as a MacVina reference-pose baseline, not as a docked-pose search benchmark.
- Compare docked-pose breakdowns against this snapshot carefully: searched poses may show zero phosphate/stacking terms when they miss crystal-like contacts.
- The largest current riboswitch-panel stacking signal is `2hoj-tpp-riboswitch` at `-0.464`.
- The cleanest current metal comparison remains `1fmn-fmn-riboswitch` versus `1fmn-fmn-riboswitch-mg`.
