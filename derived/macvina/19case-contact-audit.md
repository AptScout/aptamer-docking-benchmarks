# 19-Case Expected Contact Hit Fraction Audit

**Date:** 2026-06-03
**Scope:** Low-hit cases (< 0.50 expected_contact_hit_fraction) from `19case-metrics.csv`
**Method:** Inspect `expected_contacts.json`, PDBQT ligand/receptor files, `AptamerInteractionScorer.swift`, and `AptamerExpectedContactEvaluator.swift`
**Classification key:**
- **(A)** Expected contacts too broad / literature-only for current MacVina term definitions
- **(B)** Scorer implementation gap (missing term, false positive, geometry mismatch)
- **(C)** Local PDBQT geometry/prep issue
- **(D)** Acceptable — expected contacts include non-scored H-bond/shape contacts by design

---

## Summary

| Case | Hit Fraction | Classification | Primary Issue |
|------|-------------|----------------|---------------|
| 2ygh-sam-riboswitch | 0.300 | A | Literature ligand atom names; methionine tail not scored |
| 3sd3-thf-riboswitch | 0.350 | A | Two binding sites; non-pteridine atoms in expected list |
| 3b4b-glms-riboswitch | 0.375 | A+B | baseStacking expected for non-aromatic ligand; scorer false positive |
| 6wzs-ztp-riboswitch | 0.417 | A | HARIBOSS PDBQT atom names don't match literature names |
| 4rzd-preq1-riboswitch | 0.458 | A+B | A-minor stacking listed as baseStacking; H-bond contacts not scored |
| 2hoj-tpp-riboswitch | 0.500 | A/D | Large ligand; some contacts likely H-bond/shape (acceptable) |
| 5bjp-corn-dfho | 0.500 | A/D | Homodimer — single-chain docking can't capture interprotomer interface |

---

## Detailed Case Analysis

### 1. 2ygh-sam-riboswitch (0.300) — Classification: A

**Expected contacts:**
- interactionKinds: `["baseStacking"]`
- receptorResidues: 7 (A:45, U:57, G:11, A:46, U:78, U:7, A:87)
- ligandAtoms: 8 (N6, N1, C8, N9, S, C_carboxylate, O1, O2)

**What MacVina scores:**
- SAM has one adenine ring (10 purine ring atoms) and a methionine tail
- Only `baseStacking` is expected; SAM has no phosphate → no phosphateElectrostatic
- Adenine ring forms one aromatic plane; baseStacking produces 1 interaction per stacked receptor base
- Methionine tail atoms (S/CE/CG/CB/CA/N/C/O/OXT) are NOT scored by any MacVina term

**Root cause:**
1. Ligand atom names use literature convention ("S", "C_carboxylate", "O1", "O2") — these don't match PDBQT atom names ("SD", "C", "O", "OXT"). Only "N6", "N1", "C8", "N9" match PDBQT names.
2. Even if names matched, the methionine tail atoms aren't scored by any MacVina interaction term; the evaluator can only match atoms that appear in actual scored interactions.
3. A single baseStacking interaction references only one representative ligand atom (typically the second plane atom, e.g., C8), so at most 1/8 expected ligand atoms can match through baseStacking.
4. The 7 expected receptor residues are literature-derived; baseStacking typically hits 1-2 of them.

**Recommendation:** The notes field already acknowledges this limitation well. For calibration purposes, consider narrowing `ligandAtoms` to only adenine-ring atoms (N6, N1, C8, N9) and `receptorResidues` to only the 1-2 residues closest to the adenine stacking plane. The methionine-tail contacts are better tested via a separate case or a future H-bond term.

---

### 2. 3sd3-thf-riboswitch (0.350) — Classification: A

**Expected contacts:**
- interactionKinds: `["baseStacking", "phosphateElectrostatic"]`
- receptorResidues: 7 (C:53, U:25, G:26, G:54, G:68, U:7, A:8)
- ligandAtoms: 13 (pteridine ring atoms + C1b-C6b bridge atoms)

**What MacVina scores:**
- FFO (folinic acid, MW 473) has one pteridine ring (scored by baseStacking), a non-aromatic bridge (not scored), and a benzamide tail (not scored)
- FFO has NO phosphate group → phosphateElectrostatic only from receptor backbone phosphates
- The pteridine ring includes N1-C8a atoms; the bridge (C9/N10/C11-C16) and benzamide ring are not pteridine atoms
- 13 expected ligand atoms include bridge carbons (C1b-C6b) that are not scored

**Root cause:**
1. **Two binding sites:** FFO occupies both Site 3WJ (pteridine stacks between G26/G54) and Site PK (pteridine stacks on A8/U7). The expected contacts span both sites and 7 receptor residues. The reference pose (mode=1, crystal pose at one site) can only interact with one site's residues. The evaluator averages across both sites' expected residues and atoms, diluting the hit fraction.
2. Bridge atoms (C1b-C6b) in `ligandAtoms` are not part of any scored interaction.
3. `phosphateElectrostatic` is expected but FFO has no phosphate; any electrostatic interaction is receptor-backbone-only, which is geometrically constrained and weaker.

