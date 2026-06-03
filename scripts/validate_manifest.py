#!/usr/bin/env python3
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
VALID_STATUSES = {
    "seed",
    "parsed",
    "contact_reviewed",
    "affinity_reviewed",
    "validated",
}
VALID_SYSTEM_TYPES = {
    "dna_aptamer_protein",
    "rna_aptamer_protein",
    "rna_ligand",
    "dna_ligand",
    "protein_nucleic_acid",
    "other",
}
VALID_INTERACTION_KINDS = {
    "contact",
    "hydrophobicContact",
    "hydrogenBond",
    "electrostaticAttraction",
    "electrostaticRepulsion",
    "phosphateElectrostatic",
    "baseStacking",
    "metalCoordination",
    "clash",
}


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    errors = []
    warnings = []

    if manifest.get("schemaVersion") != 1:
        errors.append("manifest.schemaVersion must be 1")
    if not manifest.get("datasetVersion"):
        errors.append("manifest.datasetVersion is required")
    if not manifest.get("name"):
        errors.append("manifest.name is required")

    seen_ids = set()
    for entry in manifest.get("cases", []):
        case_id = entry.get("id")
        case_path = entry.get("casePath")
        if not case_id:
            errors.append("case entry missing id")
            continue
        if case_id in seen_ids:
            errors.append(f"duplicate case id: {case_id}")
        seen_ids.add(case_id)
        if not case_path:
            errors.append(f"{case_id}: missing casePath")
            continue
        if not is_repo_relative_path(case_path):
            errors.append(f"{case_id}: casePath must be a repository-relative path without '..': {case_path}")
            continue

        case_file = ROOT / case_path
        if not case_file.exists():
            errors.append(f"{case_id}: missing {case_path}")
            continue
        case = json.loads(case_file.read_text())
        validate_case(case_id, case, case_file, errors, warnings)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        for warning in warnings:
            print(f"WARNING: {warning}", file=sys.stderr)
        return 1

    for warning in warnings:
        print(f"WARNING: {warning}")
    print(f"Validated {len(seen_ids)} benchmark case(s).")
    return 0


def validate_case(case_id: str, case: dict, case_file: Path, errors: list[str], warnings: list[str]) -> None:
    if case.get("id") != case_id:
        errors.append(f"{case_id}: case.json id mismatch: {case.get('id')}")

    required = ["name", "systemType", "curationStatus", "configPath", "referencePoseMode"]
    for key in required:
        if key not in case:
            errors.append(f"{case_id}: missing required field {key}")

    if case.get("systemType") not in VALID_SYSTEM_TYPES:
        errors.append(f"{case_id}: invalid systemType {case.get('systemType')}")

    if case.get("curationStatus") not in VALID_STATUSES:
        errors.append(f"{case_id}: invalid curationStatus {case.get('curationStatus')}")

    if not isinstance(case.get("referencePoseMode"), int) or case.get("referencePoseMode", 0) < 1:
        errors.append(f"{case_id}: referencePoseMode must be an integer >= 1")

    config_path = case.get("configPath")
    if config_path:
        validate_case_relative_path(case_id, "configPath", config_path, errors)
        config_file = resolve_path(config_path, base=case_file.parent)
        if not config_file.exists():
            warnings.append(f"{case_id}: configPath does not exist locally: {config_file}")
        else:
            validate_vina_config_paths(case_id, config_file, errors)

    expected_contacts_path = case.get("expectedContactsPath")
    if expected_contacts_path:
        validate_case_relative_path(case_id, "expectedContactsPath", expected_contacts_path, errors)
        contacts_file = case_file.parent / expected_contacts_path
        if not contacts_file.exists():
            errors.append(f"{case_id}: missing expected contacts {expected_contacts_path}")
        else:
            contacts = json.loads(contacts_file.read_text())
            validate_expected_contacts(case_id, contacts, errors, warnings)

    decoy_paths = []
    if case.get("decoyPosePath"):
        decoy_paths.append(case["decoyPosePath"])
    decoy_paths.extend(case.get("decoyPosePaths", []))
    if len(decoy_paths) != len(set(decoy_paths)):
        errors.append(f"{case_id}: duplicate decoy pose paths")
    for decoy_path in decoy_paths:
        validate_case_relative_path(case_id, "decoyPosePath", decoy_path, errors)
        decoy_file = resolve_path(decoy_path, base=case_file.parent)
        if not decoy_file.exists():
            warnings.append(f"{case_id}: decoy pose path does not exist locally: {decoy_file}")

    validate_enrichment_sets(case_id, case.get("enrichmentSets", []), case_file.parent, errors)


