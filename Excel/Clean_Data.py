import pandas as pd
import numpy as np

# Carica il file dalla stessa directory di Python
df = pd.read_excel('..\Excel\Michelet.xlsx', sheet_name='Sheet1')
# Traspone la tabella convertendola in formato xlsx
Trans = df.T

Trans.to_excel('Out3.xlsx')

# Copia le prime 17 celle della seconda riga nella terza per eliminare gli spazi vuoti
for i in range(0,18,1):
    Trans.iloc[1,i]=Trans.iloc[0,i]
    # Riempe le celle vuote con degli zero
    T1 = Trans.fillna(value=0.0)
    # Elimina la seconda riga, ormai fotocopia di quella sotto
    T1.drop('Codice',inplace=True)

   #NOTA: La colonna A è come se non esistesse, non c'è modo di modificarla. Ste' pensaci tu! XD
    T1.to_excel('Clean1.xlsx')

