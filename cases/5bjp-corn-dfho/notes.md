# Corn RNA Aptamer Bound to DFHO

Parsed benchmark case `5bjp-corn-dfho`.

## Source

- RCSB PDB: `5BJP`
- HARIBOSS example: Corn RNA aptamer
- Ligand: `747` DFHO
- Method/resolution: X-ray diffraction, 2.51 A
- Chains: Two 36-mer RNA chains (E and Y); only chain Y bears DFHO

## Prepared Instance

- Receptor: RNA chain `Y`
- Ligand: `747` chain `Y`, residue `104`
- Removed ions: crystallographic `IR` (iridium hexammine, soaking/phasing), `K` (potassium), `MG` (magnesium on chain E), `DMS` (dimethyl sulfoxide)
- Local source: `inputs/5bjp.pdb`
- Local receptor precursor: `inputs/receptor_rna_chain_y.pdb`
- Local ligand precursor: `inputs/ligand_747_chain_y.pdb`
- Local PDBQT files: `inputs/receptor.pdbqt`, `inputs/ligand.pdbqt`, `inputs/reference_pose.pdbqt`
- Config: `inputs/conf.txt`

The first promoted version removes all crystallographic ions so the case exercises MacVina's base-stacking behavior without mixing in unsupported ion-specific scoring questions. Chain E (a crystallographic dimer) was excluded because it does not bear the DFHO ligand.

Open Babel 3.1.0 generated the initial PDBQT files. PDBQT atom names were preserved from the PDB source. The ligand has 2 active rotatable torsions in obabel's perception.

The generated PDBQT atom records were normalized after conversion so MacVina's whitespace-splitting PDBQT parser can read coordinates below -100 A, such as the chain Y receptor z coordinates.

## Contact Notes

- Tightest contact: G:22:N1 to 747:O14 at 2.90 A
- Key aromatic interactions: G:22, G:25, A:24, and G:12 residues form the primary ligand pocket
- DFHO has two aromatic regions: a fluorophenyl ring (F1, C2, C1, O1, C3, C4, C5, C, F) and an imidazolone-oxime conjugated system (C6, C7, C10, C12, N13, O14, N15, C16, C17, N18, O19)
- Six receptor residues have atoms within 4.0 A: A:11, G:12, G:15, G:22, A:24, G:25
- G:25 has the most contacts (44 atoms within 4.0 A), forming a broad pocket around the ligand
- Expected contacts are hypothesis-level: curated from crystal geometry only, not yet cross-checked with source publication

## Contact TODO

- Curate aromatic stacking contacts carefully; this is a high-value base-stacking case
- Cross-check the expected-contact residues and ligand atom labels against the source paper
- Consider whether the fluorophenyl F atoms participate in meaningful halogen-bond or polar interactions

## Initial MacVina Snapshot

MacVina reference-pose scoring after initial promotion:

```text
macvina-vina -9.672
aptamer      -9.946
phosphate     0.000
stacking     -0.274
metal         0.000
contact-hit   0.292
```

Top reported interaction:

```text
baseStacking Y:104:C1#11 -> Y:25:C8#542 3.46 A score -0.274
```

This confirms the case exercises the base-stacking term, but the contact labels remain first-pass until literature review.
