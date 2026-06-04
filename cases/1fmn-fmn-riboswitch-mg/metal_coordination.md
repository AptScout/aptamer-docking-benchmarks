# Metal Coordination Seed

This case is the metal-coordination companion to `1fmn-fmn-riboswitch`. It keeps the crystallographic Mg ion from 3F4E so MacVina can exercise the `metalCoordination` term on an RNA-ligand system where the ligand phosphate is close to a receptor metal site.

## Local Files

The molecular inputs are local ignored files under `inputs/`.

| Path | Role | Contents |
| --- | --- | --- |
| `inputs/receptor_mg.pdbqt` | Receptor | RNA receptor plus Mg `X:304`; 1 model, 2341 atoms |
| `inputs/ligand_fmn.pdbqt` | Ligand | FMN ligand seed pose; 1 model, 31 atoms |
| `inputs/reference_pose.pdbqt` | Reference pose | Crystallographic FMN pose as Vina-style mode 1; 1 model, 31 atoms |
| `inputs/3f4e.pdb` | Source structure | RCSB PDB source file; 240651 bytes |

## Mg Site

The retained Mg atom is:

```text
HETATM 2345  MG  MG  X 304      23.171  44.324  16.675  0.00  0.00    +2.000 MG
```

Expected contact:

| Receptor residue | Ligand atom | Interaction kind | Source geometry |
| --- | --- | --- | --- |
| `X:304` | `O1P` | `metalCoordination` | 2.54 A Mg-to-O1P distance in 3F4E |

## Current MacVina Diagnostics

Current pose-level diagnostics rank the reference first for this case:

| Pose | Rank | Total score | Metal term | RMSD | Expected-contact hit fraction | Clash count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `mode:1` reference | 1 | -8.818 | -0.158 | 0.000 | 1.000 | 38 |

Top interactions currently reported:

```text
baseStacking Y:200:C4#5 -> Y:85:C8#608 3.19 A score -0.200
metalCoordination Y:200:O1P#29 -> X:304:MG#2345 2.54 A score -0.158
phosphateElectrostatic Y:200:P#28 -> X:304:MG#2345 3.45 A score -0.098
```

## Caveats

- This is a seed-level metal-contact expectation and still needs manual structural review.
- There are no metal-site decoys yet, so the case exercises the term but does not provide discriminating signal for metal-weight calibration.
- Compare this case against the plain `1fmn-fmn-riboswitch` case, but do not treat the two as independent affinity benchmarks.
