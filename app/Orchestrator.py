import JsonHandler as jh
import ExcelXlsHandler as xh
class Orchestrator:
    def __init__(self, dataPath, profilePath):
        self.dataPath=dataPath
        self.profile=profilePath
        self.profile = open(profilePath, "r")


    def run(self):
        for line in self.profile:
            line = line.rstrip()

            if(line == "readexcel"):
                self.excelData = xh.readFile(self.dataPath)

            elif(line == "transpose"):
                self.excelData = xh.transpose(self.excelData)

            elif (line == "drop"):
                line = self.profile.readline().rstrip().split()
                self.excelData = xh.dropRowByIndex(self.excelData, int(line[0]))

            elif (line == "header"):
                self.excelData=xh.setFirstRowAsHeader(self.excelData)


            elif (line == "delcolbyname"):
                print("delcolbyname")
                print(self.profile.readline())

            elif (line == "replacecolumnname"):
                print("replacecolumnname")
                print(self.profile.readline())
                print(self.profile.readline())

            else:
                print("oops")




