# Aptamer Docking Benchmarks

Shared benchmark metadata for aptamer and nucleic-acid docking calibration across MacVina, MacDock, and external comparators such as Vina, Smina, and GNINA.

This repository is intended to version the dataset schema, case metadata, expected contacts, and curation notes. Large molecular structures and generated outputs should stay local under ignored `inputs/`, `raw/`, or `derived/` directories.

## Layout

```text
manifest.json
schema/
  benchmark.schema.json
  case.schema.json
  expected_contacts.schema.json
cases/
  t6-thrombin-vina/
    case.json
    expected_contacts.json
    notes.md
    inputs/       # ignored; local PDB/PDBQT/mmCIF files
    derived/      # ignored; per-tool outputs
raw/              # ignored; downloaded source datasets
derived/          # ignored; aggregate tool outputs
scripts/
```

## Current Cases

- `t6-thrombin-vina`: user-provided T6 thrombin aptamer reference from a traditional AutoDock/QuickVina-style run.
- `4q9r-spinach-2zy`: RNA-ligand stacking case from RCSB/NAKB 4Q9R with local ignored docking inputs and decoys.
- `1fmn-fmn-riboswitch`: parsed RNA-ligand FMN riboswitch case from RCSB PDB 3F4E with local ignored receptor, ligand, reference-pose PDBQT files, and a 1-active/60-decoy ligand-enrichment set.
- `1fmn-fmn-riboswitch-mg`: metal-coordination companion to the FMN riboswitch case with crystallographic Mg `X:304` retained near FMN `O1P`.
- Six-case riboswitch panel: `2g9c-purine-riboswitch`, `4rzd-preq1-riboswitch`, `2gdi-tpp-riboswitch`, `2ygh-sam-riboswitch`, `3b4b-glms-riboswitch`, and `2hoj-tpp-riboswitch`.
- HARIBOSS parsed expansion: `3sd3-thf-riboswitch`, `5dhb-gmp-primer-template`, `6wzs-ztp-riboswitch`, and `6c64-mango-ii-ekm`.
- HARIBOSS seed expansion: remaining RNA-small-molecule candidate case directories from RCSB/HARIBOSS metadata. These are tracked prep targets, not runnable manifest cases until their ignored `inputs/` files and contacts are curated.

See [docs/case_inventory.md](docs/case_inventory.md) for calibration coverage, decoy/enrichment status, and case-specific caveats. See [docs/benchmark_runbook.md](docs/benchmark_runbook.md) for the MacVina/MacDock run sequence. See [docs/macvina_10_case_snapshot.md](docs/macvina_10_case_snapshot.md) for the earlier MacVina reference-pose metrics. See [docs/riboswitch_panel.md](docs/riboswitch_panel.md) for the expanded riboswitch panel and MacDock scoring snapshots. See [docs/macdock_aptamer_scoring_audit.md](docs/macdock_aptamer_scoring_audit.md) for the flat-delta scoring audit. See [docs/contact_review.md](docs/contact_review.md) for expected-contact provenance and promotion criteria. See [docs/affinity_status.md](docs/affinity_status.md) before using any value as an affinity target. See [docs/local_inputs.md](docs/local_inputs.md) for the ignored molecular files expected by the tracked metadata. See [docs/hariboss_prep_queue.md](docs/hariboss_prep_queue.md) and [docs/hariboss_promotion_sop.md](docs/hariboss_promotion_sop.md) for HARIBOSS seed-case promotion order and preparation rules. See [docs/calibration_roadmap.md](docs/calibration_roadmap.md) for the next dataset maturity steps.

## Validation

```sh
python3 scripts/validate_manifest.py
```

The validator checks the top-level manifest, per-case metadata, curation status, expected contacts, and path resolution.

To inventory local ignored molecular inputs before running a tool:

```sh
python3 scripts/check_inputs.py
python3 scripts/check_inputs.py --case 4q9r-spinach-2zy --strict
python3 scripts/check_inputs.py --json
```

The inventory script resolves `configPath`, Vina config `receptor`/`ligand`/`out`/`log`, expected-contact files, and optional decoy pose files. Use `--json` when another tool or CI job needs machine-readable path status and file sizes.

To inspect a case before running docking:

```sh
python3 scripts/summarize_case.py t6-thrombin-vina
```

To scaffold a new seed case:

```sh
python3 scripts/new_case.py my-rna-ligand-case \
  --name "My RNA ligand case" \
  --system-type rna_ligand \
  --config-path inputs/conf.txt
```

## Using With MacVina

From the MacVina repo:

```sh
swift run macvinaAptamerCalibrate \
  --manifest ~/Projects/aptamer-docking-benchmarks/manifest.json
```

To run the current aptamer weight sweep:

```sh
swift run macvinaAptamerCalibrate \
  --manifest ~/Projects/aptamer-docking-benchmarks/manifest.json \
  --sweep-aptamer-weights \
  --sweep-csv ~/Projects/aptamer-docking-benchmarks/derived/macvina/aptamer-weight-sweep.csv
```

## Using With MacDock

From the MacDock repo:

```sh
swift run macvinaBenchmark -- \
  --aptamer-benchmark ~/Projects/aptamer-docking-benchmarks/manifest.json
```

MacDock should write generated benchmark outputs under `derived/macdock/`. See [docs/tool_integration.md](docs/tool_integration.md) for the shared reader and output contract.

## Curation Policy

- Keep benchmark metadata and expected-contact annotations in git.
- Keep large structures, downloaded archives, and generated outputs out of git.
- Prefer reproducible paths and notes over copied opaque files.
- Treat initial expected contacts as calibration hypotheses until validated against crystal contacts, source publications, or expert review.
