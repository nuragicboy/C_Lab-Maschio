import pandas as pd

#Faccio la trasposta del dataframe per posizionare gli articoli sulle righe anzichè sulle colonne
df = pd.read_excel('Michelet.xlsx', sheet_name='Sheet1')

#ELIMINA PUNTI DALLA PRIMA COLONNA CHE UNA VOLTA TRASPOSTA SARA' L'INTESTAZIONE.
df['Codice'] = df['Codice'].str.replace('.','')
print(df)





#INDIVIDUA COLONNE CONTENENTI PUNTI
#Dot=trans1.filter(like='.', axis=1)

#Dot.to_excel("Elimina punti.xlsx")