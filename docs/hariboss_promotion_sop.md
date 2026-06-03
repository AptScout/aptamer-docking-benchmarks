# HARIBOSS Seed Promotion SOP

This procedure converts a tracked HARIBOSS seed directory into a runnable MacVina/MacDock benchmark case. The goal is consistency: every promoted case should differ because of RNA-ligand biology, not because of ad-hoc preparation.

## Promotion Gates

Do not add a HARIBOSS seed case to `manifest.json` until it passes all gates below.

| Gate | Required evidence |
| --- | --- |
| Instance selection | `case.json` records `primaryLigandID`, `selectedReceptorChains`, and `selectedLigandChains` |
| Ion policy | `case.json` records `retainedIonLigands`, `removedIonLigands`, and `preparationNotes` |
| Local inputs | `inputs/receptor.pdbqt`, `inputs/ligand.pdbqt`, `inputs/reference_pose.pdbqt`, and `inputs/conf.txt` exist |
| Config locality | `inputs/conf.txt` references only files in the same `inputs/` directory |
| Reference pose | `referencePoseMode` points to the crystal-derived ligand pose model |
| Contacts | `expected_contacts.json` contains at least one reviewed receptor residue, ligand atom, or interaction kind |
| Validation | `python3 scripts/validate_manifest.py` and MacVina `--validate-only` both pass after adding the case |

## Standard Preparation Rules

Use these defaults unless a case note documents a deliberate exception.

| Step | Default rule |
| --- | --- |
| Receptor chains | Keep the RNA chains forming the selected ligand pocket; remove unrelated copies |
| Ligand instance | Use exactly one crystallographic ligand instance for the first promoted case |
| Alternate conformers | Choose the dominant occupancy conformer and record the choice |
| Waters | Remove crystallographic waters unless a source paper identifies a conserved bridging water |
| Metal/ions | Retain Mg2+, K+, and other ions only when they define the binding site or ligand geometry |
| Non-biological ions | Remove soaking/phasing ions such as iridium hexammine unless they are part of the benchmark question |
| Ligand pose | Generate the reference PDBQT from the co-crystallized coordinates, preserving atom identity as far as the toolchain allows |
| Docking box | Center the box on the crystal ligand heavy atoms with enough padding for the full ligand |
| Contacts | Curate from local crystal distances first, then cross-check the source publication before promotion to `validated` |

## MacVina Calibration Notes

- Keep `metadata_only` seeds outside `manifest.json`; MacVina currently treats manifest entries as runnable.
- Promote fluorogenic aptamers first for base-stacking signal: `6c64-mango-ii-ekm`, then `5bjp-corn-dfho`.
- Promote cyclic nucleotide riboswitches next for ligand-phosphate and base-stacking signal: `3irw-c-di-gmp-riboswitch`, then `4qlm-c-di-amp-riboswitch`.
- Keep ion-special cases separate from ordinary docking calibration until the score term is explicit: especially `4enc-fluoride-riboswitch`.
- For metal-containing cases, record paired ion-retained and ion-removed variants only when both are biologically defensible.

## Promotion Checklist

1. Fill `primaryLigandID`, selected chains, and ion fields in `case.json`.
2. Add local ignored source structure under `inputs/`.
3. Generate receptor, ligand, reference pose, and config PDBQT files.
4. Run `python3 scripts/check_inputs.py --case <case-id> --strict`.
5. Curate expected contacts in `expected_contacts.json`.
6. Add the case to `manifest.json`.
7. Run `python3 scripts/validate_manifest.py`.
8. Run MacVina validate-only against the manifest.
9. Generate a pose report before using the case in a sweep.
