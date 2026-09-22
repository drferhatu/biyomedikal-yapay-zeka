#!/usr/bin/env python
"""DOCX ders izlence formunu ayrıştırır; paragrafları ve tabloları belge sırasıyla
düz metin (ve isteğe bağlı JSON) olarak dışa aktarır.

Bazı formlarda içerik iç içe tablolar/içerik denetimleri içinde olduğu için
python-docx'in üst düzey gezintisi boş kalabilir; bu durumda XML üzerinden
satır/hücre ayraçlı ham metin çıkarılır.

Kullanım:
  /opt/miniconda3/envs/ferhat_ml/bin/python scripts/extract_course_docx.py "<dosya.docx>" [--json çıktı.json]
"""
import json
import re
import sys
import zipfile
from pathlib import Path

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph


def iter_block_items(doc):
    body = doc.element.body
    for child in body.iterchildren():
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            yield Paragraph(child, doc)
        elif tag == 'tbl':
            yield Table(child, doc)


def table_rows(table):
    rows = []
    for row in table.rows:
        cells, prev = [], None
        for cell in row.cells:
            if cell._tc is prev:
                continue
            prev = cell._tc
            cells.append(cell.text.strip().replace('\n', ' / '))
        rows.append(cells)
    return rows


def raw_lines(path):
    """XML'den satır (paragraf/tablo satırı) ve hücre ('|') ayraçlı ham metin."""
    xml = zipfile.ZipFile(path).read('word/document.xml').decode('utf8')
    xml = re.sub(r'</w:p>', '\n', xml)
    xml = re.sub(r'</w:tc>', ' | ', xml)
    xml = re.sub(r'</w:tr>', '\n', xml)
    text = re.sub(r'<[^>]+>', '', xml)
    return [l.strip(' |\t') for l in text.split('\n') if l.strip(' |\t')]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = Path(sys.argv[1])
    doc = Document(str(path))
    blocks = []
    for item in iter_block_items(doc):
        if isinstance(item, Paragraph):
            if item.text.strip():
                blocks.append({"type": "p", "style": item.style.name, "text": item.text.strip()})
        else:
            blocks.append({"type": "table", "rows": table_rows(item)})

    if not blocks:
        print("(üst düzey blok bulunamadı; XML'den ham metin çıkarılıyor)\n")
        blocks = [{"type": "raw", "lines": raw_lines(path)}]

    for b in blocks:
        if b["type"] == "p":
            print(f"[{b['style']}] {b['text']}")
        elif b["type"] == "table":
            print("=== TABLE ===")
            for r in b["rows"]:
                print(" | ".join(r))
            print("=== /TABLE ===")
        else:
            print("\n".join(b["lines"]))

    if "--json" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--json") + 1])
        out.write_text(json.dumps(blocks, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nJSON yazıldı: {out}")


if __name__ == "__main__":
    main()
