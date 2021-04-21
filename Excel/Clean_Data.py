import pandas as pd
import numpy as np

# Carica il file dalla stessa directory di Python
df = pd.read_excel('..\Excel\Michelet.xlsx', sheet_name='Sheet1')

# Traspone la tabella convertendola in formato xlsx
Trans = df.T

Trans.to_excel('Out3.xlsx')



def Clean_Data():
    # Copia le prime 17 celle della seconda riga nella terza per eliminare gli spazi vuoti
    for i in range(0,18,1):
    Trans.iloc[1,i]=Trans.iloc[0,i]
    Trans.to_excel('Clean1.xlsx')
    # Eliminare la seconda riga che non serve ad un tubo

