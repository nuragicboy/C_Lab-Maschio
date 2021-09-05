import pandas as pd
import re

def readXLS(file, sheet=0, header=0):
    return pd.read_excel(file, sheet_name=sheet, header=header)

def readCSV(file, header=0, skiprows=0, separator=";", notifyErrors=False):

    return pd.read_csv(file, header=header, sep=separator, skiprows=skiprows, error_bad_lines=notifyErrors, engine='python', encoding='UTF-16')

def transpose(file):
    return file.T

def dropRowByIndex(file, index, inplace=True):
    file.drop(file.index[index], inplace=inplace)
    return file

def dropColumnsByName(file, columns):
    file.drop(columns, inplace=True, axis=1)
    return file

def setFirstRowAsHeader(file):
    headers = file.iloc[0]
    return pd.DataFrame(file.values[1:], columns=headers)

def renameHeaderByIndex(file, index, newValues):
    for i in range(0, len(index)):
        file.columns.values[int(index[i])] = newValues[i]
    return file

def renameHeader(file, dict):
    print(type(file))
    writeLocal(file, "BUGO"".xlsx", "Test/", header=True)
    return file.rename(columns=dict)

def updateData(file, column, data):
    print(file)
    print(data)
    writeLocal(file, "testUpdate"".xlsx", "Test/", header=True)
    file[column].replace(data, inplace=True)
    print(file)
    writeLocal(file, "testUpdate"".xlsx", "Test/", header=True)
    return file
"""
def renameHeader(file, oldNames, newNames):
    pairings=dict(zip(oldNames, newNames))
    file.rename(columns=pairings)
    return file
"""

def writeLocal(file, name, path="", header=True):
    file.to_excel(path+name, header=header, merge_cells=False)

def toXMLString(file):
    return file.to_json(orient='records')

def addStaticColumn(file, column, value):
    for col in column:
        file[column]=value
    return file

def removeExtraColumns(file, list):
    print ("i seguenti campi non hanno corrispondenze e verranno scartati:\n ")
    print(file.columns.difference(list))
    #print (file.columns.intersection(list))
    return file[file.columns.intersection(list)]

def fill(file,keys,columns):
    file[columns] = file.groupby(keys, sort=False)[columns].apply(lambda x: x.ffill().bfill())
    return file

def removeDBDuplicates(file,column, keys):
    print(keys)
    print("\n")
    print(file[column])
    print("\n")
    print(file[column].isin(keys))
    print("\n")
    print(file[~file[column].isin(keys)])
    print("\n")
    print("\n")
    return file[~file[column].isin(keys)]

def dropNullFromColumn(file, columns):
    return file.dropna(subset=columns)

def transposeKeyValues(file, ind, keyColumn, valuesColumn):
    columns = list(dict.fromkeys(file[keyColumn]))
    #print(colonne)
    print(ind)
    newFile = file.copy()

    dropColumnsByName(newFile, [keyColumn, valuesColumn])
    newFile = newFile.drop_duplicates()
    newFile = addStaticColumn(newFile, columns, None)

    newFile.set_index(ind)
    writeLocal(file, "aggColonne"".xlsx", "Test/", header=True)

    for index, row in file.iterrows():
        """
        print(ind)
        print(newFile[ind])
        print("\n")
        print(row[keyColumn])
        print("\n")
        print(newFile[str(row[keyColumn])])
        print("\n\n\n\n\n")
        """
        newFile.loc[newFile[ind] == row[ind], row[keyColumn]] = row[valuesColumn]
    return newFile

def test(file):


    #droppo i valori null nella colonna x
    file=dropNullFromColumn(file,['PROVA'])

    #trasporto i valori di colonna x come colonne e li valorizzo con i valori di colonna y in base ai valori di colonna z
    file=transposeKeyValues(file,'RDP','PROVA','VALORE')
    """    
    colonne = list(dict.fromkeys(file["PROVA"]))
    print(colonne)

    newFile = file.copy()

    dropColumnsByName(newFile, ["PROVA","VALORE"])
    newFile=newFile.drop_duplicates()
    newFile=addStaticColumn(newFile, colonne, None)

    newFile.set_index("RDP")
    writeLocal(file, "aggColonne"".xlsx", "Test/", header=True)


    for index, row in file.iterrows():
        print(newFile['RDP'])
        print("\n")
        print(row["PROVA"])
        print("\n")
        print(newFile[str(row["PROVA"])])
        print("\n\n\n\n\n")
        newFile.loc[newFile['RDP'] == row['RDP'], row["PROVA"]] = row["VALORE"]

    """
    writeLocal(file, "definitivo"".xlsx", "Test/", header=True)
    return file