import pandas as pd
import smtplib



#Faccio la trasposta del dataframe per posizionare gli articoli sulle righe anzichè sulle colonne
df = pd.read_excel('Vini_Finiti.xlsx', sheet_name='Foglio1')
df.reset_index(inplace=False)

df.to_excel('Vini_Finit#2.xlsx',header=True)

soglia=3.2

oggetto = "Subject: Attenzione! Valore fuori soglia\n\n"
messaggio = oggetto
#print(messaggio)


for i in range(1,len(df.index),1):
    if df.iloc[i,7]<soglia:
        #print("Indice:"+ str(i)+" "+"Codice:"+str(df.iloc[i,0]))
        parametro="Parametro analizzato : pH"
        contenuto = "Indice:"+ str(i+1)+"\n"+"Codice:"+str(df.iloc[i,0])
        valore="Valore:"+str(df.iloc[i,7])+" "+"-"+" "+"Soglia:"+str(soglia)
        messaggio = messaggio+parametro+"\n"+ contenuto+"\n"+valore+"\n\n"

print(messaggio)

email = smtplib.SMTP("smtp.gmail.com", 587)
email.ehlo()
email.starttls()
email.login("winenotcantinemaschio@gmail.com", "WineNot2021")
email.sendmail("winenotcantinemaschio@gmail.com", "alberto.carmignani1@gmail.com", messaggio)
email.quit()



