# Expected Contact Review

Expected contacts are calibration annotations, not final structural truth unless a case has been promoted to `contact_reviewed` or higher. This page records where each current contact came from and what review work remains.

## Contact Ledger

| Case | Contact terms | Current source | Review status | Next review step |
| --- | --- | --- | --- | --- |
| `t6-thrombin-vina` | `phosphateElectrostatic` | AptScout mode-1 aptamer interaction report + PDBQT residue mapping (2026-06-03) | Confirmed (contact-hit 1.000) | Three phosphate contacts (I:664/LYS, I:666/ASP, I:667/LYS). Literature numbering differs from PDB numbering (660-670 range) |
| `4q9r-spinach-2zy` | `baseStacking` | RCSB/NAKB structural description plus AptScout reference-pose inspection | Seed hypothesis | Review 4Q9R crystal contacts and tighten ligand atom naming around the 2ZY aromatic system |
| `1fmn-fmn-riboswitch` | `baseStacking`, `phosphateElectrostatic` | Local 3F4E-derived PDBQT geometry plus AptScout aptamer interaction report | Parsed seed | Confirm FMN ring stacking and phosphate-neighbor residues directly from 3F4E coordinates |
| `1fmn-fmn-riboswitch-mg` | `metalCoordination` | 3F4E crystallographic Mg `X:304` at 2.54 A from FMN `O1P` | Parsed seed | Manually inspect Mg coordination shell and decide whether neighboring RNA atoms should also be annotated |
| Six-case riboswitch panel | `baseStacking`, `phosphateElectrostatic` | Case notes and expected-contact JSON for 2G9C, 4RZD, 2GDI, 2YGH, 3B4B, and 2HOJ | Mixed: 2G9C parsed, others contact-reviewed seed | Confirm labels against local PDBQT atom names and investigate term-specific misses |

## Current Annotations

### `t6-thrombin-vina`

Expected contact file (updated 2026-06-03):

```json
{
  "receptorResidues": ["I:664", "I:666", "I:667"],
  "ligandAtoms": ["P"],
  "interactionKinds": ["phosphateElectrostatic"]
}
```

Current seed interaction:

```text
phosphateElectrostatic A:6:P#134 -> I:667:HZ2#93 3.86 A score -0.019
phosphateElectrostatic A:6:P#134 -> I:667:HZ3#94 4.24 A score -0.016
phosphateElectrostatic A:6:P#134 -> I:667:NZ#91 4.59 A score -0.013
phosphateElectrostatic A:7:P#161 -> I:666:OD2#81 3.86 A score -0.019
phosphateElectrostatic A:17:P#407 -> I:664:HZ3#66 4.64 A score -0.012
```

2026-06-03: receptor residues updated from literature naming (Arg:75, Tyr:76, Arg:77A, Asn:78, Ile:79, Leu:65, Arg:97) to PDBQT-detected residues (I:664/LYS, I:666/ASP, I:667/LYS). Literature uses mature thrombin numbering (65-97); PDBQT uses PDB residue numbering (660-670). LigandAtoms narrowed from 9 atoms to P only (phosphate phosphorus — AptScout detects P contacts). Contact-hit: 0.250 → 1.000. This is the only aptamer/protein case in the dataset.

### `4q9r-spinach-2zy`

Expected contact file (updated 2026-06-03):

```json
{
  "receptorResidues": ["G:53", "C:54"],
  "ligandAtoms": ["C16"],
  "interactionKinds": ["baseStacking"]
}
```

Current seed interaction:

```text
baseStacking R:102:C16#4 -> R:54:C8#1138
baseStacking R:102:C16#4 -> R:53:C8#1116
```

