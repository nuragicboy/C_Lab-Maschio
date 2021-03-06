import json
import numpy as np
import tkinter as tk
from tkinter import filedialog
import pandas as pd

#Importo file da interfaccia grafica bruttissima ma funziona
def FileImport():
    global file
    file=filedialog.askopenfilename()
    label=tk.Label(root, text="SELEZIONARE:"+file).pack()

root=tk.Tk()
root.title('IMPORT FILE')
label=tk.Label(root, text="SELEZIONARE FILE:", fg="purple").pack()
button=tk.Button(root, text='SCEGLI',fg="blue", command=FileImport)
button.pack()

root.mainloop()
uploaded_file=np.fromfile(file)

df = pd.read_excel(file, sheet_name='Sheet1')

#SOSTITUISCE I PUNTI COL NULLA NELLA PRIMA COLONNA CHE UNA VOLTA TRASPOSTA DIVENTERà L'INTESTAZIONE

df['Codice'] = df['Codice'].str.replace('.','',regex=False)

#Faccio la trasposta del dataframe per posizionare gli articoli sulle righe anzichè sulle colonne
trans = df.T


#Elimino la seconda riga
trans.drop(trans.index[1:2], inplace=True)

#Resetto l'indice di riga con numeri interi. In questo modo è possibile indicizzare anche il codice prodotto
#trans.reset_index(inplace=True)

#Trasformo la prima riga nell'intestazione di colonna
headers = trans.iloc[0]
trans1 = pd.DataFrame(trans.values[1:], columns=headers)

#Elimino colonne tramite etichetta

columns = ['Attività', 'Attività - Matrice','Descrizione','Locazione','Prodotto','Assegnato','Stampa']
trans1.drop(columns, inplace=True, axis=1)

#Elimino i punti dalle intestazioni altrimenti non possiamo inserire il file nel DB (Andrebbe creato un codice generico e non
#specifico per l'etichetta (modulo replace)

#old_value=[2,3,4,54,55,58,59]
#new_value=["N Vasca","N Lotto","N Partita","calcio limite max sec Ridomi mg/l","potassio ad equilibrio raggiunto sec Ridomi g/l","decremento acidità totale sec Ridomi g/l","pH ad equilibrio raggiunto sec Ridomi"]

#for i in range(0,7,1):
    #trans1.columns.values[old_value[i]]=new_value[i]

#Scrivo su file
trans1.to_excel('Michelet#2.xlsx', header=True)

#Converto il dataframe in formato json
F1=json.loads(trans1.to_json(orient='records'))

#print(F1)

######### MONGO DB #########
import pymongo



client = pymongo.MongoClient("mongodb+srv://Albert:112358@maschio.enbsn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.Analisi

print("connesso in teoria")

col = db["Michelet#2"]

x = col.insert_many(F1)

#Trova=col.find_one({"Codice":"20-LM06395"})

#print(Trova)

result = client['Analisi']['Michelet#2'].aggregate([
    {
        '$match': {
            'Acetaldeide enzimatico mg/l': {
                '$lt': 70,
                '$gt': 62
            }
        }
    }
])

# Non da errore ma non so che fine faccia questo filtro -_-