def validate_enrichment_sets(case_id: str, enrichment_sets: list[dict], case_directory: Path, errors: list[str]) -> None:
    if not isinstance(enrichment_sets, list):
        errors.append(f"{case_id}: enrichmentSets must be a list")
        return
    path_keys = [
        "receptorPath",
        "activePosePath",
        "crystalPosePath",
        "decoyPosePath",
    ]
    path_list_keys = [
        "activePosePaths",
        "decoyPosePaths",
    ]
    seen_ids = set()
    for index, enrichment_set in enumerate(enrichment_sets):
        if not isinstance(enrichment_set, dict):
            errors.append(f"{case_id}: enrichmentSets[{index}] must be an object")
            continue
        enrichment_id = enrichment_set.get("id", f"#{index}")
        if enrichment_id in seen_ids:
            errors.append(f"{case_id}: duplicate enrichment set id {enrichment_id}")
        seen_ids.add(enrichment_id)
        for key in path_keys:
            if value := enrichment_set.get(key):
                validate_case_relative_path(case_id, f"enrichmentSets.{enrichment_id}.{key}", value, errors)
        for key in path_list_keys:
            values = enrichment_set.get(key, [])
            if not isinstance(values, list):
                errors.append(f"{case_id}: enrichmentSets.{enrichment_id}.{key} must be a list")
                continue
            for value in values:
                validate_case_relative_path(case_id, f"enrichmentSets.{enrichment_id}.{key}", value, errors)
        active_count = enrichment_pose_count(case_directory, [enrichment_set.get("activePosePath")] + enrichment_set.get("activePosePaths", []))
        decoy_count = enrichment_pose_count(case_directory, [enrichment_set.get("decoyPosePath")] + enrichment_set.get("decoyPosePaths", []))
        if enrichment_set.get("activeCount") is not None and enrichment_set["activeCount"] != active_count:
            errors.append(
                f"{case_id}: enrichmentSets.{enrichment_id}.activeCount declares "
                f"{enrichment_set['activeCount']} but local files contain {active_count} model(s)"
            )
        if enrichment_set.get("decoyCount") is not None and enrichment_set["decoyCount"] != decoy_count:
            errors.append(
                f"{case_id}: enrichmentSets.{enrichment_id}.decoyCount declares "
                f"{enrichment_set['decoyCount']} but local files contain {decoy_count} model(s)"
            )


def validate_expected_contacts(case_id: str, contacts: dict, errors: list[str], warnings: list[str]) -> None:
    allowed_keys = {"receptorResidues", "ligandAtoms", "interactionKinds", "notes"}
    for key in contacts:
        if key not in allowed_keys:
            errors.append(f"{case_id}: unexpected expected_contacts key {key}")

    receptor_residues = contacts.get("receptorResidues", [])
    ligand_atoms = contacts.get("ligandAtoms", [])
    interaction_kinds = contacts.get("interactionKinds", [])

    for field_name, values in [
        ("receptorResidues", receptor_residues),
        ("ligandAtoms", ligand_atoms),
        ("interactionKinds", interaction_kinds),
    ]:
        if not isinstance(values, list):
            errors.append(f"{case_id}: expected_contacts.{field_name} must be a list")
            continue
        if len(values) != len(set(values)):
            errors.append(f"{case_id}: expected_contacts.{field_name} contains duplicates")

    for kind in interaction_kinds:
        if kind not in VALID_INTERACTION_KINDS:
            errors.append(f"{case_id}: invalid interaction kind {kind}")

    if not receptor_residues and not ligand_atoms and not interaction_kinds:
        warnings.append(f"{case_id}: expected contacts file has no expectations")


def validate_vina_config_paths(case_id: str, config_file: Path, errors: list[str]) -> None:
    values = parse_vina_config(config_file)
    for key in ["receptor", "ligand", "out", "log"]:
        value = values.get(key)
        if value and not is_vina_config_local_path(value):
            errors.append(f"{case_id}: Vina config {key} path must stay local to config directory: {value}")


def parse_vina_config(config_file: Path) -> dict[str, str]:
    values = {}
    for raw_line in config_file.read_text().splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip().lower()] = value.strip()
    return values


def enrichment_pose_count(case_directory: Path, paths: list[str | None]) -> int:
    total = 0
    for path in paths:
        if not path:
            continue
        pdbqt_file = resolve_path(path, base=case_directory)
        if not pdbqt_file.exists():
            continue
        total += pdbqt_model_count(pdbqt_file)
    return total


def pdbqt_model_count(pdbqt_file: Path) -> int:
    text = pdbqt_file.read_text(errors="replace")
    model_count = sum(1 for line in text.splitlines() if line.strip().startswith("MODEL"))
    if model_count:
        return model_count
    has_atoms = any(line.strip().startswith(("ATOM", "HETATM")) for line in text.splitlines())
    return 1 if has_atoms else 0


def resolve_path(path: str, base: Path) -> Path:
    expanded = Path(path).expanduser()
    if expanded.is_absolute():
        return expanded
    return (base / expanded).resolve()


def validate_case_relative_path(case_id: str, field_name: str, value: str, errors: list[str]) -> None:
    if not is_repo_relative_path(value):
        errors.append(f"{case_id}: {field_name} must be case-relative without '..' or absolute roots: {value}")


def is_repo_relative_path(value: str) -> bool:
    path = Path(value).expanduser()
    return not path.is_absolute() and ".." not in Path(value).parts


def is_vina_config_local_path(value: str) -> bool:
    stripped = value.strip()
    normalized = stripped.replace("\\", "/").strip("/")
    parts = Path(normalized).parts
    return bool(stripped) and not stripped.startswith("/") and not stripped.startswith("~") and ".." not in parts


if __name__ == "__main__":
    raise SystemExit(main())
