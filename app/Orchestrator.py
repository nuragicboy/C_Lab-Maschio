import json
from MySQLConnector import MySQLConnector
import PandasHandler as pd
import datetime


class Orchestrator:
    def __init__(self, dataPath, profileName="Michelet"):
        self.dataPath = dataPath
        self.profileName=profileName
        with open('conf.json', encoding='utf-8') as f:
            self.conf = json.load(f)

        with open(self.conf["Profiles"], encoding='utf-8') as f:
            self.profile = json.load(f)[self.profileName]

    def run(self):
        conn = self.conf["RemoteConnections"]["digitalocean"]
        self.dab = MySQLConnector(conn)
        test = 0


        for step in self.profile["steps"]:

            if (step["action"] == "readExcel"):
                self.excelData = pd.readXLS(self.dataPath)

            elif (step["action"] == "readCSV"):
                self.excelData = pd.readCSV(self.dataPath, skiprows=step["SkipRows"])

            elif (step["action"] == "translateColumns"):
                self.excelData = self.translateColumns()

            elif (step["action"] == "transpose"):
                self.excelData = pd.transpose(self.excelData)

            elif (step["action"] == "drop"):
                self.excelData = pd.dropRowByIndex(self.excelData, int(step["rownum"]))

            elif (step["action"] == "header"):
                self.excelData = pd.setFirstRowAsHeader(self.excelData)

            elif (step["action"] == "delColByName"):
                self.excelData = pd.dropColumnsByName(self.excelData, step["columns"])

            elif (step["action"] == "renameColumn"):
                self.excelData = pd.renameHeaderByIndex(self.excelData, step["columnNumber"], step["newName"])

            elif (step["action"] == "dropNullFromColumn"):
                self.excelData = pd.dropNullFromColumn(self.excelData, step["columns"])

            elif (step["action"] == "dropNullFromColumn"):
                self.excelData = pd.dropNullFromColumn(self.excelData, step["columns"])

            elif (step["action"] == "transposeKeyValues"):
                self.excelData = pd.transposeKeyValues(self.excelData, step["index"],step["keyColumn"],step["valuesColumn"])

            elif (step["action"] == "removeDBDuplicates"):
                self.excelData = self.removeDBDuplicates(step)

            elif (step["action"] == "updateDataFromDB"):
                self.excelData = self.updateDataFromDB(step)

            else:
                print("azione "+step["action"]+" inesistente, verificare il profilo e riprovare")
                exit()


            test += 1

            pd.writeLocal(self.excelData, self.profileName + str(test) + str(step["action"]) + ".xlsx", "Test/",header=True)

        if self.profile["options"]["TranslateColumnsBeforeLoading"] == True:
            self.translateColumns()

        if self.profile["options"]["AddProfileColumn"] == True:
            pd.addStaticColumn(self.excelData,self.profile["options"]["ProfileColumn"],self.profileName)

        if self.profile["options"]["AddTimestamp"] == True:
            timestamp=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            pd.addStaticColumn(self.excelData,self.profile["options"]["TimestampColumn"],timestamp)

        if self.profile["options"]["AllowMismatchedColumns"] == False:
            self.excelData=self.translateColumns()
            self.excelData=self.removeExtraColumns()

        #self.dab.insertTable(self.excelData, "analisi")
        print("dati caricati sul db per il file "+self.dataPath)

    def translateColumns(self):
        query="select campo_lab,campo_interno from dizionario where lab in ('"+self.profileName+"','all')"
        results=self.dab.select(query)
        columnNames= {str(row[0]): str(row[1]) for row in results}
        return pd.renameHeader(self.excelData, columnNames)

    def updateDataFromDB(self,step):
        query="select denominazione,'nome interno' from denominazioni where Laboratorio in ('"+self.profileName+"','all')"
        results=self.dab.select(query)
        dict= {str(row[0]): str(row[1]) for row in results}
        return pd.updateData(self.excelData, step["column"], dict)

    def removeDBDuplicates(self,step):
        query="select distinct '"+str(step["DBColumn"])+"' from analisi where Laboratorio ='"+self.profileName+"'"
        results=self.dab.select(query)
        keys= {str(row[0]) for row in results}
        return pd.removeDBDuplicates(self.excelData,step["dataColumn"], keys)

    def removeExtraColumns(self):
        query="select campo_interno from dizionario where lab in ('"+self.profileName+"','all')"
        results=self.dab.select(query)
        columnNames= {str(row[0]) for row in results}
        return pd.removeExtraColumns(self.excelData, columnNames)


"""
        for key in dict:
            print(key)
            print(key in self.excelData)

            print(dict[key])
            print(dict[key] in newExcel)
            print("---")

        return newExcel
"""
