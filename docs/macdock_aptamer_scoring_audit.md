# MacDock Aptamer Scoring Audit

This note records the MacDock aptamer-scoring issue that was exposed by the six-case riboswitch panel and Claude's current fix summary.

## Original Diagnostic

The riboswitch panel initially reported a constant aptamer delta for every case:

```text
2g9c-purine-riboswitch   Vina -6.31   Aptamer -6.52   delta -0.21
4rzd-preq1-riboswitch    Vina -7.06   Aptamer -7.27   delta -0.21
2gdi-tpp-riboswitch      Vina -5.30   Aptamer -5.51   delta -0.21
2ygh-sam-riboswitch      Vina -11.06  Aptamer -11.27  delta -0.21
3b4b-glms-riboswitch     Vina -2.76   Aptamer -2.97   delta -0.21
2hoj-tpp-riboswitch      Vina -7.51   Aptamer -7.72   delta -0.21
```

That flat delta was a benchmark diagnostic, not a calibration result. The six cases have different ligands, receptor pockets, expected contacts, and interaction terms, so a mature aptamer-aware scorer should produce case-specific contributions.

## Root Cause

Claude traced the flat delta to placeholder logic in MacDock's `runAptamerBenchmark` path. The benchmark code was adding:

- a phosphate contribution whenever the receptor had any phosphate positions
- a stacking contribution whenever the receptor had any nucleobase centers

Because every RNA receptor has both features, every riboswitch case got the same contribution:

```text
phosphate: -1.5 * 0.1  = -0.15
stacking:  -1.2 * 0.05 = -0.06
total:                 = -0.21
```

The placeholder did not depend on docked pose geometry, ligand identity, or expected-contact annotations.

## Reported Fix

Claude reports that MacDock now routes the aptamer benchmark path through a real `VirtualScreeningSession` with an `AptamerGridConfig`:

- receptor phosphate positions are baked into a Gaussian phosphate grid
- receptor nucleobase centers are baked into a Gaussian stacking grid
- `ReceptorGridScorer.scoreSync` samples those grids at transformed ligand atom positions
- `aptamerBreakdown(pose:)` reports phosphate, stacking, and ligand-phosphate contributions for the top pose

This means phosphate and stacking terms are now pose-geometry dependent in MacDock's benchmark path. The ligand-phosphate term remains pose-independent and differentiates ligands that contain phosphate atoms.

## Post-Fix Interpretation

Claude's post-fix breakdown summary:

| Case | Ligand-P | Phosphate | Stacking | Interpretation |
| --- | ---: | ---: | ---: | --- |
| `2g9c-purine-riboswitch` | 0 | -0.13 | 0 | 3AY has no P; some N atoms land near receptor phosphate grid |
| `4rzd-preq1-riboswitch` | 0 | 0 | 0 | PRF pose misses expected crystal contacts |
| `2gdi-tpp-riboswitch` | -1.70 | 0 | 0 | CCC pyrophosphate contributes ligand-P; docked pose misses stacking |
| `2ygh-sam-riboswitch` | 0 | 0 | 0 | SAM has no P; current pose misses contacts |
| `3b4b-glms-riboswitch` | -0.85 | 0 | 0 | GLP has one phosphate |
| `2hoj-tpp-riboswitch` | -1.42 | 0 | 0 | TPP pyrophosphate contributes ligand-P |

The panel now differentiates cases, but most pose-dependent phosphate/stacking terms remain zero at the reported low search settings. Treat that as a pose-quality and search-depth limitation, not as proof that the expected contacts are absent.

## Dataset Implications

- Keep the constant `-0.21` table as historical evidence that the panel caught placeholder scoring.
- Future MacDock and MacVina reports should include per-term aptamer breakdowns before using scores for calibration.
- Same-ligand pose decoys are still needed for the riboswitch panel, because the current panel mostly validates loader/scoring paths rather than reference-vs-decoy discrimination.
- Expected-contact hit metrics should eventually be pose-geometry based, not just receptor-feature based.
- Metal coordination remains a separate gap for MacDock unless a metal grid or post-scoring metal term is added.

## Suggested MacDock Benchmark Settings

Claude recommends deeper search before interpreting phosphate and stacking breakdowns:

```sh
--grid-screen-count 10000 --grid-refine-count 10
```

Use the resulting pose-level term breakdowns to decide whether the docked poses reproduce crystal-like contacts.
