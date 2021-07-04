import json

import pandas as pd

#Faccio la trasposta del dataframe per posizionare gli articoli sulle righe anzichè sulle colonne
df = pd.read_excel('Vini_Finiti.xlsx', sheet_name='Foglio1')
df.reset_index(inplace=False)

df.to_excel('Vini_Finit#2.xlsx',header=True)
F1=json.loads(df.to_json(orient='records'))

import pymongo



client = pymongo.MongoClient("mongodb+srv://Albert:112358@maschio.enbsn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.Analisi

print("connesso in teoria")

col = db["File Vini"]

x = col.insert_many(F1)