import pandas as pd
import numpy as np

# Carica il file dalla stessa directory di Python
df = pd.read_excel('..\Excel\Michelet.xlsx', sheet_name='Sheet1')

# Traspone la tabella convertendola in formato xlsx
Trans = df.T

Trans.replace('Codice', 'CODICE', regex=True, inplace=True)

Trans.to_excel('Out2.xlsx')

# Analisi statistiche automatiche e copia su file excel
D = Trans.describe()
D.to_excel('Stat_Analysys.xlsx')

# Ordina le righe in ordine alfabetico dal basso verso l'alto. Con true fa il contrario
Ord_righe = Trans.sort_index(axis=0, ascending=False)

# Ordina le colonne in ordine alfabetico dal basso verso l'alto. Con true fa il contrario
Ord_colonne = Trans.sort_index(axis=1, ascending=False)

# Seleziona tutte le righe ma solo due colonne (i numeri sono gli indici stampati nella prima riga del file Out2)
Sel = Trans.loc[:, [0,2]]
print(Sel)

# Seleziona un singolo elemento all'interno del DF
Elem = Trans.iloc[2,3]
print(Elem)

