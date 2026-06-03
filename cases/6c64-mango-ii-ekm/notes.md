# Mango-II Fluorescent RNA Aptamer Bound to EKM

Parsed benchmark case `6c64-mango-ii-ekm`.

## Source

- RCSB PDB: `6C64`
- HARIBOSS example: Mango-II fluorescent aptamer
- Ligand: `EKM`
- Method/resolution: X-ray diffraction, 3.00014879601 A

## Prepared Instance

- Receptor: RNA chain `A`
- Ligand: `EKM` chain `A`, residue `101`
- Removed ions: crystallographic `K`
- Local source: `inputs/6c64.pdb`
- Local receptor precursor: `inputs/receptor_rna_chain_a.pdb`
- Local ligand precursor: `inputs/ligand_ekm_chain_a.pdb`
- Local PDBQT files: `inputs/receptor.pdbqt`, `inputs/ligand.pdbqt`, `inputs/reference_pose.pdbqt`
- Config: `inputs/conf.txt`

The first promoted version removes potassium ions so the case exercises MacVina's base-stacking behavior without mixing in an unsupported K-specific scoring question. A retained-K companion can be added later if the benchmark grows explicit ion handling.

Open Babel generated the initial PDBQT files. It emitted a ligand kekulization warning for EKM, so aromatic atom typing should be reviewed before promoting this case beyond `parsed`.

## Contact TODO

- Curate aromatic stacking contacts carefully; this is likely a high-value base-stacking case.
- Cross-check the expected-contact residues and ligand atom labels against the source paper.

## Initial MacVina Snapshot

MacVina reference-pose scoring after initial promotion:

```text
macvina-vina -12.156
aptamer      -12.389
phosphate     -0.032
stacking      -0.201
metal          0.000
contact-hit    0.793
```

Top reported interaction:

```text
baseStacking A:101:C12#17 -> A:29:C8#635 3.98 A score -0.201
```

This confirms the case exercises the base-stacking term, but the contact labels remain first-pass until literature review.
