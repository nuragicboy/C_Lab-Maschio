# Codice per convertire un pdf immagine in immagine jpg

import fitz

pdffile = "POLO.pdf"
doc = fitz.open(pdffile)
page = doc.loadPage(0)  # number of page
pix = page.getPixmap()
output = "POLO.jpg"
pix.writePNG(output)