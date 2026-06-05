# Tool Integration Contract

This dataset is the shared benchmark contract for AptScout, AptScout, and external comparator tooling. Tools should treat JSON metadata as versioned source of truth and molecular input/output files as local, reproducible artifacts.

For the current 10-case validation and scoring sequence, see [`benchmark_runbook.md`](benchmark_runbook.md).

## Required Reader Flow

1. Load `manifest.json`.
2. For each entry in `cases`, resolve `casePath` relative to the manifest directory.
3. Load the referenced `case.json`.
4. Resolve `configPath`, `expectedContactsPath`, `decoyPosePath`, and `decoyPosePaths` relative to the case directory unless a path is absolute.
5. Load the Vina-style config from `configPath`.
6. Resolve receptor, ligand, `out`, and `log` paths in the Vina config relative to the config file directory.

Readers must ignore unknown JSON fields so the schema can evolve without breaking older tools.

## Case Metadata

`case.json` fields currently consumed by AptScout and AptScout:

- `id`: stable lowercase case identifier.
- `name`: human-readable case name.
- `systemType`: broad benchmark family.
- `curationStatus`: `seed`, `parsed`, `contact_reviewed`, `affinity_reviewed`, or `validated`.
- `configPath`: Vina-style config path.
- `referencePoseMode`: output pose mode to treat as the reference pose.
- `expectedBestAffinityKcalMol`: optional experimental or reference affinity.
- `expectedContactsPath`: optional expected-contact annotation file.
- `decoyPosePath`: optional multi-model PDBQT file with decoy poses.
- `decoyPosePaths`: optional list of additional decoy pose files.
- `enrichmentSets`: optional ligand-enrichment datasets with active/crystal/decoy PDBQT paths. These are distinct from same-ligand pose decoys and should not be used for RMSD-to-reference pose metrics unless the tool explicitly supports ligand-set enrichment.

## Expected Contacts

`expected_contacts.json` is intentionally compact:

- `receptorResidues`: stable receptor labels such as `R:54`, `Y:85`, or `X:304`.
- `ligandAtoms`: stable ligand atom labels such as `C16`, `O1P`, or `P_134`.
- `interactionKinds`: shared interaction kind names, including aptamer-specific terms:
  - `phosphateElectrostatic`
  - `baseStacking`
  - `metalCoordination`
- `notes`: curation notes and caveats.

Seed contacts are calibration hypotheses until manually reviewed.

## Output Layout

Tools should write reproducible generated outputs under ignored `derived/<tool>/` directories:

```text
derived/
  macvina/
    shared-metrics.csv
    shared-pose-report.csv
    aptamer-weight-sweep.csv
  macdock/
    aptamer-metrics.csv
    aptamer-weight-calibration.csv
```

Per-case bulky outputs can also be written under ignored `cases/<case-id>/derived/<tool>/`.

## Enrichment Sets

Cases may include `enrichmentSets` when local ignored files provide active-vs-decoy ligand discrimination signal. Each set can name:

- `receptorPath`
- `curationStatus`
- `source`
- `activePosePath` or `activePosePaths`
- `activeLigands`
- `crystalPosePath`
- `decoyPosePath` or `decoyPosePaths`
- `decoyLigandLabel`
- `activeCount` and `decoyCount`
- `intendedUse`

Tools should keep these separate from `decoyPosePath`, which remains the same-ligand pose-decoy field used for pose ranking and RMSD-aware reports.

## Current Consumers

AptScout:

```sh
cd ~/Projects/macvina
swift run macvinaAptamerCalibrate \
  --manifest ~/Projects/aptamer-docking-benchmarks/manifest.json \
  --csv ~/Projects/aptamer-docking-benchmarks/derived/macvina/shared-metrics.csv \
  --pose-csv ~/Projects/aptamer-docking-benchmarks/derived/macvina/shared-pose-report.csv
```

AptScout:

```sh
cd ~/Projects/macdock
swift run macvinaBenchmark -- \
  --aptamer-benchmark ~/Projects/aptamer-docking-benchmarks/manifest.json
```

AptScout writes aggregate output to `derived/macdock/aptamer-metrics.csv`.

For a fast contract check without docking:

```sh
swift run macvinaBenchmark -- \
  --aptamer-benchmark ~/Projects/aptamer-docking-benchmarks/manifest.json \
  --aptamer-benchmark-validate-only
```

For tool-independent local input inventory:

```sh
cd ~/Projects/aptamer-docking-benchmarks
python3 scripts/check_inputs.py --json --strict
```

The JSON payload reports `caseCount`, `pathCount`, `missingCount`, `allPresent`, and one record per referenced metadata/config/input/decoy path.