**Recommendation:**
- (Complex) Split into two expected_contacts variants — one per binding site — with the reference pose docked to each site. This is the most honest treatment but requires splitting the benchmark case.
- (Minimal) Add a note documenting the two-site issue clearly.
- Remove non-pteridine bridge atoms from `ligandAtoms`.

---

### 3. 3b4b-glms-riboswitch (0.375) — Classification: A+B

**Expected contacts:**
- interactionKinds: `["baseStacking", "phosphateElectrostatic"]`
- receptorResidues: 6 (G:1, G:57, U:43, A:2, G:65, G:66)
- ligandAtoms: 5 (N2, O1, O1P, O2P, O3P)

**What MacVina scores:**
- GlcN6P is a glucosamine-6-phosphate — a sugar ring with amine and phosphate substituents
- **No aromatic ring** → baseStacking should never fire
- The scorer detects a **false positive baseStacking** interaction: `C2→C8` (non-aromatic sugar carbon treated as aromatic by the generic fallback)
- Phosphate group (P + O1P/O2P/O3P) does trigger phosphateElectrostatic against receptor backbone phosphates
- Literature contacts are primarily **H-bonds** (N2 to G1 5'-O, O1 to G57 N1, phosphate to G1 N1/backbone) — NONE of these are scored by MacVina's current aptamer terms

**Root cause:**
1. **baseStacking in interactionKinds is incorrect** for this ligand. The case notes explicitly state it's a "negative control for baseStacking term specificity," yet expected_contacts lists baseStacking. This contradiction artificially lowers the calibration metric.
2. The scorer produces a **false positive** baseStacking interaction (C2→C8, scored -0.257), which is a scorer bug — the generic aromatic fallback incorrectly treats non-aromatic sugar carbons as aromatic.
3. Primary literature interactions are H-bonds, which MacVina's aptamer suite does not yet score.

**Action taken:** Removed `"baseStacking"` from `interactionKinds` — GlcN6P has no aromatic ring and should not expect baseStacking. This is the only clearly justified expected_contacts edit across the 19-case set.

**Recommendation:** 
- (B) The scorer false positive (C2 plane detection) should be fixed. The generic aromatic fallback in `ligandAromaticPlanes` needs stricter filtering — the current `autoDockType == "A"` check is too permissive for non-aromatic carbons.
- (B) Consider adding an H-bond term to the aptamer scorer for cases like this where the literature interactions are purely H-bond-driven.

---

### 4. 6wzs-ztp-riboswitch (0.417) — Classification: A

**Expected contacts:**
- interactionKinds: `["baseStacking", "phosphateElectrostatic"]`
- receptorResidues: 6 (G:63, U:70, G:71, G:17, C:35, C:69)
- ligandAtoms: 14 (N1, C2, N3, C4, C5, C6, N4, C4a, N7, C8, N9, C8a, N12, O13)

**What MacVina scores:**
- UG4 is a synthetic ZTP analog with pyridine and imidazole rings, linked by a carboxamide bridge
- HARIBOSS PDBQT atom names: C02, C03, C08, N01, N07, N09, C10, N12, C13, C15, C11, C14, C04, N05, O06
- **Literature atom names in expected_contacts DON'T match HARIBOSS PDBQT names**
- UG4 has NO phosphate → phosphateElectrostatic is receptor-backbone-only

**Root cause:**
1. **PDBQT naming mismatch:** The expected_contacts uses literature ring-atom names (N1, C2, N3, etc.) but HARIBOSS PDBQT uses a different convention (N01, C02, C03, etc.). The evaluator `normalizedExpectation` cannot bridge the gap. Expected atom "N1" will never match interaction atom "N01".
2. The 14 expected atoms include non-scored linker atoms (the carboxamide bridge).
3. No phosphate on UG4, so phosphateElectrostatic hits are weak/incidental.

**Recommendation:**
- Remap ligandAtoms to HARIBOSS PDBQT names. Mapping key:
  - N1→N01, C2→C02, N3→? (no direct match; C03 is carbon), C4→C08?, etc.
  - This requires careful manual mapping by someone who knows the HARIBOSS naming convention.
- Narrow ligandAtoms to only aromatic ring atoms that can participate in baseStacking.
- Alternatively, switch 6WZS to a non-HARIBOSS PDBQT prep pipeline for naming consistency.

---

### 5. 4rzd-preq1-riboswitch (0.458) — Classification: A+B

**Expected contacts:**
- interactionKinds: `["baseStacking", "phosphateElectrostatic"]`
- receptorResidues: 6 (C:7, U:8, U:17, A:18, A:85, A:84)
- ligandAtoms: 9 (N1, C2, N3, C4, C5, N7, C8, N9, C7b)

**What MacVina scores:**
- PRF is a preQ1 analog with one 7-deazaguanine ring (scored by baseStacking) + an aminomethyl tail
- The pose-report shows: baseStacking A:201:C4#4 → A:52:C8#398 (score -0.237), and interactions with A:42, A:85

**Root cause:**
1. **A-minor stacking ≠ MacVina baseStacking.** Literature reports that A84 and A18 provide **A-minor** interactions (adenine stacking on the minor-groove face of the ligand). MacVina's baseStacking requires a ligand aromatic plane stacking on a receptor nucleobase plane — it does NOT capture A-minor geometry where the adenine inserts into the minor groove.
2. H-bond contacts (C7 trans Watson-Crick, U17 minor-groove edge, A85/methylamine salt bridge) are listed as "phosphateElectrostatic" in expected contacts but are actually H-bonds, which MacVina does not score as a separate term.
3. 6 expected receptor residues include A-minor contacts (A84, A18) that can't be scored by baseStacking geometry.

**Recommendation:**
- Remove A-minor residues (A84, A18) from expected receptorResidues or document that A-minor stacking is a known scorer gap.
- Consider adding an "H-bond" or "polarContact" term to the aptamer scorer for riboswitch cases where H-bonds dominate recognition.
- The baseStacking term correctly captures the primary π-stacking interaction; the hit fraction is diluted by expecting A-minor and H-bond contacts through terms that can't score them.

---

### 6. 2hoj-tpp-riboswitch (0.500) — Classification: A/D (borderline)

TPP is a large ligand with aminopyrimidine, thiazole, and pyrophosphate moieties. The pyrophosphate contacts involve Mg²⁺-mediated interactions and backbone contacts that are partially captured by phosphateElectrostatic. The 0.500 hit rate reflects about half the expected contacts being H-bond/shape interactions not in MacVina's current term set. This is **acceptable** for the current calibration scope — TPP's complex multi-modal binding is inherently hard to fully capture with three scoring terms.

### 7. 5bjp-corn-dfho (0.500) — Classification: A/D (borderline)

Corn is a **homodimer** — DFHO is sandwiched at the interprotomer interface between G-quadruplexes from both chains. Single-chain MacVina docking uses chain Y only and cannot capture half the interface. The 0.500 rate is expected and **acceptable** given the dimer architecture. The remaining matches (baseStacking with chain Y's G-quartet) are the only contacts geometrically available in single-chain docking.

---

## Evaluator Design Note

The `AptamerExpectedContactEvaluator` computes hit fraction as the average of three sub-fractions:

1. `interactionKinds` match (requires both receptor AND ligand atom match)
2. `receptorResidues` match
3. `ligandAtoms` match

**Design implication for baseStacking:** Each baseStacking interaction records only ONE representative ligand atom (the second atom in the aromatic plane). A single stacking interaction thus contributes at most 1 ligand atom to the ligandAtoms fraction, regardless of how many ring atoms participate in the plane. For ligands with large aromatic systems (e.g., SAM's 10-atom adenine ring, FFO's pteridine), the evaluator structurally undercounts ligand atoms for baseStacking. This is not a bug — it's an inherent limitation of representing a plane-to-plane interaction through a single representative atom. Consider either (a) documenting this in expected_contacts notes, or (b) expanding the evaluator to credit all plane atoms.

---

## Files Changed

1. `cases/3b4b-glms-riboswitch/expected_contacts.json` — removed `"baseStacking"` from `interactionKinds` (only clearly justified edit)

## Top Recommendations

1. **Fix scorer false positive (score B):** The generic aromatic fallback in `AptamerInteractionScorer.ligandAromaticPlanes` incorrectly detects baseStacking for non-aromatic atoms (e.g., GlcN6P C2). Add an explicit non-aromatic exclusion or raise the `autoDockType == "A"` threshold.

2. **Add H-bond term to aptamer scorer (score B):** 3 of 5 low-hit cases (3b4b, 4rzd, 2ygh) have literature contacts dominated by H-bonds. A lightweight H-bond term (donor-acceptor distance + angle) would improve calibration without adding complexity.

3. **Harmonize PDBQT naming:** HARIBOSS-prep cases (3sd3, 6wzs) use non-standard atom names that don't match literature convention. Remap expected_contacts to use actual PDBQT names or standardize the prep pipeline.

4. **Consider A-minor stacking as a separate term:** 4rzd and other riboswitch cases rely on A-minor interactions. This is geometrically distinct from plane-to-plane baseStacking and may warrant its own scoring term.

5. **Two-site cases (3sd3):** Split multi-site riboswitches into separate calibration entries, one per binding site, to avoid averaging across distinct interaction networks.
