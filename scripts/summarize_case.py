#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize a shared aptamer docking benchmark case."
    )
    parser.add_argument("case_id", nargs="?", help="Case ID to summarize. Defaults to the first case.")
    parser.add_argument(
        "--manifest",
        default=str(MANIFEST),
        help="Path to benchmark manifest.json.",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest = load_json(manifest_path)
    entry = find_case_entry(manifest, args.case_id)
    if entry is None:
        available = ", ".join(case.get("id", "<missing>") for case in manifest.get("cases", []))
        print(f"ERROR: case not found. Available cases: {available}", file=sys.stderr)
        return 1

    case_path = resolve_path(entry["casePath"], manifest_path.parent)
    case = load_json(case_path)
    expected_contacts = {}
    expected_contacts_path = None
    if case.get("expectedContactsPath"):
        expected_contacts_path = resolve_path(case["expectedContactsPath"], case_path.parent)
        if expected_contacts_path.exists():
            expected_contacts = load_json(expected_contacts_path)

    config_path = resolve_path(case.get("configPath", ""), case_path.parent)

    print(f"Case: {case.get('id', entry.get('id'))}")
    print(f"Name: {case.get('name', 'n/a')}")
    print(f"Status: {case.get('curationStatus', 'n/a')}")
    print(f"System: {case.get('systemType', 'n/a')}")
    print(f"Reference pose mode: {case.get('referencePoseMode', 'n/a')}")
    print(f"Expected affinity: {format_optional(case.get('expectedBestAffinityKcalMol'), suffix=' kcal/mol')}")
    print("")

    print("Paths:")
    print(f"- manifest: {relative_or_absolute(manifest_path)} [exists]")
    print(f"- case.json: {relative_or_absolute(case_path)} [{exists_label(case_path)}]")
    print(f"- config: {relative_or_absolute(config_path)} [{exists_label(config_path)}]")
    if expected_contacts_path:
        print(f"- expected contacts: {relative_or_absolute(expected_contacts_path)} [{exists_label(expected_contacts_path)}]")
    else:
        print("- expected contacts: n/a")
    print("")

    print("Expected Contacts:")
    print_list("receptor residues", expected_contacts.get("receptorResidues", []))
    print_list("ligand atoms", expected_contacts.get("ligandAtoms", []))
    print_list("interaction kinds", expected_contacts.get("interactionKinds", []))
    if expected_contacts.get("notes"):
        print(f"- notes: {expected_contacts['notes']}")
    print("")

    print("Source:")
    print(f"- {case.get('source', 'n/a')}")
    if case.get("notes"):
        print(f"- notes: {case['notes']}")
    print("")

    print("Suggested Next Actions:")
    for action in suggested_actions(case, expected_contacts, config_path):
        print(f"- {action}")
    return 0


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def find_case_entry(manifest: dict, case_id: str | None) -> dict | None:
    cases = manifest.get("cases", [])
    if case_id is None:
        return cases[0] if cases else None
    return next((case for case in cases if case.get("id") == case_id), None)


def resolve_path(path: str, base: Path) -> Path:
    expanded = Path(path).expanduser()
    if expanded.is_absolute():
        return expanded
    return (base / expanded).resolve()


def relative_or_absolute(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def exists_label(path: Path) -> str:
    return "exists" if path.exists() else "missing"


def print_list(label: str, values: list[str]) -> None:
    if values:
        print(f"- {label}: {', '.join(values)}")
    else:
        print(f"- {label}: n/a")


def format_optional(value, suffix: str = "") -> str:
    if value is None:
        return "n/a"
    return f"{value}{suffix}"


def suggested_actions(case: dict, expected_contacts: dict, config_path: Path) -> list[str]:
    actions = []
    status = case.get("curationStatus")
    if status == "seed":
        actions.append("Validate seed contacts against crystal/literature contacts.")
    if not case.get("structureID"):
        actions.append("Add source PDB/NAKB identifier if available.")
    if not case.get("affinitySource"):
        actions.append("Add affinity source beyond docking log if available.")
    if not config_path.exists():
        actions.append("Make configPath resolvable locally or document how to restore inputs.")
    if not expected_contacts:
        actions.append("Add expected_contacts.json before contact-aware calibration.")
    elif expected_contacts.get("notes", "").lower().find("seed") >= 0:
        actions.append("Promote expected contacts from seed hypothesis after manual review.")
    if not actions:
        actions.append("No immediate curation gaps detected.")
    return actions


if __name__ == "__main__":
    raise SystemExit(main())
