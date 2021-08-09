import pymongo

class MongoConnector:
    def __init__(self,client, db, collection, remote=True):
        self.client = pymongo.MongoClient("mongodb+srv://<username>:<password>@maschio.enbsn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.test
        self.db = self.client[db]
        self.collection = self.db[collection]

        if "maschio" not in self.client.list_database_names():
            print("The database doesn't exist")

        if "analisi" not in self.db.list_collection_names():
            print("The collection doesnt exist")


    def insert(self, data):
        return self.collection.insert_many(data)






