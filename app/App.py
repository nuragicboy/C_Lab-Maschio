from Orchestrator import Orchestrator
from GmailMonitor import GmailMonitor
import os
import sys
import time

from app.ProfileSelector import ProfileSelector
"""
if len(sys.argv) > 2:
    print('You have specified too many arguments')
    sys.exit()

if len(sys.argv) < 2:
    print('You need to specify the path to be listed')
    sys.exit()

filePath = sys.argv[1]
"""
#monitor = GmailMonitor()
selector = ProfileSelector()
a=True
while a==True:
    #filePath= monitor.run()
    filePath=["RDP_UIV mini.csv"]
    for file in filePath:
        orchestrator = Orchestrator(file, selector.auto(file))
        orchestrator.run()
        del orchestrator

    print("ora nanna")
    #time.sleep(600)
    a=False