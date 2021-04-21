import tabula
import pandas as pd

#Legge la tabella in formato pdf e crea un dataframe
df = tabula.read_pdf('../data-1.pdf', pages=3, lattice=True) [1]

#Elimina i valori "/r" nelle intestazioni
df.columns = df.columns.str.replace('\r', ' ')

#Stampa le intestazioni per vedere se ci sono altre cose strane
print(df.columns)

#Sostituisce lo zero al posto degli "NA"
data = df.dropna()

#Invia i dati ad un foglio Excel
data.to_excel('Test_Tabula.xlsx')

#Invoco il Panda per leggere tale file
MyExcel = pd.ExcelFile('Test_Tabula.xlsx')

#Riporto su Python la tabella creata su Excel
data1 = MyExcel.parse('Sheet1')

#Stampo tale tabella
print(data1)

