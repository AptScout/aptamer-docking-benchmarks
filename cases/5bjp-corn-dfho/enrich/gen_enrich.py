#!/usr/bin/env python3
"""Generate actives.pdbqt and decoys.pdbqt for 5bjp-corn-dfho enrichment set."""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import AllChem

ENRICH_DIR = Path(__file__).parent
INPUTS_DIR = ENRICH_DIR.parent / "inputs"


def smiles_to_pdbqt(name: str, smiles: str, out_path: Path) -> bool:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        print(f"  ERROR: invalid SMILES for {name}: {smiles}")
        return False
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    if AllChem.EmbedMolecule(mol, params) == -1:
        print(f"  ERROR: embedding failed for {name}")
        return False
    AllChem.MMFFOptimizeMolecule(mol)

    with tempfile.NamedTemporaryFile(suffix=".mol", delete=False) as f:
        tmp_mol = f.name
    Chem.MolToMolFile(mol, tmp_mol)

    result = subprocess.run(
        ["obabel", tmp_mol, "-O", str(out_path), "--partialcharge", "gasteiger"],
        capture_output=True, text=True
    )
    os.unlink(tmp_mol)

    if not out_path.exists():
        print(f"  ERROR obabel failed for {name}: {result.stderr}")
        return False
    mw = Chem.Descriptors.MolWt(Chem.RemoveHs(mol))
    print(f"  OK: {name}, MW={mw:.1f}, atoms={Chem.RemoveHs(mol).GetNumAtoms()}")
    return True


def wrap_model(pdbqt_text: str, name: str, model_num: int) -> str:
    """Strip existing MODEL/ENDMDL, set Name remark, wrap in MODEL/ENDMDL."""
    lines = pdbqt_text.splitlines(keepends=True)
    inner = []
    name_inserted = False
    for line in lines:
        if line.startswith("MODEL") or line.startswith("ENDMDL"):
            continue
        if line.startswith("REMARK  Name") and not name_inserted:
            inner.append(f"REMARK  Name = {name}\n")
            name_inserted = True
            continue
        inner.append(line)
    if not name_inserted:
        inner.insert(0, f"REMARK  Name = {name}\n")

    result = [f"MODEL        {model_num}\n"]
    result.extend(inner)
    if not result[-1].endswith("\n"):
        result.append("\n")
    result.append("ENDMDL\n")
    return "".join(result)


def build_actives():
    """Build actives.pdbqt: DFHO (crystal) + DFHBI + DFHBI-1T."""
    active_smiles = {
        # DFHBI: (Z)-4-[(3,5-difluoro-4-hydroxyphenyl)methylidene]-1-methylimidazol-5(4H)-one
        "DFHBI": "CN1C(=O)/C(=C\\c2cc(F)c(O)c(F)c2)N=C1",
        # DFHBI-1T: N1-(2,2,2-trifluoroethyl) variant
        "DFHBI_1T": "O=C1/C(=C\\c2cc(F)c(O)c(F)c2)N=CN1CC(F)(F)F",
        # DMABI: 4-(dimethylamino)benzylidene imidazolinone (non-fluoro analog)
        "DMABI": "CN1C(=O)/C(=C\\c2ccc(N(C)C)cc2)N=C1",
    }

    models = []

    # Model 1: crystal ligand from inputs
    crystal_pdbqt = (INPUTS_DIR / "ligand.pdbqt").read_text()
    models.append(wrap_model(crystal_pdbqt, "DFHO_crystal", len(models) + 1))

    # Models 2+: generated analogues
    with tempfile.TemporaryDirectory() as tmpdir:
        for name, smi in active_smiles.items():
            tmp_pdbqt = Path(tmpdir) / f"{name}.pdbqt"
            if smiles_to_pdbqt(name, smi, tmp_pdbqt):
                text = tmp_pdbqt.read_text()
                models.append(wrap_model(text, name, len(models) + 1))
            else:
                print(f"  Skipping {name}")

    out_path = ENRICH_DIR / "actives.pdbqt"
    out_path.write_text("".join(models))
    print(f"Wrote actives.pdbqt with {len(models)} compounds")


def build_decoys():
    """Build decoys.pdbqt: 20 small aromatic heterocycles, NOT benzylidene-imidazolinone."""
    decoy_smiles = {
        # Indoles / pyrroles
        "indole":            "c1ccc2[nH]ccc2c1",
        "benzimidazole":     "c1ccc2nc[nH]c2c1",
        "benzoxazole":       "c1ccc2ocnc2c1",
        "benzothiazole":     "c1ccc2scnc2c1",
        # Quinolines / isoquinolines
        "quinoline":         "c1ccc2ncccc2c1",
        "isoquinoline":      "c1ccc2cnccc2c1",
        "quinoxaline":       "c1cnc2ccccc2n1",
        "phthalazine":       "c1ccc2cnncc2c1",
        # Simple phenyl + hetero
        "phenylimidazole":   "c1ccc(-c2cnc[nH]2)cc1",
        "phenylpyrazole":    "c1ccc(-c2cc[nH]n2)cc1",
        "phenyloxazole":     "c1ccc(-c2cnco2)cc1",
        "phenylthiophene":   "c1ccc(-c2cccs2)cc1",
        # Flavone-like (but no imidazolinone)
        "chromone":          "O=c1ccoc2ccccc12",
        "coumarin":          "O=C1CC(=O)c2ccccc21",
        # Smaller MW
        "purine":            "c1nc2cncnc2[nH]1",
        "acridine":          "c1ccc2nc3ccccc3cc2c1",
        "xanthene_simple":   "C1COc2ccccc2C1",
        "fluorene":          "C1c2ccccc2Cc2ccccc21",
        # Hydroxy/methyl variants
        "methylbenzimidazole": "Cc1nc2ccccc2[nH]1",
        "hydroxybenzothiazole": "Oc1ccc2scnc2c1",
    }

    models = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for name, smi in decoy_smiles.items():
            tmp_pdbqt = Path(tmpdir) / f"{name}.pdbqt"
            if smiles_to_pdbqt(name, smi, tmp_pdbqt):
                text = tmp_pdbqt.read_text()
                models.append(wrap_model(text, name, len(models) + 1))
            else:
                print(f"  Skipping decoy {name}")

    out_path = ENRICH_DIR / "decoys.pdbqt"
    out_path.write_text("".join(models))
    print(f"Wrote decoys.pdbqt with {len(models)} compounds")


if __name__ == "__main__":
    from rdkit.Chem import Descriptors  # noqa

    print("=== Building actives ===")
    build_actives()
    print("\n=== Building decoys ===")
    build_decoys()
    print("\nDone.")
