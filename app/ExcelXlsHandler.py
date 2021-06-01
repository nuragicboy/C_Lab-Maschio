import pandas as pd

def readFile(file, sheet="Sheet1"):
    return pd.read_excel(file, sheet_name=sheet)

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

def writeLocal(file, name, path="", header=True):
    file.to_excel(path+name, header=header)

def toXMLString(file):
    return file.to_json(orient='records')