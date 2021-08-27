import pandas as pd

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
    return file.rename(columns=dict)

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
    file[column]=value

def removeExtraColumns(file, list):
    print (file.columns.difference(list))
    print (file.columns.intersection(list))
    return file[file.columns.intersection(list)]
