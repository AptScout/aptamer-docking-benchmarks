# FMN riboswitch with crystallographic Mg bridge

Metal-coordination companion benchmark for `1fmn-fmn-riboswitch`.

## Source

RCSB PDB `3F4E`, crystal structure of the *Fusobacterium nucleatum* FMN riboswitch bound to flavin mononucleotide. This variant retains crystallographic Mg ion `X:304`, which is near the FMN phosphate group.

## Inputs

Configured path:

```text
inputs/1fmn-mg-conf.txt
```

Local ignored inputs currently include:

- `3f4e.pdb`: downloaded source structure.
- `receptor_mg.pdbqt`: RNA receptor plus Mg `X:304`.
- `ligand_fmn.pdbqt`: ligand PDBQT seed pose.
- `reference_pose.pdbqt`: Vina-style output pose for reference mode 1.

Detailed metal-site notes: [`metal_coordination.md`](metal_coordination.md).

## Curation Notes

- Receptor role: RNA riboswitch chains X and Y, with Mg `X:304` retained.
- Ligand role: FMN hetero ligand from the bound complex.
- Reference pose mode 1 is the crystallographic FMN pose.
- Mg `X:304` is 2.54 A from FMN `O1P` in the source PDB and should activate MacVina's `metalCoordination` term.
- No binding affinity has been curated yet.
