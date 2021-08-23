import ExcelXlsHandler as xh
import re
import json

class ProfileSelector:
    def __init__(self):
        with open('conf.json', encoding='utf-8') as f:
            self.conf = json.load(f)

        with open(self.conf["Auto"], encoding='utf-8') as f:
            self.profile = json.load(f)

    def auto(self,file):
        data = xh.readFile(file, header=None)
        for profile in self.profile["auto"]:
            for check in profile["check"]:

                if (check["action"] == "checkMail"):
                    print("checco la mail, ma ancora non esiste")

                elif (check["action"] == "regex"):
                    print(data.iloc[int(check["cell"][0]),int(check["cell"][1])])
                    p = re.compile(check["expression"])
                    if p.match(str(data.iloc[int(check["cell"][0]),int(check["cell"][1])])):
                        print (profile["ProfileName"])
                        return profile["ProfileName"]
        return -1


