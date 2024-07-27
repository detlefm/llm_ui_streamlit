from io import BytesIO
import fitz  # PyMuPDF
from PIL import Image



def convert(filename:str|BytesIO) -> Image:
    if isinstance(filename,str):
        # Öffne die PDF-Datei mit PyMuPDF
        pdf_document = fitz.open(filename)
    elif isinstance(filename,BytesIO):
        pdf_stream = BytesIO(filename.read())
        pdf_document = fitz.open(stream=pdf_stream, filetype="pdf")

    # Liste zum Speichern der Seitenbilder
    pages = []

    # Iteriere durch jede Seite der PDF und konvertiere sie in ein Bild
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pages.append(img)

    # Bestimme die Breite und Höhe des kombinierten Bildes
    total_width = max(page.width for page in pages)
    total_height = sum(page.height for page in pages)

    # Erstelle ein neues Bild mit der berechneten Größe und setze es auf weiß
    combined_image = Image.new('RGB', (total_width, total_height), (255, 255, 255))

    # Füge die Seitenbilder in das kombinierte Bild ein
    y_offset = 0
    for page in pages:
        combined_image.paste(page, (0, y_offset))
        y_offset += page.height

    return combined_image
