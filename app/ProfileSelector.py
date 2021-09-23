import os

import PandasHandler as pd
import re
import json

class ProfileSelector:
    def __init__(self):
        with open('conf.json', encoding='utf-8') as f:
            self.conf = json.load(f)

        with open(self.conf["Auto"], encoding='utf-8') as f:
            self.profile = json.load(f)

    def auto(self,file):
        ext=os.path.splitext(file)[1].upper()
        datatype=None
        data=None
        if(ext in {".XLS",".XLSX"}):
            datatype="xls//xlsx"
            data = pd.readXLS(file, header=None)
        elif(ext==".CSV"):
            datatype = "csv"
            data = pd.readCSV(file, header=None, skiprows=1)
        #else:
            #print("formato non valido")

        for profile in self.profile["auto"]:
            for check in profile["check"]:

                if (check["action"] == "checkMail"):
                    pass

                elif (check["action"] == "regex"):
                    temp=data[check["cell"][1]].astype(str)
                    field=str(temp.iloc[int(check["cell"][0])])
                    p = re.compile(check["expression"])

                    print(type(field))

                    print(field)
                    print("21MA01630")

                    if p.search(str("21MA01630")):
                        print("got ")
                    if p.search(str(field)):
                        print("got ti")
                        return profile["ProfileName"]
        return -1


