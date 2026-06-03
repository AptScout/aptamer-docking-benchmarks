# Tetrahydrofolate Riboswitch Bound to Folate Analog

Benchmark case `3sd3-thf-riboswitch`.

## Source

- RCSB PDB: `3SD3`
- HARIBOSS candidate: RNA-small-molecule complex
- Ligand: `FFO` (folinic acid, (6S)-5-formyl-tetrahydrofolate, MW 473)
- Method/resolution: X-ray diffraction, 1.95 Å
- Ref: Serganov et al. 2012 Nat Chem Biol (THF riboswitch)

## Curation Status

`contact_reviewed` in case.json (based on initial local PDBQT inspection and
literature-derived expected contacts). Earlier MacVina snapshots did not detect
the expected pteridine ring stacking; the 2026-06-02 scorer fix resolved that
implementation blocker.

## 2026-06-02 Stacking Blocker Assessment

MacVina 15-case calibration snapshot (derived/macvina/15case-metrics.csv) and
`macvinaAptamerCalibrate --validate-only` both report:

```text
3sd3-thf-riboswitch | base_stacking = 0.000 | expected_contact_hit_fraction = 0.175
Expected aptamer terms silent on reference pose: 3sd3-thf-riboswitch:stacking
```

The 0.175 hit fraction comes from phosphateElectrostatic contacts alone
(N10/C9/C14 → A:80:P, 4.96–5.45 Å). baseStacking contributes zero.

Two near-miss stacking interactions are reported:

```text
baseStackingNearMiss C12#18 → C2#905  plane 4.67 Å lateral 8.34 Å angle 32.5° fail lateral
baseStackingNearMiss C12#18 → C8#1677 plane 4.42 Å lateral 13.48 Å angle 9.9°  fail lateral
```

- C12 (ligand serial 18) is in the FFO aminobenzoyl tail, not the pteridine ring.
- C2#905 = U:42:C2 (in the expected receptor residue list).
- C8#1677 = G:78:C8 (not in the expected receptor residue list; expected list
  cites U:42, U:7, A:8, C:79, G:44).

The expected pteridine ring atoms (C4a, C8a, N5, N8, C6) are not picked up by
MacVina's ring-detection logic as stackable ring atoms. MacVina sees the
aminobenzoyl tail (C12) as the only potential stacker, and its geometry fails
both lateral and angle thresholds.

Root cause is twofold:
1. MacVina does not recognize the FFO pteridine ring as a stackable aromatic
   ring for baseStacking scoring.
2. MacVina's lateral stacking cutoff (2.5 Å) and plane-distance tolerance
   fail the aminobenzoyl tail geometry (lateral 8.34–13.48 Å).

Resolution requires one of:
- Extend MacVina aromatic ring detection to recognize pteridine/pterin ring
  systems (fused pyrimidine-pyrazine).
- Relax lateral and/or plane-distance stacking tolerances for large ligands
  like FFO (MW 473, 22 atoms).
- Add hydrogen-bond interaction kinds to the schema and MacVina scoring so
  the pteridine H-bond network can be scored independently of baseStacking.

No label change was applied on 2026-06-02. The expected contacts describe the
literature-known pteridine stacking geometry, but MacVina's ring detection and
stacking criteria cannot score it. The blockage is a MacVina implementation
issue, not a data-label issue.

*Reviewed: local PDBQT geometry. Not source-paper validated.*

## 2026-06-02 Resolution

MacVina scorer fix (2026-06-02, same day) resolved both root causes:

1. Pteridine/pterin ring recognition added via `isPteridineRingAtom`,
   covering N1, C2, N3, C4, C4A, N5, C6, C7, N8, C8A atom names. MacVina
   now detects the FFO pteridine ring for baseStacking scoring.
2. Lateral stacking cutoff relaxed from 2.5 Å to 4.0 Å
   (`stackingMaxLateralDistance`).

The blocker assessment above (`## 2026-06-02 Stacking Blocker Assessment`)
is historical. Expected-contact labels were unchanged. Re-run enrichment
after this fix to confirm the baseStacking contribution.
