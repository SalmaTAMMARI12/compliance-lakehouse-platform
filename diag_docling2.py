import sys
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption

CHEMIN_PDF = sys.argv[1]

options = PdfPipelineOptions()
options.do_ocr = False
converter = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=options)})
resultat = converter.convert(CHEMIN_PDF)
document = resultat.document

items = list(document.iterate_items())
for idx, (item, level) in enumerate(items):
    texte = getattr(item, "text", None)
    type_item = type(item).__name__
    if texte and texte.strip() == "Constats" and type_item == "SectionHeaderItem":
        page = item.prov[0].page_no if getattr(item, "prov", None) else "?"
        print(f"=== 'Constats' (SectionHeaderItem) page {page}, item #{idx} ===")
        # affiche les 5 items suivants
        for j in range(idx + 1, min(idx + 6, len(items))):
            item_suivant, _ = items[j]
            t = getattr(item_suivant, "text", "")
            print(f"  [{type(item_suivant).__name__}]: {t[:120]}")
        print()
