# Codice per convertire un pdf immagine in immagine jpg

import fitz

zoom=3

pdffile = "POLO.pdf"
doc = fitz.open(pdffile)
page = doc.loadPage(0)  # number of page
mat = fitz.Matrix(zoom, zoom)     #matrice per lo zoom. risoluzione di default 596x842, moltiplicata poi per il numeretto
pix = page.getPixmap(matrix = mat)
output = "POLO.jpg"
pix.writePNG(output)