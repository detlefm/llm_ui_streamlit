import subprocess
import os

path2office = r'C:\Program Files\LibreOffice\program'

# This module is not needed yet. 

def word_to_pdf_with_libreoffice(word_bytes, output_path):
    # Temporäre Datei erstellen
    with open(output_path, 'wb') as f:
        f.write(word_bytes)

    soffice = os.path.join(path2office,"soffice.exe")
    # LibreOffice-Befehl ausführen
    subprocess.run([
        soffice,
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', os.path.dirname(output_path),
        output_path
    ])

    # PDF-Datei lesen
    pdf_path = os.path.splitext(output_path)[0] + '.pdf'
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    # Temporäre Dateien löschen
    os.remove(output_path)
    os.remove(pdf_path)

    return pdf_bytes