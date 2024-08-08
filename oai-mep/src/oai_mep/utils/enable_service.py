#   Copyright 2023 OAI-MEP Authors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#   Contact: netsoft@eurecom.fr

import sys
import requests
import json
import os
import logging

# add logging to console and log file
logging.basicConfig(format='%(asctime)s (%(levelname)s) %(message)s', level=logging.DEBUG, datefmt='%d.%m.%Y %H:%M:%S')

log = logging.getLogger(__name__)

if len(sys.argv) != 3:
    log.error("Expecting 2 extra argouments, but " + str(len(sys.argv) - 1) +" provided")
    log.error("\n\nUsage: "+sys.argv[0] +" <registry url> <app-descriptor-file.json>")
    log.error("\nExample: "+sys.argv[0] +" http://mp1.mec.eurecom.fr/registry/v2/register app-descriptor.json", sys.argv[0])
    exit(2)
    
#retrieve service descriptor filename
filename = sys.argv[2]


url = sys.argv[1]
with open(filename) as app_descriptor:
    appd = json.load(app_descriptor)

    #run bootstrapping commands if present
    if "cmd" in appd:   
        log.info("Executing preparatory commands specified in the app descriptor") 
        for cmd in appd["cmd"]:
            os.system(cmd)
    
    #the docker compose will be automatically deploy the container. Be sure the one you chose is working fine
    if "docker-compose" in appd:
        log.info("Deploying from docker-compose file")
        os.system("sudo docker-compose -f "+appd["docker-compose"]+ " up -d")
        
    #push the service to the registry service
    log.info("Pushing the service to the Registry Service")
    def_header = {'Content-type': 'application/json'}
    for s in appd['services']:
        service = {
            'name': s['name'],
            'type': s['type'],
            'host': appd['dns'],
            'port': s['port'],
            'path': s['path'],
            'endpoints': s['endpoints'],
            'description':s['description']
        }
        r = requests.post(url, data = json.dumps(service), headers =def_header )
        log.debug(r.text)
        if r.status_code != 200:
            exit(1)
    log.info("Successful")
    exit(0)