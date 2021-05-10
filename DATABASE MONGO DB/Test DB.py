import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["Cantine_Maschio_DB"]

mycol = mydb["Michelet"]

mydb.mycoll.insert(trans1.to_dict())