import pymongo
from pymongo import MongoClient

# Eseguo la conessione con MongoDB
client = MongoClient('localhost', 27017)

# Creo un database e lo chiamo TestDB
db = client.testdb

# Creo la collection "persone"
persone_coll = db.persone

# Creo un sistema di indicizzazione
persone_coll.create_index([("nome", pymongo.ASCENDING)])
persone_coll.create_index([("cognome", pymongo.ASCENDING)])
persone_coll.create_index([("computer", pymongo.ASCENDING)])

# Creo un documento
p1 = {"nome": "Mario", "cognome": "Rossi", "eta": 30,
        "computer": ["asus","apple"]}

# Inseriamo il documento in MongoDB
persone_coll.insert_one(p1)

# Creo un documento
p2 = {"nome": "Giuseppe", "cognome": "Verdi", "eta": 45,
        "computer": ["apple"]}

# Inseriamo il documento in MongoDB
persone_coll.insert_one(p2)

