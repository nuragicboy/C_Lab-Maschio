import json
from MySQLConnector import MySQLConnector
import ExcelXlsHandler as xh


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
                self.excelData = xh.readFile(self.dataPath)

            elif (step["action"] == "translateColumns"):
                self.excelData = self.translateColumns()

            elif (step["action"] == "transpose"):
                self.excelData = xh.transpose(self.excelData)

            elif (step["action"] == "drop"):
                self.excelData = xh.dropRowByIndex(self.excelData, int(step["rownum"]))

            elif (step["action"] == "header"):
                self.excelData = xh.setFirstRowAsHeader(self.excelData)

            elif (step["action"] == "delColByName"):
                self.excelData = xh.dropColumnsByName(self.excelData, step["columns"])

            elif (step["action"] == "renameColumn"):
                self.excelData = xh.renameHeaderByIndex(self.excelData, step["columnNumber"], step["newName"])
            else:
                print("oops")

            test += 1

            xh.writeLocal(self.excelData, self.profileName + str(test) + str(step["action"]) + ".xlsx", "Test/",header=True)

        if self.profile["options"]["TranslateColumnsBeforeLoading"] == True:
            self.translateColumns()

        if self.profile["options"]["AddProfileColumn"] == True:
            xh.addStaticColumn(self.excelData,"Laboratorio",self.profileName)

        self.dab.insertTable(self.excelData, "analisi")

    def translateColumns(self):
        query="select campo_lab,campo_interno from dizionario where lab='"+self.profileName+"'"
        results=self.dab.select(query)
        columnNames= {str(row[0]): str(row[1]) for row in results}
        return xh.renameHeader(self.excelData, columnNames)

"""
        for key in dict:
            print(key)
            print(key in self.excelData)

            print(dict[key])
            print(dict[key] in newExcel)
            print("---")

        return newExcel
"""
