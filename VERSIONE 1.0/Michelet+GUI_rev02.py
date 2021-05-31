import datetime
import json
import numpy as np
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import pymongo
import time

file=''

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.FileImport()
        self.master = master
        self.pack()
        self.create_widgets()
        self.create_widgets2()
        self.Py_Mongo()

    def FileImport(self):
        #global file
        self.file = filedialog.askopenfilename()
        self.label=tk.Label(root, text="Selected:"+file).pack()
        self.label=tk.Label(root, text="Upload a file:", fg="purple").pack()
        self.button=tk.Button(root, text='Upload',fg="blue", command=self.FileImport)
        self.button.pack(side="top")

        self.uploaded_file = np.fromfile(self.file)

        self.df = pd.read_excel(self.file, sheet_name='Sheet1')

    # SOSTITUISCE I PUNTI COL NULLA NELLA PRIMA COLONNA CHE UNA VOLTA TRASPOSTA DIVENTERà L'INTESTAZIONE

        self.df['Codice'] = self.df['Codice'].str.replace('.', '', regex=False)

        # Faccio la trasposta del dataframe per posizionare gli articoli sulle righe anzichè sulle colonne
        self.trans = self.df.T

        # Elimino la seconda riga
        self.trans.drop(self.trans.index[1:2], inplace=True)

        # Resetto l'indice di riga con numeri interi. In questo modo è possibile indicizzare anche il codice prodotto
        # trans.reset_index(inplace=True)

        # Trasformo la prima riga nell'intestazione di colonna
        self.headers = self.trans.iloc[0]
        self.trans1 = pd.DataFrame(self.trans.values[1:], columns=self.headers)

        # Elimino colonne tramite etichetta

        self.columns = ['Attività', 'Attività - Matrice', 'Descrizione', 'Locazione', 'Prodotto', 'Assegnato', 'Stampa']
        self.trans1.drop(self.columns, inplace=True, axis=1)

        # Elimino i punti dalle intestazioni altrimenti non possiamo inserire il file nel DB (Andrebbe creato un codice generico e non
        # specifico per l'etichetta (modulo replace)

        # old_value=[2,3,4,54,55,58,59]
        # new_value=["N Vasca","N Lotto","N Partita","calcio limite max sec Ridomi mg/l","potassio ad equilibrio raggiunto sec Ridomi g/l","decremento acidità totale sec Ridomi g/l","pH ad equilibrio raggiunto sec Ridomi"]

        # for i in range(0,7,1):
        # trans1.columns.values[old_value[i]]=new_value[i]

        # Scrivo su file
        self.trans1.to_excel('Michelet#2.xlsx', header=True)

        # Converto il dataframe in formato json
        self.F1 = json.loads(self.trans1.to_json(orient='records'))

    def create_widgets(self):
        self.verifica = tk.Button(self)
        self.verifica["text"] = "VERIFICA"
        self.verifica["command"] = self.Prova
        self.verifica.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def Prova(self):
        print(self.F1)

    def Py_Mongo(self):
        self.client = pymongo.MongoClient(
            "mongodb+srv://Albert:112358@maschio.enbsn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db =self.client.Analisi_Laboratorio

        self.col = self.db["MICHELET"+" "+time.strftime("%d/%m/%Y")]

    def create_widgets2(self):
        self.verifica = tk.Button(self)
        self.verifica["text"] = "CONNETTI MONGO"
        self.verifica["command"] = self.Mongo_Connect
        self.verifica.pack(side="bottom")
    def Mongo_Connect(self):
        self.x = self.col.insert_many(self.F1)
        print('DATI INSERITI CON SUCCESSO!')

root = tk.Tk()
app = Application(master=root)
app.mainloop()


#Trova=col.find_one({"Codice":"20-LM06395"})

#print(Trova)

# result = client['Analisi']['Michelet#2'].aggregate([
#     {
#         '$match': {
#             'Acetaldeide enzimatico mg/l': {
#                 '$lt': 70,
#                 '$gt': 62
#             }
#         }
#     }
# ])
#
# # Non da errore ma non so che fine faccia questo filtro -_-