#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
CONFIG_PATH_KEYS = ("receptor", "ligand", "out", "log")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory local ignored molecular inputs for benchmark cases."
    )
    parser.add_argument(
        "--manifest",
        default=str(MANIFEST),
        help="Path to benchmark manifest.json.",
    )
    parser.add_argument(
        "--case",
        dest="case_id",
        help="Only check one benchmark case ID.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when any referenced local input is missing.",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        help="Write machine-readable JSON instead of a table.",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest = load_json(manifest_path)
    entries = manifest.get("cases", [])
    if args.case_id:
        entries = [entry for entry in entries if entry.get("id") == args.case_id]
        if not entries:
            available = ", ".join(entry.get("id", "<missing>") for entry in manifest.get("cases", []))
            print(f"ERROR: case not found. Available cases: {available}", file=sys.stderr)
            return 1

    all_records: list[InputRecord] = []
    for entry in entries:
        case_id = entry.get("id", "<missing>")
        case_path_value = entry.get("casePath")
        if not case_path_value:
            all_records.append(InputRecord(case_id, "case.json", Path("<missing casePath>"), False))
            continue

        case_path = resolve_path(case_path_value, manifest_path.parent)
        all_records.append(InputRecord(case_id, "case.json", case_path, case_path.exists()))
        if not case_path.exists():
            continue

        case = load_json(case_path)
        all_records.extend(records_for_case(case_id, case, case_path))

    missing = [record for record in all_records if not record.exists]

    if args.json_output:
        print(json.dumps(json_payload(all_records, missing), indent=2, sort_keys=True))
    else:
        print_records(all_records)
        print("")
        print(f"Checked {len(set(record.case_id for record in all_records))} case(s), {len(all_records)} referenced path(s).")
        if missing:
            print(f"Missing {len(missing)} path(s).")
        else:
            print("All referenced paths exist locally.")

    if missing and args.strict:
        return 1
    return 0


def records_for_case(case_id: str, case: dict, case_path: Path) -> list["InputRecord"]:
    records = []
    case_dir = case_path.parent

    contacts_path = case.get("expectedContactsPath")
    if contacts_path:
        contacts_file = resolve_path(contacts_path, case_dir)
        records.append(InputRecord(case_id, "expected_contacts", contacts_file, contacts_file.exists()))

    config_path = case.get("configPath")
    if not config_path:
        records.append(InputRecord(case_id, "config", Path("<missing configPath>"), False))
        return records

    config_file = resolve_path(config_path, case_dir)
    records.append(InputRecord(case_id, "config", config_file, config_file.exists()))
    if config_file.exists():
        config = parse_vina_config(config_file)
        for key in CONFIG_PATH_KEYS:
            if key in config:
                resolved = resolve_vina_config_path(config[key], config_file.parent)
                records.append(InputRecord(case_id, f"config:{key}", resolved, resolved.exists()))

    decoy_paths = []
    if case.get("decoyPosePath"):
        decoy_paths.append(case["decoyPosePath"])
    decoy_paths.extend(case.get("decoyPosePaths", []))
    for index, decoy_path in enumerate(decoy_paths, start=1):
        decoy_file = resolve_path(decoy_path, case_dir)
        label = "decoyPosePath" if len(decoy_paths) == 1 else f"decoyPosePath[{index}]"
        records.append(InputRecord(case_id, label, decoy_file, decoy_file.exists()))

    return records


def parse_vina_config(config_file: Path) -> dict[str, str]:
    values = {}
    for raw_line in config_file.read_text(errors="replace").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def resolve_vina_config_path(path: str, base: Path) -> Path:
    # Historical Vina configs sometimes prefix relative paths with a slash or backslash.
    trimmed = path.strip()
    if trimmed.startswith("\\"):
        trimmed = trimmed.lstrip("\\/")
    expanded = Path(trimmed).expanduser()
    if expanded.is_absolute():
        return expanded
    return (base / expanded).resolve()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def resolve_path(path: str, base: Path) -> Path:
    expanded = Path(path).expanduser()
    if expanded.is_absolute():
        return expanded
    return (base / expanded).resolve()


def print_records(records: list["InputRecord"]) -> None:
    case_width = max([len("case")] + [len(record.case_id) for record in records])
    label_width = max([len("label")] + [len(record.label) for record in records])
    print(f"{'case'.ljust(case_width)}  {'label'.ljust(label_width)}  status   path")
    print(f"{'-' * case_width}  {'-' * label_width}  -------  ----")
    for record in records:
        status = "ok" if record.exists else "missing"
        print(
            f"{record.case_id.ljust(case_width)}  "
            f"{record.label.ljust(label_width)}  "
            f"{status.ljust(7)}  "
            f"{relative_or_absolute(record.path)}"
        )


def json_payload(records: list["InputRecord"], missing: list["InputRecord"]) -> dict:
    case_ids = sorted(set(record.case_id for record in records))
    return {
        "caseCount": len(case_ids),
        "pathCount": len(records),
        "missingCount": len(missing),
        "allPresent": not missing,
        "cases": case_ids,
        "records": [record.to_json() for record in records],
    }


def relative_or_absolute(path: Path) -> str:
    if str(path).startswith("<"):
        return str(path)
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


class InputRecord:
    def __init__(self, case_id: str, label: str, path: Path, exists: bool):
        self.case_id = case_id
        self.label = label
        self.path = path
        self.exists = exists

    def to_json(self) -> dict:
        payload = {
            "caseID": self.case_id,
            "label": self.label,
            "path": str(self.path),
            "relativePath": relative_or_absolute(self.path),
            "exists": self.exists,
        }
        if self.exists:
            payload["sizeBytes"] = self.path.stat().st_size
        return payload


if __name__ == "__main__":
    raise SystemExit(main())
