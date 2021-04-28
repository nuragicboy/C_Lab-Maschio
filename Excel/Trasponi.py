""""#Aggiungo una riga per permettere l'indicizzazione completa del dataframe
from openpyxl import load_workbook
wb = load_workbook('Michelet.xlsx')
ws = wb.active
ws.insert_rows(1, amount=1)
wb.save("Michelet#1.xlsx")"""

import pandas as pd

#Faccio la trasposta del dataframe per posizionare gli articoli sulle righe anzichè sulle colonne
df = pd.read_excel('Michelet.xlsx', sheet_name='Sheet1')
trans = df.T
"""T1 = Trans.fillna(value=0.0)
# Tutti i valori nulli nella seconda riga vengono sostituiti con i medesimi della riga precedente
for i in range(0,len(df),1):
    if T1.iloc[1,i]==0:
        T1.iloc[1,i]=T1.iloc[0,i]"""

#Elimino la seconda riga
trans.drop(trans.index[1:2], inplace=True)

#Scrivo su file
trans.to_excel('Michelet#2.xlsx', header=False)


