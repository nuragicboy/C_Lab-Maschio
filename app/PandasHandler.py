import pandas as pd
import re

def readXLS(file, sheet=0, header=0):
    return pd.read_excel(file, sheet_name=sheet, header=header)

def readCSV(file,header=0, skiprows=0, separator=";", notifyErrors=False):
    return pd.read_csv(file, header=header, sep=separator, skiprows=skiprows, error_bad_lines=notifyErrors, engine='python', encoding='UTF-16')

def readCSVCharLimit(file, columns, sep=";", rowLimit=255,header=0, skiprows=0, separator=";", notifyErrors=False):
    buf=""
    discarded=0
    #print(columns)
    with open(file, encoding='utf-16') as inf, open("edited.csv", 'w',encoding='utf-16') as outf, open("discarded.csv", "w",encoding='utf-16') as outd:
        for _ in range(skiprows):
            outf.write(inf.readline())

        for line in inf:
            #print(len(line.split(sep)))
            #print(len(line))
            #print(line)

            if len(buf)==0:
                if len(line.split(sep)) > columns:
                    #print("troppo lungo")
                    outd.write(line)
                    discarded += 1
                elif len(line.split(sep)) < columns and (len(line)>=rowLimit):
                    #print("aggiungo a buf")
                    buf += line.replace('\n', '');
                else:
                    #print("scrivo cossì")
                    outf.write(line)

            else:
                #print(len(line.split(sep))+len(buf.split(sep)))
                if len(line.split(sep))+len(buf.split(sep)) < columns+1:
                    buf += line.replace('\n', '');
                    #print("cortino dio canino")
                elif len(line.split(sep))+len(buf.split(sep)) == columns+1:
                    #print("lunghezza okay,stampo buf")
                    buf += line
                    outf.write(buf)
                    buf=""
                elif len(line.split(buf))+len(buf.split(file)) > columns+1:
                    #print("troppo lungo")
                    buf += line
                    outd.write(buf)
                    buf=""
                    discarded += 1
                #else:
                    #print("bohhh")
            #print("-----------------------------------------------------")

        """
            # check if the number of "splits equals the nummber of fields"
            if len(line.split(sep)) > columns:
                print("troppo lungo")
                outd.write(line)
                discarded+=1
            else:
                if len(line.split(sep)) < columns and (len(line)>=rowLimit or len(buf)>0):
                    print("aggiungo a buf")
                    buf += line.replace('\n', '');
                if len(line.split(buf)) == columns:
                    print("lunghezza okay,stampo buf")
                    outf.write(buf)
                    buf=""
                else:
                    outf.write(line)
        """
    return pd.read_csv("edited.csv", header=header, sep=separator, skiprows=skiprows, error_bad_lines=notifyErrors, engine='python', encoding='UTF-16')

def transpose(file):
    return file.T

def dropRowByIndex(file, index, inplace=True):
    file.drop(file.index[index], inplace=inplace)
    return file

def dropColumnsByName(file, columns):
    #print(columns)
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
    #print(type(file))
    #print(dict)
    writeLocal(file, "BUGO"".xlsx", "Test/", header=True)
    f= file.rename(columns=dict)
    '''
    for key, value in dict.items():
        if key in file:
            print("rinomino "+key+ " "+ value)
            f.rename(columns={key:value}, inplace=True)
    '''
    writeLocal(f, "POSTBUGO"".xlsx", "Test/", header=True)
    return f

def updateData(file, column, data):
    #print(file)
    #print(data)
    writeLocal(file, "testUpdate"".xlsx", "Test/", header=True)
    file[column].replace(data, inplace=True)
    #print(file)
    writeLocal(file, "testUpdate2"".xlsx", "Test/", header=True)
    return file

def writeLocal(file, name, path="", header=True):
    file.to_excel(path+name, header=header, merge_cells=False)

def toXMLString(file):
    return file.to_json(orient='records')

def addStaticColumn(file, column, value):
    for col in column:
        file[column]=value
    return file

def removeExtraColumns(file, list):
    #print ("i seguenti campi non hanno corrispondenze e verranno scartati:\n ")
    #print(file.columns)
    #print(list)
    #print(file.columns.difference(list))
    #print (file.columns.intersection(list))
    return file[file.columns.intersection(list)], file.columns.difference(list)

def fill(file,keys,columns):
    for column in columns:
        file[column] = file.groupby(keys, sort=False)[column].apply(lambda x: x.ffill().bfill())
    return file

def removeDBDuplicates(file,column, keys):
    #print(keys)
    #print("\n")
    #print(file[column])
    #print("\n")
    #print(file[column].isin(keys))
    #print("\n")
    #print(file[~file[column].isin(keys)])
    #print("\n")
    #print("\n")
    return file[~file[column].isin(keys)]

def takeFirstPerGroup(file, column):
    return file.groupby(column).first().reset_index()

def dropNullFromColumn(file, columns):
    return file.dropna(subset=columns)

def transposeKeyValues(file, ind, keyColumn, valuesColumn):
    columns = list(dict.fromkeys(file[keyColumn]))
    #print(colonne)
    #print(ind)
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

def between(file, values):
    #print("sono in between")
    copy=file.fillna(-1)
    #print(copy['Denominazione'])
    elapsed=[]
    over=[]
    for v in values:
        if v[1] in copy.columns:
            if v[1] not in elapsed:
                copy[v[1]] = copy[v[1]].astype(str)
                copy.loc[copy[v[1]].str.contains('<|%'), v[1]] = -1
                copy[v[1]] = copy[v[1]].astype(float)
                elapsed.append(v[1])

            rslt_df = copy[(copy['Denominazione'].str.contains(v[0])) & (copy[v[1]]!=-1) & ((copy[v[1]]>float(v[2].replace(',','.'))) | (copy[v[1]]<float(v[3].replace(',','.'))))]
            if not rslt_df.empty:
                for index, r in rslt_df.iterrows():
                    over.append([r['Codice Laboratorio'],r['Denominazione'],v[1],r[v[1]],v[2],v[3]])
    return over