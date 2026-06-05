# Affinity Status

This dataset currently supports parser validation, pose scoring, expected-contact diagnostics, and early aptamer-aware calibration. It does not yet contain reviewed experimental binding affinities.

## Affinity Ledger

| Case | Affinity-like value in metadata | Meaning | Review status | Use in calibration |
| --- | ---: | --- | --- | --- |
| `t6-thrombin-vina` | -17.2 kcal/mol | Best QuickVina output affinity from the local legacy run | Docking reference only | Use for Vina-output compatibility checks, not experimental affinity fitting |
| `4q9r-spinach-2zy` | None | No affinity source curated | Not curated | Use for structural/contact and same-ligand pose-decoy calibration |
| `1fmn-fmn-riboswitch` | None | No affinity source curated | Not curated | Use for structural/contact specificity and ligand-enrichment experiments |
| `1fmn-fmn-riboswitch-mg` | None | No affinity source curated | Not curated | Use as metal-term smoke test and comparison with the plain FMN case |
| Six-case riboswitch panel | None | No affinity source curated | Not curated | Use for structural/contact breadth and aptamer-term specificity checks |

## Interpretation Rules

- `expectedBestAffinityKcalMol` may describe a docking reference score when a case comes from existing Vina/QuickVina output.
- A docking reference score must not be treated as experimental affinity.
- Cases with `affinitySource: "not curated"` should not contribute to experimental affinity regression or model-selection objectives.
- A case should not move to `affinity_reviewed` until the source, assay type, units, and caveats are recorded.

## Current Gaps

- No case has a reviewed publication, PDBbind, ITC, SPR, fluorescence, or other experimental affinity annotation yet.
- T6 needs a clearer upstream biological/source reference if it is going to become more than a legacy Vina compatibility case.
- RNA-ligand cases, including the expanded riboswitch panel, need affinity-source review before AptScout/AptScout can use them for absolute or relative experimental affinity calibration.
