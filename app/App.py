from Orchestrator import Orchestrator
import EmailHandler as eh
import json
import os
import sys
import time

from ProfileSelector import ProfileSelector
"""
if len(sys.argv) > 2:
    print('You have specified too many arguments')
    sys.exit()

if len(sys.argv) < 2:
    print('You need to specify the path to be listed')
    sys.exit()

filePath = sys.argv[1]
"""

with open('conf.json', encoding='utf-8') as f:
    conf = json.load(f)

selector = ProfileSelector()
a=True
while a==True:
    response= eh.getAttachments(conf["Email"][conf["DataEmail"]])
    if len(response)!=0:
        for data in response:
            #print(response)
            prof = selector.auto(data[0])
            if(prof!=-1):
                orchestrator = Orchestrator(data[0], prof)
                status=orchestrator.run()
                del orchestrator
                """
                if(status[0]!=-1):
                    eh.markAsRead(conf["Email"][conf["DataEmail"]],data[1])

                eh.send(conf["Email"][conf["DataEmail"]],conf["Email"][conf["AlertEmail"]],status[1])
                """
                for r in status:
                    print(r)

            else:
                print("errore: profilo non trovato per il file "+data[0])
    #time.sleep(600)
    a=False