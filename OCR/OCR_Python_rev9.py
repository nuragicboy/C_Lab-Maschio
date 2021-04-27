import numpy as np
import cv2
import pytesseract
import openpyxl



#Inserire il percorso di installazione di PyTesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#Ricordati di inserire l'immagine all'interno del progetto Python
img = cv2.imread("POLO.jpg")

# 2. Ridimensionare l'immagine di output
img = cv2.resize(img, None, fx=1.6, fy=1.6)
# 3. Converti l'immagine in scala di grigi
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

config = "--psm 3"

# Page segmentation modes:
        #0    Orientation and script detection (OSD) only.
        #1    Automatic page segmentation with OSD.
        #2    Automatic page segmentation, but no OSD, or OCR.
        #3    Fully automatic page segmentation, but no OSD. (Default)
        #4    Assume a single column of text of variable sizes.
        #5    Assume a single uniform block of vertically aligned text.
        #6    Assume a single uniform block of text.
        #7    Treat the image as a single text line.
        #8    Treat the image as a single word.
        #9    Treat the image as a single word in a circle.
        #10   Treat the image as a single character.

        #11    Sparse text. Find as much text as possible in no particular order.
        #12    Sparse text with OSD.
        #13    Raw line. Treat the image as a single text line


#4 Definisco le dimensioni dell'oggetto kernel che scorre sull'immagine da sinistra a destra
Runner = np.ones((1, 1), np.uint8)

#5 L'erosione viene utilizzata per rilevare se il kernel contiene pixel bianchi in primo piano
# o pixel di sfondo nero. Se il kernel è pieno di pixel bianchi, il pixel nell'immagine originale
# sarà considerato 1 e quindi bianco. Se il kernel contiene pixel neri, il pixel originale sarà considerato nero.
# Visto però che ho scelto un kernel delle dimensioni di un pixel, il risultato sarà o 0 o 1 (precisione aumentata)
# Di conseguenza, le linee bianche vengono erose.

img = cv2.erode(gray, Runner, iterations=1)

#6 Stessa cosa dell'erosione solo che dilata le parti bianche facendo risaltare quelle nere
img = cv2.dilate(img, Runner, iterations=1)

# 7 Converte l'immagine modificata in stringhe di testo
out_below = pytesseract.image_to_string(img)
print("OUTPUT:", out_below)


#cv2.imshow("Img", img)
cv2.waitKey(0)

Messaggio = input("INSERISCI txt o Excel: ")
# 8 Copia i dati in un file di testo.
# w : Write (Scrive dati)
# a : Append (aggiunge dei dati in coda in un file contenente altri dati)


#Ciclo if per esportare i dati su txt o Excel. Su Excel ho ancora dei problemi :(
if Messaggio == "txt":
    file_txt = open("Export_dati.txt", "w")
    file_txt.write(out_below)
    file_txt.close()

    file_txt = open("Export_dati.txt", "a")
    file_txt.write("\nENJOY!")
    file_txt.close()

elif Messaggio == "Excel":
    nuovo_file = openpyxl.Workbook()
    sheet = nuovo_file.active
    sheet.title = 'Foglio1'

    sheet['A1']="CIAO"
    nuovo_file.save('Export_dati.xlsx')
    nuovo_file.close()
