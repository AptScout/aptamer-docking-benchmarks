# 2G9C Enrichment Seed

This case includes a local seed enrichment set under `enrich/`. These files are useful for exploratory active-vs-decoy plumbing, but they are not yet source-reviewed enough for enrichment calibration claims.

## Local Files

| Path | Role | Local contents |
| --- | --- | --- |
| `enrich/receptor.pdbqt` | Enrichment receptor | 1 model, 1422 atoms, 67 RNA residues |
| `enrich/crystal.pdbqt` | Crystal ligand pose | 1 model, 9 atoms, residue `3AY A 91` |
| `enrich/actives.pdbqt` | Active ligand set | 7 models, 89 atoms total, residue label `UNL` |
| `enrich/decoys.pdbqt` | Decoy ligand set | 198 models, different-ligand decoys with mixed residue labels |

## Metadata Caveats

- `case.json` names intended active ligands as `3AY`, `adenine`, `guanine`, and `hypoxanthine`, but the local active PDBQT models are all labeled `UNL`.
- The decoy file has mixed residue labels and should be treated as a generated ligand set, not as curated biochemical identities.
- The decoy generation note says property-matched RDKit decoys with Tanimoto below 0.35, but the exact generation inputs and seed are not yet traced.
- These enrichment ligands are different-ligand actives/decoys, not same-ligand pose decoys. Do not use them for RMSD-to-reference pose metrics.

## Current Use

Use this set only for exploratory enrichment-reader and active-vs-decoy scoring checks. Before promoting it beyond `seed`, review:

- active ligand identity and ordering for all 7 models,
- decoy identity/provenance for all 198 models,
- whether the enrichment receptor matches the main 2G9C receptor exactly,
- whether the local 3AY stacking/contact annotation should be represented as base-stacking, hydrogen-bond/contact, or both.
