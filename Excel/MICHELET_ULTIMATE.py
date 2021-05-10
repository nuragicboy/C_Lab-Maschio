import pandas as pd

#Faccio la trasposta del dataframe per posizionare gli articoli sulle righe anzichè sulle colonne
df = pd.read_excel('Michelet.xlsx', sheet_name='Sheet1')

trans = df.T


#Elimino la seconda riga
trans.drop(trans.index[1:2], inplace=True)

#Resetto l'indice di riga con numeri interi. In questo modo è possibile indicizzare anche il codice prodotto
trans.reset_index(inplace=True)

#Trasformo la prima riga nell'intestazione di colonna
headers = trans.iloc[0]
trans1 = pd.DataFrame(trans.values[1:], columns=headers)

#Elimino colonne tramite etichetta

columns = ['Attività', 'Attività - Matrice','Descrizione','Locazione','Prodotto','Assegnato','Stampa']
trans1.drop(columns, inplace=True, axis=1)

#PROBLEMA: ci sono due intestazioni "codice", come faccio ad eliminarne solo 1?

#Scrivo su file
trans1.to_excel('Michelet#2.xlsx', header=True)




