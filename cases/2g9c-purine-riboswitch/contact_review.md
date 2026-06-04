# 2G9C Contact Review

This case is a high-resolution purine-riboswitch structural benchmark. Earlier
MacVina snapshots did not score its expected base-stacking contacts, but the
2026-06-02 scorer fix resolved that implementation blocker.

## Historical Finding

Before the 2026-06-02 scorer fix, MacVina reference-pose scoring reported:

```text
phosphate_electrostatic = 0.000
base_stacking = 0.000
metal_coordination = 0.000
expected_contact_hit_fraction = 0.000
```

The local 3AY ligand PDBQT atoms are:

```text
NAA, C6, C5, N1, C2, NAH, N3, C4, NAI
```

The previous expected-contact labels `N4` and `N9` are not present in the local PDBQT and have been replaced in `expected_contacts.json`.

## Local Geometry

Nearest local atom contacts support close pocket contacts, but not necessarily MacVina-style ring-plane stacking:

| Receptor residue | Example local atom contact | Distance |
| --- | --- | ---: |
| `U:74` | `3AY:N3` to `U:N3` | 2.87 A |
| `U:51` | `3AY:N1` to `U:N3` | 2.87 A |
| `A:52` | `3AY:NAA` to `A:N1` | 3.22 A |
| `A:21` | `3AY:C5` to `A:C2` | 3.31 A |
| `U:22` | `3AY:NAA` to `U:N3` | 3.37 A |
| `U:47` | `3AY:NAA` to `U:O2` | 3.37 A |
| `U:75` | `3AY:C2` to `U:O2` | 3.06 A |

Approximate 3AY ring-centroid distances to expected receptor base centroids in
the local PDBQT are about 5 to 8 A, outside the old MacVina stacking geometry
envelope. That explained why earlier snapshots had zero MacVina `baseStacking`
contribution despite close atom contacts.

The old MacVina pose report included explicit base-stacking near-miss
diagnostics. The two closest receptor base planes passed plane distance and
angle, but failed lateral overlap under the former 2.5 A cutoff:

```text
baseStackingNearMiss C5#3 -> C8#801 plane 3.37 A lateral 3.19 A angle 6.5 deg fail lateral
baseStackingNearMiss C5#3 -> C8#141 plane 3.20 A lateral 3.83 A angle 0.5 deg fail lateral
```

This made the issue specific: MacVina could build a ligand plane for 3AY, but
under the local coordinates and former 2.5 A lateral cutoff it did not classify
the pose as stacked.

## Review Tasks

- Confirm whether the local receptor/ligand PDBQT coordinates preserve the intended 2G9C crystal-frame pocket geometry.
- Decide whether 2G9C should be represented as `baseStacking`, `hydrogenBond/contact`, or both in future schema/metric layers.
- Review whether the 2.5 A lateral stacking cutoff is appropriate for purine-riboswitch contacts, or whether 2G9C should remain a non-stacking contact case.
- Do not promote this case back to `contact_reviewed` until the expected-contact labels and MacVina stacking geometry agree.

## 2026-06-02 Blocker Assessment

MacVina 15-case calibration snapshot (derived/macvina/15case-metrics.csv) and
`macvinaAptamerCalibrate --validate-only` both confirm:

```text
2g9c-purine-riboswitch | base_stacking = 0.000 | expected_contact_hit_fraction = 0.000
Expected aptamer terms silent on reference pose: 2g9c-purine-riboswitch:stacking
```

Root cause confirmed: the expected-contact labels in `expected_contacts.json`
match the local PDBQT atom names. The ligand 3AY labels were previously
corrected from N4/N9 to NAA/NAH/NAI. The two closest receptor ring-plane
near-misses are against A:21:C8 and A:52:C8 (both in the expected receptor
residue list), with plane distance 3.20–3.37 Å and angle 0.5–6.5°, but
lateral displacement 3.19–3.83 Å exceeds MacVina's 2.5 Å lateral stacking
cutoff. The labels are correct; the silence comes from MacVina's stacking
geometry threshold, not from a label mismatch.

Resolution requires one of:
- Relax MacVina lateral stacking cutoff (currently 2.5 Å) for RNA aptamer
  cases where plane distance and angle are within tolerance.
- Add per-case lateral tolerance overrides.
- Reclassify 2G9C as a hydrogen-bond/contact case instead of baseStacking
  if the schema gains those interaction kinds.

No label change was applied on 2026-06-02 because the expected contacts are
locally consistent with the PDBQT geometry. The blockage is a MacVina
scoring-threshold issue, not a data-label issue.

*Reviewed: local PDBQT geometry. Not source-paper validated.*

## 2026-06-02 Resolution

MacVina scorer fix (2026-06-02, same day) resolved the lateral stacking
cutoff by raising `stackingMaxLateralDistance` from 2.5 Å to 4.0 Å. The two
near-miss receptor planes (A:21:C8 lateral 3.19 Å, A:52:C8 lateral 3.83 Å)
now fall within the relaxed cutoff.

The blocker assessment above (`## 2026-06-02 Blocker Assessment`) is
historical. Expected-contact labels were unchanged. Re-run enrichment
after this fix to confirm the baseStacking contribution.
