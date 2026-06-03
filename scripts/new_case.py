#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
VALID_SYSTEM_TYPES = {
    "dna_aptamer_protein",
    "rna_aptamer_protein",
    "rna_ligand",
    "dna_ligand",
    "protein_nucleic_acid",
    "other",
}
CASE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a new shared aptamer docking benchmark case."
    )
    parser.add_argument("case_id", help="Lowercase case ID, e.g. t6-thrombin-vina.")
    parser.add_argument("--name", required=True, help="Human-readable case name.")
    parser.add_argument(
        "--system-type",
        required=True,
        choices=sorted(VALID_SYSTEM_TYPES),
        help="Benchmark system type.",
    )
    parser.add_argument(
        "--config-path",
        default="inputs/conf.txt",
        help="Path to docking config, resolved relative to the generated case.json directory.",
    )
    parser.add_argument(
        "--reference-mode",
        type=int,
        default=1,
        help="Reference output pose mode number.",
    )
    parser.add_argument(
        "--expected-affinity",
        type=float,
        help="Optional expected/reference affinity in kcal/mol.",
    )
    parser.add_argument("--source", default="", help="Optional source database, publication, or local source note.")
    parser.add_argument("--notes", default="", help="Optional case notes.")
    parser.add_argument(
        "--manifest",
        default=str(MANIFEST),
        help="Path to benchmark manifest.json.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned files without writing them.",
    )
    args = parser.parse_args()

    case_id = args.case_id.strip()
    if not CASE_ID_PATTERN.match(case_id):
        print(
            "ERROR: case_id must start with lowercase alphanumeric and contain only lowercase letters, numbers, '.', '_' or '-'.",
            file=sys.stderr,
        )
        return 1
    if args.reference_mode < 1:
        print("ERROR: --reference-mode must be >= 1.", file=sys.stderr)
        return 1

    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest = load_json(manifest_path)
    existing_ids = {entry.get("id") for entry in manifest.get("cases", [])}
    if case_id in existing_ids:
        print(f"ERROR: case already exists in manifest: {case_id}", file=sys.stderr)
        return 1

    case_dir = manifest_path.parent / "cases" / case_id
    case_path = case_dir / "case.json"
    contacts_path = case_dir / "expected_contacts.json"
    notes_path = case_dir / "notes.md"
    manifest_case_path = f"cases/{case_id}/case.json"

    case = {
        "id": case_id,
        "name": args.name,
        "systemType": args.system_type,
        "curationStatus": "seed",
        "configPath": args.config_path,
        "referencePoseMode": args.reference_mode,
        "expectedContactsPath": "expected_contacts.json",
        "source": args.source,
        "notes": args.notes or "New seed case. Fill in source identifiers, affinity provenance, and contact review notes.",
    }
    if args.expected_affinity is not None:
        case["expectedBestAffinityKcalMol"] = args.expected_affinity

    expected_contacts = {
        "receptorResidues": [],
        "ligandAtoms": [],
        "interactionKinds": [],
        "notes": "Seed case: add expected contacts after initial parsing or literature/crystal-contact review.",
    }
    notes = notes_template(args, case_id)

    print(f"New benchmark case: {case_id}")
    print(f"- case directory: {relative(case_dir, manifest_path.parent)}")
    print(f"- case.json: {relative(case_path, manifest_path.parent)}")
    print(f"- expected contacts: {relative(contacts_path, manifest_path.parent)}")
    print(f"- notes: {relative(notes_path, manifest_path.parent)}")
    print(f"- manifest entry: {manifest_case_path}")

    if args.dry_run:
        print("Dry run only; no files written.")
        return 0

    if case_dir.exists():
        print(f"ERROR: case directory already exists: {case_dir}", file=sys.stderr)
        return 1

    case_dir.mkdir(parents=True)
    write_json(case_path, case)
    write_json(contacts_path, expected_contacts)
    notes_path.write_text(notes)

    manifest.setdefault("cases", []).append({
        "id": case_id,
        "casePath": manifest_case_path,
    })
    write_json(manifest_path, manifest)

    print("")
    print("Created case. Next:")
    print("  python3 scripts/validate_manifest.py")
    print(f"  python3 scripts/summarize_case.py {case_id}")
    return 0


def notes_template(args: argparse.Namespace, case_id: str) -> str:
    return f"""# {args.name}

Seed benchmark case `{case_id}`.

## Source

{args.source or "TODO: add source database, PDB/NAKB/RCSB/PDBbind ID, publication, or local source note."}

## Inputs

Configured path:

```text
{args.config_path}
```

Place local raw inputs under `inputs/` if needed. That directory is ignored by git.

## Curation Notes

- TODO: identify receptor and aptamer/ligand roles.
- TODO: confirm reference pose mode {args.reference_mode}.
- TODO: review expected contacts.
- TODO: add affinity source if available.
"""


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n")


def relative(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