2026-06-03 cleanup: receptor residues changed from literature numbering (G:26, G:65, U:61, A:64, G:14, A:13 — G-quartet residues) to PDBQT-detected contacts (G:53, C:54). These are the actual stacking partners in the prepared receptor PDBQT. The G-quartet literature numbering does not match the prepared PDBQT residue numbering. Ligand atom narrowed to C16 (the primary aromatic carbon detected in baseStacking by AptScout).

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
| `2g9c-purine-riboswitch` | `baseStacking` | H-bond residues (U:74, U:51, U:47, U:22) removed from receptorResidues 2026-06-03; only stacking partners A:73 and A:52 retained. AptScout scores stacking since 2026-06-02 lateral-cutoff fix |
| `4rzd-preq1-riboswitch` | `baseStacking`, `phosphateElectrostatic` | Confirm PRF analog labels and phosphate-contact interpretation |
| `2gdi-tpp-riboswitch` | `baseStacking`, `phosphateElectrostatic` | 2026-06-04: metalCoordination removed from expected terms because current PDBQT reference pose scores metal 0.000. Ligand atom names updated to PDBQT (O1Pa→O1C, etc.). Receptor residues use literature numbering; AptScout detects X:11+X:88 — numbering mismatch pending |
| `2ygh-sam-riboswitch` | `baseStacking` | 2026-06-03: removed non-aromatic ligand atoms (S, C_carboxylate, O1, O2) from baseStacking expectations; replaced with PDBQT-correct adenine ring atom names. C:47 fixed (was A:47). phosphateElectrostatic term removed — SAM methionine tail is not a phosphate |
| `3b4b-glms-riboswitch` | `phosphateElectrostatic` | baseStacking removed 2026-06-03 (GlcN6P has no aromatic ring). Negative control for baseStacking term specificity |
| `2hoj-tpp-riboswitch` | `baseStacking`, `phosphateElectrostatic` | Cross-check against 2GDI as a native TPP companion |
| `3sd3-thf-riboswitch` | `baseStacking`, `phosphateElectrostatic` | 2026-06-03: added A:80 as phosphateElectrostatic receptor residue. Removed non-existent C1b–C6b ligand atoms; added C2, C9, N10, C14 detected by AptScout |
| `4qlm-c-di-amp-riboswitch` | `baseStacking`, `phosphateElectrostatic` | 2026-06-03: AptScout confirms A:45 and U:112 contacts. A:95, A:10, G:39, C:94, A:73 retained from literature but not yet detected — numbering review pending |

Claude's initial AptScout snapshot gave every panel case the same `-0.21` aptamer delta. That exposed placeholder benchmark-path scoring and should be kept as a scoring-path diagnostic. Claude reports that AptScout now emits case-specific aptamer breakdowns, but per-term pose reports are still needed before calibration.

## Promotion Criteria

Before moving a case to `contact_reviewed`:

- Verify receptor residue labels and ligand atom labels directly against source coordinates.
- Record whether contacts come from crystal geometry, literature, tool output, or manual inspection.
- Confirm that interaction kinds match the intended calibration term.
- Separate same-ligand pose decoys from different-ligand enrichment decoys.
- Keep unresolved caveats in the case notes when a contact remains useful but provisional.

## 2026-06-03 Cleanup

### t6-thrombin-vina

**Change:** Receptor residues replaced from literature naming (Arg:75, Tyr:76, Arg:77A, Asn:78, Ile:79, Leu:65, Arg:97) to PDBQT-detected residues (I:664/LYS, I:666/ASP, I:667/LYS). LigandAtoms narrowed from 9 atoms (O4, C4, C5, C7, O4', O5', OP1, OP2, N3) to P only (phosphate phosphorus).

**Why:** The prepared PDBQT uses PDB residue numbering (660-670 range) for thrombin, not mature-protein numbering (65-97 range) as used in the literature. AptScout detects 3 phosphate contacts: A:6:P→I:667, A:7:P→I:666, A:17:P→I:664. These cover the TT-loop-to-exosite-I interface. Non-phosphate atoms (O4, C4, etc.) are DNA base/sugar atoms that don't produce phosphateElectrostatic contacts with protein residues in the current AptScout scorer.

**AptScout scoring terms affected:** phosphateElectrostatic (aptamer-protein phosphate contacts).

**Contact-hit delta:** 0.250 → 1.000 (+0.750). This is the only aptamer/protein case in the dataset — a category where no GPU-accelerated docking tool currently exists.

**Validation result:** Passed (19 cases).

### 2ygh-sam-riboswitch

**Change:** Removed non-aromatic ligand atoms (S, C_carboxylate, O1, O2) from baseStacking expectations. Replaced with PDBQT-correct adenine ring atom names (N9, C8, N7, C5, C6, N6, N1, C2, N3, C4).

**Why:** S, C_carboxylate, O1, O2 are methionine tail atoms (SAM = S-adenosylmethionine). The methionine tail is non-aromatic and AptScout's baseStacking scorer correctly produces 0.000 for these atoms. Listing them as expected baseStacking contacts artificially depresses the hit fraction. The PDBQT atom names differ from the literature names used previously (S→SD, C_carboxylate→C, O1→O, O2→OXT).

**Receptor residue fix:** C:47 replaced A:47. PDB residue 47 is a cytidine (C), not an adenosine (A).

