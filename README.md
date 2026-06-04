# RNA Aptamer–Ligand Docking Benchmark

**19 crystallographically validated RNA aptamer–small-molecule cases for structure-based virtual screening.**

The first publicly curated benchmark for RNA aptamer VS with ROC-AUC evaluation — the DUD-E equivalent for RNA drug discovery.

## Key Results (MacDock GPU, aptamer scoring)

| Metric | Value |
|--------|-------|
| Cases evaluated | 17 / 19 |
| AUC improves (ΔAUC > +0.05) | 7 / 17 |
| Mean ΔAUC | +0.080 |
| **Near-native poses (RMSD < 2 Å)** | **8 / 17 ★** |
| Median RMSD | 5.1 Å |
| Max EF₁% | 50× (GMP, c-di-GMP) |
| Spearman ρ (score vs Kd) | 0.13 |

## Structure

```
cases/
  {case-id}/
    inputs/
      receptor.pdbqt   # RNA receptor
      ligand.pdbqt     # Crystal ligand
      conf.txt         # Docking box parameters
      reference_pose.pdbqt  # Crystal reference for RMSD
    enrich/
      actives.pdbqt    # True binders (1–14 compounds)
      decoys.pdbqt     # Property-matched decoys (10–532 compounds)
    case.json          # Metadata (PDB ID, resolution, affinity source)
    expected_contacts.json  # Literature-validated binding contacts
manifest.json          # Master case list (19 entries)
derived/macdock/
  enrichment-auc.csv                # AUC results (17 cases)
  gemini_validation_complete.csv    # Full Gemini validation (AUC + EF1% + RMSD)
  aptamer-metrics.csv               # Per-case crystal-pose scoring breakdown
figures/
  fig1_aptamer_auc.pdf              # Main AUC bar chart
  fig2_term_breakdown.pdf           # Per-term scoring breakdown
  fig3_ligandP_vs_dauc.pdf          # Ligand-P contribution scatter
  fig4_affinity_correlation.pdf     # Score vs Kd scatter
scripts/
  run_full_benchmark.py             # Complete Gemini validation pipeline
  new_case.py                       # Scaffold a new case
```

## 19 Cases

| Structural Family | Cases |
|-------------------|-------|
| Riboswitches | TPP (×2), SAM-I, Purine, PreQ1, ZTP, Lysine, Glycine, glmS |
| Fluorogenic aptamers | Spinach, Mango-II, Corn |
| RNA–ligand contexts | FMN riboswitch (×2), GMP primer-template |
| DNA aptamer–protein | Thrombin T6 |
| Excluded | Cobalamin (MW > 1300 Da), Fluoride (no pocket) |

## Three Novel Insights

1. **The Mg²⁺ Anomaly** — Explicit unrelaxed Mg²⁺ in rigid-receptor docking collapses RMSD from 0.3 → 16.6 Å while maintaining correct enrichment. Proof that soft-boundary metal representation is required for RNA VS.

2. **The Lysine Paradox** — RMSD = 0.3 Å (near-perfect geometry) but AUC = 0.277 (near-random enrichment). Pose quality and enrichment quality are orthogonal metrics requiring separate evaluation.

3. **Aromatic Decoy Contamination** — Property-matched decoys for large aromatic ligands (FMN, preQ1) contain aromatic scaffolds that the nucleobase-stacking term rewards non-specifically. Extended exclusion SMARTS required for aromatic ligands.

## Running the Benchmark

```bash
# Full Gemini validation (AUC + RMSD + EF1%) for one case
python3 scripts/run_full_benchmark.py --case 2hoj-tpp-riboswitch

# All 17 evaluable cases
python3 scripts/run_full_benchmark.py

# MacDock aptamer benchmark (single-pose scoring)
macvinaBenchmark \
  --aptamer-benchmark manifest.json \
  --aptamer-scoring \
  --grid-hybrid \
  --grid-screen-count 1000 \
  --grid-refine-count 3
```

Requires: [MacDock](https://github.com/khoonie/macdock), RDKit, Open Babel 3.x.

## Citation

[Paper submitted to NAR / JCIM — citation TBD]

## License

MIT — all PDBQT files derived from RCSB PDB structures (open access).
