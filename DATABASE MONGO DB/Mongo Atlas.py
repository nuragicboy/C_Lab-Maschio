# Installati pacchetti dnspython e Starlette

import pymongo

client = pymongo.MongoClient("mongodb+srv://unza:112358@maschio.enbsn.mongodb.net/test?retryWrites=true&w=majority")

#unza --> username del cluster, 112358 --> Password del cluster /test --> Nome del DB su Mongo Atlas in cui inserire i dati
db = client.test # Stesso nome di sopra

COLL = db["SONO UN GENIO"] #CREA LA COLLECTION

dizionario = { "nome": "Peter", "cognome": "Griffin" } #CREO IL DIZIONARIO DEI DATI

result = COLL.insert_one(dizionario) #INSERISCO I DATI


