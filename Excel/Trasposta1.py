import pandas as pd

# Carica il file dalla stessa directory di Python
df = pd.read_excel('..\Excel\Michelet.xlsx', sheet_name='Sheet1')

# Traspone la tabella convertendola in formato xlsx
df.T.to_excel('Out.xlsx', index= False)

# Rilegge il file appena creato in modo tale da poterlo modificare in locale sottoforma di dataframe
dft = pd.read_excel('Out.xlsx')


dft.replace('Codice', 'CODICE', regex=True, inplace=True)

dft.to_excel('Out2.xlsx')

print(dft)
