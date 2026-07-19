import sys
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption

CHEMIN_PDF = sys.argv[1]

options = PdfPipelineOptions()
options.do_ocr = False
options.table_structure_options.mode = TableFormerMode.ACCURATE

converter = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=options)})
resultat = converter.convert(CHEMIN_PDF)
document = resultat.document

print(f"Nombre de tableaux détectés (mode ACCURATE): {len(document.tables)}")
print()

for i, table in enumerate(document.tables):
    df = table.export_to_dataframe(doc=document)
    premiere_col = df.iloc[:, 0].astype(str).tolist() if not df.empty else []
    a_constats = any("Constats" in str(c) for c in premiere_col)
    marqueur = " <-- CONTIENT CONSTATS" if a_constats else ""
    print(f"Tableau {i}: {premiere_col[:4]}{marqueur}")
