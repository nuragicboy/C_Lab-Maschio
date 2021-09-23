import json
import traceback
import pandas

from MySQLConnector import MySQLConnector
import PandasHandler as pd
import datetime


class Orchestrator:
    def __init__(self, dataPath, profileName="Michelet"):
        self.timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.dataPath = dataPath
        self.profileName=profileName
        with open('conf.json', encoding='utf-8') as f:
            self.conf = json.load(f)

        with open(self.conf["Profiles"], encoding='utf-8') as f:
            self.profile = json.load(f)[self.profileName]

    def run(self):
        try:
            conn = self.conf["RemoteConnections"]["digitalocean"]
        except:
            err = "errore: la connessione non esiste nelle configurazioni" + traceback.format_exc()
            return [-1, err]
        self.dab = MySQLConnector(conn)
        self.status=[0,""]
        test = 0


        for step in self.profile["steps"]:

            if (step["action"] == "readExcel"):
                try:
                    self.excelData = pd.readXLS(self.dataPath)
                except:
                    err="Errore nella lettura del file\n\n"+traceback.format_exc()
                    return[-1,err]

            elif (step["action"] == "readCSV"):
                try:
                    self.excelData = pd.readCSV(self.dataPath, skiprows=step["SkipRows"])
                except:
                    err="Errore nella lettura del file\n\n"+traceback.format_exc()
                    return[-1,err]

            elif (step["action"] == "translateColumns"):
                try:
                    self.excelData = self.translateColumns()
                except:
                    err="Errore durante la rinominazione delle colonne\n\n"+traceback.format_exc()
                    return[-1,err]

            elif (step["action"] == "transpose"):
                try:
                    self.excelData = pd.transpose(self.excelData)
                except:
                    err="Errore durante la trasposta del dataframe\n\n"+traceback.format_exc()
                    return[-1,err]

            elif (step["action"] == "drop"):
                try:
                    self.excelData = pd.dropRowByIndex(self.excelData, int(step["rownum"]))
                except:
                    err="Errore durante l'eliminazione delle colonne\n\n"+traceback.format_exc()
                    return[-1,err]

            elif (step["action"] == "header"):
                try:
                    self.excelData = pd.setFirstRowAsHeader(self.excelData)
                except:
                    err="Errore durante l'aggiunta delle intestazioni delle colonne\n\n"+traceback.format_exc()
                    return[-1,err]

            elif (step["action"] == "delColByName"):
                try:
                    self.excelData = pd.dropColumnsByName(self.excelData, step["columns"])
                except:
                    err="Errore durante l'eliminazione delle colonne\n\n"+traceback.format_exc()
                    return[-1,err]

            elif (step["action"] == "renameColumn"):
                try:
                    self.excelData = pd.renameHeaderByIndex(self.excelData, step["columnNumber"], step["newName"])
                except:
                    err="Errore durante la rinominazione delle colonne\n\n"+traceback.format_exc()
                    return[-1,err]

            elif (step["action"] == "dropNullFromColumn"):
                try:
                    self.excelData = pd.dropNullFromColumn(self.excelData, step["columns"])
                except:
                    err="Errore durante l'eliminazione delle righe contenenti valori nulli\n\n"+traceback.format_exc()
                    return[-1,err]

            elif (step["action"] == "transposeKeyValues"):
                try:
                    self.excelData = pd.transposeKeyValues(self.excelData, step["index"],step["keyColumn"],step["valuesColumn"])
                except:
                    err="Errore durante la trasposta delle colonne chiave in intestazioni\n\n"+traceback.format_exc()
                    return[-1,err]

            elif (step["action"] == "removeDBDuplicates"):
                """
                try:
                    self.excelData = self.removeDBDuplicates(step)
                    if self.excelData.empty:
                        msg = "il documento contiene solamente righe già presenti nel db"
                        return [-1, msg]
                except:
                    err="Errore durante la rimozione dei duplicati\n\n"+traceback.format_exc()
                    return[-1,err]
                """
                pass

            elif (step["action"] == "updateDataFromDB"):
                try:
                    self.excelData = self.updateDataFromDB(step)
                except:
                    err="Errore durante l'update dei dati tramite db\n\n"+traceback.format_exc()
                    return[-1,err]



            elif (step["action"] == "fill"):
                try:
                    self.excelData = pd.fill(self.excelData, step["keys"],step["columns"])
                except:
                    err="Errore durante il fill dei campi vuoti\n\n"+traceback.format_exc()
                    return[-1,err]

            else:
                err = "azione "+step["action"]+" inesistente, verificare il profilo e riprovare"
                return [-1, err]


            test += 1

            pd.writeLocal(self.excelData, self.profileName + str(test) + str(step["action"]) + ".xlsx", "Test/",header=True)

        if self.profile["options"]["TranslateColumnsBeforeLoading"] == True:
            try:
                self.translateColumns()
            except:
                err="Errore durante la rinomiazione delle colonne tramite dizonario del db\n\n"+traceback.format_exc()
                return[-1,err]

        if self.profile["options"]["AddProfileColumn"] == True:
            try:
                pd.addStaticColumn(self.excelData,self.profile["options"]["ProfileColumn"],self.profileName)
            except:
                err="Errore durante l'aggiunta della colonna profilo\n\n"+traceback.format_exc()
                return[-1,err]

        if self.profile["options"]["AddTimestamp"] == True:
            try:
                pd.addStaticColumn(self.excelData,self.profile["options"]["TimestampColumn"],self.timestamp)
            except:
                err="Errore durante l'aggiunta del timestamp\n\n"+traceback.format_exc()
                return[-1,err]

        pd.writeLocal(self.excelData, "PREaaaaaaaa.xlsx", "Test/",
                      header=True)

        if self.profile["options"]["RemoveExtraColumns"] == True:
            try:
                self.excelData, columns=self.removeExtraColumns()
                if len(columns) != 0:
                    if self.profile["options"]["OnMismatchedColumns"]=="Notify":
                        self.status[0]=1
                        self.status[1]+="Le seguenti colonne non hanno corrispondenza e non sono state caricate:\n"+str(columns)
                    elif self.profile["options"]["OnMismatchedColumns"] == "Abort":
                        err = "Caricamento annullato: la configurazione contiene OnMismatchedColumns = Abort e nel file sono presenti colonne non presenti nel db:\n"+str(columns)
                        return [-1, err]
            except:
                err="Errore durante l'eliminazione delle colonne extra:\n\n"+traceback.format_exc()
                return[-1,err]

        pd.writeLocal(self.excelData, "aaaaaaaa.xlsx", "Test/",
                      header=True)

        for step in self.profile["analysis"]:
            if (step["action"] == "checkRange"):
                #print("entro in checkRange")
                #print(self.excelData)
                try:
                    self.excelData = self.checkRange(step)
                except:
                    err="Errore durante l'update dei dati tramite db\n\n"+traceback.format_exc()
                    print(err)
                    return[-1,err]


        """
        #print(self.excelData)
        if not self.excelData.empty():
            try:
                self.dab.insertTable(self.excelData, "analisi")
                self.dab.insertTable(pandas.DataFrame({"file":[self.dataPath], "dataora": [self.timestamp]}), "storico")
                #print("dati caricati sul db per il file "+self.dataPath)
            except:
                err="Errore durante il caricamento dei dati nel database\n\n"+traceback.format_exc()
                return[-1,err]
        """
        return self.status

    def translateColumns(self):
        query="select campo_lab,campo_interno from dizionario where lab in ('"+self.profileName+"','all')"
        results=self.dab.select(query)
        columnNames= {str(row[0]): str(row[1]) for row in results}
        return pd.renameHeader(self.excelData, columnNames)

    def updateDataFromDB(self,step):
        query="select Denominazione,\"nome interno\" from denominazioni where Laboratorio in ('"+self.profileName+"','all')  and (\"nome interno\" is not null AND \"nome interno\" != '')"
        print(query)
        results=self.dab.select(query)
        dict= {str(row[0]): str(row[1]) for row in results}
        return pd.updateData(self.excelData, step["column"], dict)

    def removeDBDuplicates(self,step):

        query="select distinct \""+str(step["DBColumn"])+"\" from analisi where Laboratorio ='"+self.profileName+"'"
        #print(query)
        results=self.dab.select(query)
        #print(results)
        keys= {str(row[0]) for row in results}
        return pd.removeDBDuplicates(self.excelData,step["dataColumn"], keys)

    def removeExtraColumns(self):
        query="select campo_interno from dizionario where lab in ('"+self.profileName+"','all')"
        results=self.dab.select(query)
        columnNames= {str(row[0]) for row in results}
        return pd.removeExtraColumns(self.excelData, columnNames)

    def checkRange(self,step):
        #print("checkRange")
        query="select * from soglie_test"
        results=self.dab.select(query)
        columnNames= {str(row[0]) for row in results}
        return pd.between(self.excelData, results)

"""
        for key in dict:
            print(key)
            print(key in self.excelData)

            print(dict[key])
            print(dict[key] in newExcel)
            print("---")

        return newExcel
"""
