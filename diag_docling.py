"""Diagnostic : explore la structure interne de Docling pour comprendre
pourquoi certains chapitres n'ont pas de tableau 'Constats' détecté.
"""
import sys
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption

CHEMIN_PDF = sys.argv[1] if len(sys.argv) > 1 else "CHEMIN_A_REMPLACER.pdf"

options = PdfPipelineOptions()
options.do_ocr = False
converter = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=options)})

resultat = converter.convert(CHEMIN_PDF)
document = resultat.document

print(f"Nombre de tableaux détectés par Docling: {len(document.tables)}")
print()

for i, table in enumerate(document.tables):
    pages = set()
    if table.prov:
        for p in table.prov:
            pages.add(p.page_no)
    print(f"--- Tableau {i} (page(s): {sorted(pages)}) ---")

    df = table.export_to_dataframe()
    premiere_col = df.iloc[:, 0].astype(str).tolist() if not df.empty else []
    print("  Première colonne:", premiere_col[:3], "..." if len(premiere_col) > 3 else "")
    print()

print("=" * 60)
print("Recherche de 'Constats' dans le texte hors-tableau (paragraphes)")
print("=" * 60)

for item, level in document.iterate_items():
    texte = getattr(item, "text", None)
    if texte and "Constats" in texte:
        page = item.prov[0].page_no if getattr(item, "prov", None) else "?"
        type_item = type(item).__name__
        print(f"  page {page} [{type_item}]: {texte[:150]}")
