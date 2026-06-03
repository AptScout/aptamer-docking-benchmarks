# Expected Contact Review

Expected contacts are calibration annotations, not final structural truth unless a case has been promoted to `contact_reviewed` or higher. This page records where each current contact came from and what review work remains.

## Contact Ledger

| Case | Contact terms | Current source | Review status | Next review step |
| --- | --- | --- | --- | --- |
| `t6-thrombin-vina` | `phosphateElectrostatic` | MacVina mode-1 aptamer interaction report for local T6 QuickVina files | Seed hypothesis | Confirm aptamer-protein residue mapping and whether `I:667` is the intended phosphate-contact partner |
| `4q9r-spinach-2zy` | `baseStacking` | RCSB/NAKB structural description plus MacVina reference-pose inspection | Seed hypothesis | Review 4Q9R crystal contacts and tighten ligand atom naming around the 2ZY aromatic system |
| `1fmn-fmn-riboswitch` | `baseStacking`, `phosphateElectrostatic` | Local 3F4E-derived PDBQT geometry plus MacVina aptamer interaction report | Parsed seed | Confirm FMN ring stacking and phosphate-neighbor residues directly from 3F4E coordinates |
| `1fmn-fmn-riboswitch-mg` | `metalCoordination` | 3F4E crystallographic Mg `X:304` at 2.54 A from FMN `O1P` | Parsed seed | Manually inspect Mg coordination shell and decide whether neighboring RNA atoms should also be annotated |
| Six-case riboswitch panel | `baseStacking`, `phosphateElectrostatic` | Case notes and expected-contact JSON for 2G9C, 4RZD, 2GDI, 2YGH, 3B4B, and 2HOJ | Mixed: 2G9C parsed, others contact-reviewed seed | Confirm labels against local PDBQT atom names and investigate term-specific misses |

## Current Annotations

### `t6-thrombin-vina`

Expected contact file:

```json
{
  "receptorResidues": ["I:667"],
  "ligandAtoms": ["P_134"],
  "interactionKinds": ["phosphateElectrostatic"]
}
```

Current seed interaction:

```text
phosphateElectrostatic A:6:P#134 -> I:667:HZ2#93
phosphateElectrostatic A:6:P#134 -> I:667:HZ3#94
phosphateElectrostatic A:6:P#134 -> I:667:NZ#91
```

Use this as a loader and scoring-regression contact until the aptamer-protein structural annotation is reviewed.

### `4q9r-spinach-2zy`

Expected contact file:

```json
{
  "receptorResidues": ["R:54"],
  "ligandAtoms": ["C16_4"],
  "interactionKinds": ["baseStacking"]
}
```

Current seed interaction:

```text
baseStacking R:102:C16#4 -> R:54:C8#1138
```

This is the key base-stacking case with same-ligand pose decoys. Contact review should preserve its role as a discriminating pose-ranking benchmark while tightening atom/residue labels against the crystal structure.

### `1fmn-fmn-riboswitch`

Expected contact file:

```json
{
  "receptorResidues": ["Y:85", "Y:67", "Y:68", "Y:62"],
  "ligandAtoms": ["C4", "P"],
  "interactionKinds": ["baseStacking", "phosphateElectrostatic"]
}
```

Current seed interpretation:

- FMN ring atom `C4` stacks with receptor residue `Y:85`.
- FMN phosphate atom `P` contributes phosphate-electrostatic contacts near residues `Y:67`, `Y:68`, and `Y:62`.

This case is useful because it combines two aptamer-aware terms in one RNA-ligand geometry. The enrichment decoys are different ligands, so contact review should keep pose-contact annotation separate from ligand-enrichment use.

### `1fmn-fmn-riboswitch-mg`

Expected contact file:

```json
{
  "receptorResidues": ["X:304"],
  "ligandAtoms": ["O1P"],
  "interactionKinds": ["metalCoordination"]
}
```

Current seed interaction:

```text
metalCoordination Y:200:O1P#29 -> X:304:MG#2345 2.54 A score -0.158
```

This is the current metal-coordination smoke test. It should be compared with the plain 1FMN case to understand the scoring effect of retaining Mg, but it still needs metal-site decoys or additional cases before it can calibrate metal weights by itself.

### Riboswitch Panel

The expanded riboswitch panel adds six RNA-ligand expected-contact files:

| Case | Current terms | Contact-review caution |
| --- | --- | --- |
| `2g9c-purine-riboswitch` | `baseStacking` | H-bond residues (U:74, U:51, U:47, U:22) removed from receptorResidues 2026-06-03; only stacking partners A:73 and A:52 retained. MacVina scores stacking since 2026-06-02 lateral-cutoff fix |
| `4rzd-preq1-riboswitch` | `baseStacking`, `phosphateElectrostatic` | Confirm PRF analog labels and phosphate-contact interpretation |
| `2gdi-tpp-riboswitch` | `baseStacking`, `phosphateElectrostatic` | Distinguish direct phosphate scoring from Mg-mediated TPP contacts |
| `2ygh-sam-riboswitch` | `baseStacking`, `phosphateElectrostatic` | Resolve charged-tail/backbone contact labels |
| `3b4b-glms-riboswitch` | `phosphateElectrostatic` | baseStacking removed 2026-06-03 (GlcN6P has no aromatic ring). Negative control for baseStacking term specificity |
| `2hoj-tpp-riboswitch` | `baseStacking`, `phosphateElectrostatic` | Cross-check against 2GDI as a native TPP companion |

Claude's initial MacDock snapshot gave every panel case the same `-0.21` aptamer delta. That exposed placeholder benchmark-path scoring and should be kept as a scoring-path diagnostic. Claude reports that MacDock now emits case-specific aptamer breakdowns, but per-term pose reports are still needed before calibration.

## Promotion Criteria

Before moving a case to `contact_reviewed`:

- Verify receptor residue labels and ligand atom labels directly against source coordinates.
- Record whether contacts come from crystal geometry, literature, tool output, or manual inspection.
- Confirm that interaction kinds match the intended calibration term.
- Separate same-ligand pose decoys from different-ligand enrichment decoys.
- Keep unresolved caveats in the case notes when a contact remains useful but provisional.