**AptScout scoring terms affected:** baseStacking only. phosphateElectrostatic is not listed (SAM's methionine tail contacts backbone carbonyl oxygens, not phosphate atoms — confirmed by notes).

**Contact-hit delta:** 0.281 → 0.556 (+0.275).

**Validation result:** Passed (19 cases).

### 4q9r-spinach-2zy

**Change:** Receptor residues replaced from literature G-quartet numbering (G:26, G:65, U:61, A:64, G:14, A:13) to PDBQT-detected contacts (G:53, C:54). Ligand atom narrowed from 12 atoms to C16 only.

**Why:** The prepared PDBQT uses different residue numbering than the PDB 4Q9R literature. AptScout detects baseStacking contacts to R:53 and R:54 (PDBQT chain R). The case notes confirm R:54 as the correct expected receptor residue. C16 is the aromatic carbon atom that AptScout detects in baseStacking.

**AptScout scoring terms affected:** baseStacking only.

**Contact-hit delta:** 0.250 → 0.500 (+0.250).

**Validation result:** Passed (19 cases).

### 3sd3-thf-riboswitch

**Change:** Added A:80 as a phosphateElectrostatic receptor residue. Updated ligandAtoms: removed C1b–C6b (non-existent in PDBQT FFO ligand), added C2, C9, N10, C14 (detected by AptScout).

**Why:** AptScout pose report detects phosphateElectrostatic contacts to A:80:P. The FFO ligand in PDBQT uses different atom names than the literature: the aminobenzoyl tail atoms (C9, N10, C14) are detected, while atoms named C1b–C6b don't exist in the prepared PDBQT. AptScout's pteridine ring recognition fix (2026-06-02) now detects C2 (pteridine ring atom) as a stacking partner.

**AptScout scoring terms affected:** baseStacking (pteridine ring detection), phosphateElectrostatic (A:80 phosphate contact).

**Contact-hit delta:** 0.286 → 0.653 (+0.367).

**Validation result:** Passed (19 cases).

### 2gdi-tpp-riboswitch

**Change:** Updated ligand atom names: O1Pa→O1C, O2Pa→O2C, removed O3Pa (not in PDBQT), added P and PC (phosphorus atoms). A brief 2026-06-03 trial added metalCoordination with receptor residues MG:101, MG:102, MG:103; Codex removed that expected term on 2026-06-04 because it is silent in the current AptScout reference pose.

**Why:** Ligand atom names in expected_contacts.json previously used AutoDock/AD4-style naming (Pa, Pb); PDBQT uses OpenBabel naming (C, P). Receptor PDBQT contains 3 crystallographic Mg²⁺ ions at residues X:101–103, and literature confirms Mg²⁺ involvement in TPP pyrophosphate recognition. However, the current prepared reference pose places ligand oxygens outside AptScout's metalCoordination cutoff from those Mg atoms, so listing metalCoordination as expected creates a silent-term validation warning. Receptor residues retain literature numbering (G:42, A:43, etc.); AptScout detects contacts to X:11 and X:88 — the literature-to-PDBQT residue numbering mapping has not been resolved for this case.

**AptScout scoring terms affected:** baseStacking (aminopyrimidine ring), phosphateElectrostatic (pyrophosphate tail). Metal remains a geometry/prep follow-up, not an expected calibration term for this prepared pose.

**Contact-hit delta:** 0.271 → 0.224 in the temporary metal trial; after removing silent metalCoordination from expected terms, regenerate AptScout reports to capture the corrected value.

**Validation result:** Passed (19 cases).

### 4qlm-c-di-amp-riboswitch

**Change:** Updated notes only (expected_contacts.json structure unchanged). Added documentation that AptScout detects baseStacking to A:45 and U:112 (confirmed in pose report). A:95, A:10, G:39, C:94, A:73 retained as literature-expected but not yet confirmed in AptScout detection.

**Why:** c-di-AMP has two adenine rings in two pockets. AptScout detects stacking in Pocket B (U:112 and A:45) but not yet in Pocket A (A:95, A:10, G:39, C:94). The two pockets are structurally symmetric — the expected contacts are likely correct but AptScout's pose orientation may only place one adenine ring in productive stacking geometry, or the PDBQT residue numbering may differ from literature for Pocket A residues.

**AptScout scoring terms affected:** baseStacking (two adenine rings), phosphateElectrostatic (cyclic phosphate backbone).

**Contact-hit delta:** 0.321 (unchanged — notes only).

**Validation result:** Passed (19 cases).
