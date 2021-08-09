import json
from MySQLConnector import MySQLConnector
import ExcelXlsHandler as xh


class Orchestrator:
    def __init__(self, dataPath, profilePath):
        self.dataPath = dataPath

        with open('conf.json', encoding='utf-8') as f:
            self.conf = json.load(f)

        with open(profilePath, encoding='utf-8') as f:
            self.profile = json.load(f)

    def run(self):
        test = 0
        for step in self.profile["steps"]:

            if (step["action"] == "readExcel"):
                self.excelData = xh.readFile(self.dataPath)

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

            xh.writeLocal(self.excelData, "michelet" + str(test) + str(step["action"]) + ".xlsx", "Test/")

        conn = self.conf["RemoteConnections"]["remotemysql"]
        dab = MySQLConnector(conn)
        dab.insertTable(self.excelData, "analisi")
