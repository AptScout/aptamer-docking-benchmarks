# Curation Checklist

Use this checklist before promoting a benchmark case beyond `seed`.

## Required Metadata

- Case ID follows lowercase slug format, for example `t6-thrombin-vina`.
- `systemType` is selected from the shared schema.
- `curationStatus` is set to the current maturity level.
- Source database or origin is recorded.
- Structure ID is recorded when available, such as PDB or NAKB identifier.
- Reference pose source is clear.
- Config/input paths resolve on the local machine or are documented as intentionally local.
- Optional decoy pose paths are listed with `decoyPosePath` or `decoyPosePaths` when a case has reference-vs-decoy calibration signal.
- Optional ligand-enrichment files are listed under `enrichmentSets` instead of pose-decoy fields when decoys are different ligands.
- `python3 scripts/check_inputs.py --case <case-id> --strict` passes on a machine with local ignored inputs restored.

## Structure Review

- Receptor and ligand/aptamer roles are identified.
- Nucleic-acid residues are present and named consistently.
- Phosphate atoms are present when phosphate scoring is expected.
- Metals are retained or intentionally removed.
- Protonation/charge source is documented.
- Missing residues, alternate conformations, or unusual modifications are noted.

## Contact Review

- Expected contacts are separated into `expected_contacts.json`.
- Contact annotations name receptor residues in a stable format such as `I:667`.
- Ligand atoms use stable labels such as `P_134` when atom IDs are inherited from PDBQT.
- Interaction kinds are selected from the shared schema.
- Seed contacts derived from AptScout/AptScout are labeled as hypotheses until manually reviewed.
- Metal-mediated contacts name the ion residue, for example `X:304`, and the ligand donor atom, for example `O1P`.

## Affinity Review

- Affinity value and unit are recorded when known.
- Source is identified, such as PDBbind, publication, ITC, SPR, or original Vina log.
- Assay caveats are noted.
- Avoid treating docking score as experimental affinity.

## Status Levels

- `seed`: metadata is useful for exploratory tooling, but contacts/affinity are not fully reviewed.
- `parsed`: files parse reproducibly and roles are identified.
- `contact_reviewed`: expected contacts have been manually reviewed.
- `affinity_reviewed`: affinity source and unit have been reviewed.
- `validated`: ready for calibration/regression reporting across tools.
