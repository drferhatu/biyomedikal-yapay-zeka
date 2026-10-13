#!/usr/bin/env python
"""templates/proje/ klasöründen öğrencilere dağıtılacak şablon paketlerini üretir:
  public/proje/proje-sablonu.zip      depo iskeleti (README, .gitignore, src/, notebooks/, rapor/)
  public/proje/rapor-sablonu.zip      yalnızca LaTeX raporu (Overleaf'e doğrudan yüklenebilir)
  public/proje/main.tex, kaynaklar.bib  tek tek indirilebilir kopyalar
Ayrıca notebooks/proje-baslangic.ipynb varsa şablonun notebooks/ klasörüne kopyalar.

Kullanım: /opt/miniconda3/envs/ferhat_ml/bin/python scripts/make_project_templates.py
"""
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "templates" / "proje"
OUT = ROOT / "public" / "proje"
OUT.mkdir(parents=True, exist_ok=True)

starter = ROOT / "notebooks" / "proje-baslangic.ipynb"
if starter.exists():
    shutil.copy(starter, SRC / "notebooks" / "01_baslangic.ipynb")


def zipdir(zpath: Path, base: Path, prefix: str):
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(base.rglob("*")):
            if p.is_file() and ".ipynb_checkpoints" not in p.parts and p.name != ".DS_Store":
                z.write(p, f"{prefix}/{p.relative_to(base).as_posix()}")
    print(f"✓ {zpath.relative_to(ROOT)} ({zpath.stat().st_size // 1024} KB)")


zipdir(OUT / "proje-sablonu.zip", SRC, "proje-sablonu")
zipdir(OUT / "rapor-sablonu.zip", SRC / "rapor", "rapor")
for f in ["main.tex", "kaynaklar.bib"]:
    shutil.copy(SRC / "rapor" / f, OUT / f)
    print(f"✓ public/proje/{f}")
