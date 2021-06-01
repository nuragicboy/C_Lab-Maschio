from Orchestrator import Orchestrator
import os
import sys

if len(sys.argv) > 3:
    print('You have specified too many arguments')
    sys.exit()

if len(sys.argv) < 3:
    print('You need to specify the path to be listed')
    sys.exit()

filePath = sys.argv[1]
profilePath = sys.argv[2]

orchestrator = Orchestrator(filePath,profilePath)
orchestrator.run()