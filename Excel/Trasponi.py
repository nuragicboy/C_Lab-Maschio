import pandas as pd

#Faccio la trasposta del dataframe per posizionare gli articoli sulle righe anzichè sulle colonne
df = pd.read_excel('Michelet.xlsx', sheet_name='Sheet1')
trans = df.T

#Elimino la seconda riga
trans.drop(trans.index[1:2], inplace=True)

#Scrivo su file
trans.to_excel('Michelet#2.xlsx', header=False)


