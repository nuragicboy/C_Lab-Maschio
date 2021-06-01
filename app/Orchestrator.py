import JsonHandler as jh
import ExcelXlsHandler as xh
class Orchestrator:
    def __init__(self, dataPath, profilePath):
        self.dataPath=dataPath
        self.profile=profilePath
        self.profile = open(profilePath, "r", encoding="utf-8")


    def run(self):
        test=0
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
                colname=self.profile.readline().rstrip().split(",")
                self.excelData = xh.dropColumnsByName(self.excelData, colname)

            elif (line == "replacecolumnname"):
                index = self.profile.readline().rstrip().split(",")
                value = self.profile.readline().rstrip().split(",")
                self.excelData = xh.renameHeaderByIndex(self.excelData, index, value)
            else:
                print("oops")

            test+=1

            xh.writeLocal(self.excelData, "michelet"+str(test)+str(line)+".xlsx", "Test/")



