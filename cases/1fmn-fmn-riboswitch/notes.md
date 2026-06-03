# FMN riboswitch bound to flavin mononucleotide

Seed benchmark case `1fmn-fmn-riboswitch`.

## Source

RCSB PDB `3F4E`, crystal structure of the *Fusobacterium nucleatum* FMN riboswitch bound to flavin mononucleotide. The benchmark keeps the RNA receptor and FMN ligand from the crystallographic complex.

## Inputs

Configured path:

```text
inputs/1fmn-conf.txt
```

Local ignored inputs currently include:

- `3f4e.pdb`: downloaded source structure.
- `receptor_rna.pdb`: RNA receptor extracted from chains X and Y.
- `ligand_fmn.pdb`: crystallographic FMN ligand.
- `receptor.pdbqt`: receptor PDBQT used by MacVina calibration.
- `ligand_fmn.pdbqt`: ligand PDBQT seed pose.
- `reference_pose.pdbqt`: Vina-style output pose for reference mode 1.

Local ignored enrichment inputs also include:

- `enrich_calib/receptor.pdbqt`: receptor used for ligand-enrichment calibration.
- `enrich_calib/crystal.pdbqt`: crystallographic FMN ligand pose.
- `enrich_calib/actives.pdbqt`: active ligand set with 1 model.
- `enrich_calib/decoys.pdbqt`: ligand-decoy set with 60 models.

The active and crystal enrichment ligands are FMN with the same 31 atom layout as the reference ligand. The enrichment decoys are `UNL` ligands, not alternate FMN poses, and should not be used for same-ligand RMSD reporting.

See `enrichment.md` for enrichment-set counts, file roles, and caveats.

## Curation Notes

- Receptor role: RNA riboswitch chains X and Y.
- Ligand role: FMN hetero ligand from the bound complex.
- Reference pose mode 1 is the crystallographic FMN pose, exposed through `out = reference_pose.pdbqt` so calibration can score it as a Vina-compatible output model.
- Expected contacts are seed-level but now name the observed MacVina aptamer-specific contacts in the local PDBQT geometry: base stacking with receptor residue `Y:85` and phosphate electrostatic contacts near `Y:67`, `Y:68`, and `Y:62`.
- No binding affinity has been curated yet.
