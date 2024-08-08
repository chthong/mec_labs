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

import connexion
import requests
from oai_mep.utils import encoder
from oai_mep.utils.util import configuration, log
import uuid
import time
import sys

def initialize_mep(configuration):
    """
    add the registry service in the kong database and create a route fo registry service to be exposed via kong 
    else this has to be done manually
    """
    service = {
        "name": "service_registry",  # for development you can change to str(uuid.uuid4()),
        "host": configuration['application']['host'],
        "port": int(configuration['application']['port'])
        }

    i = 0
    for i in range(0,40):
        r = None
        try:
            r = requests.post(url=f"http://{configuration['application']['kong']}/services", json=service)
        except Exception as e:
            log.info('Waiting for oai-mep-gateway to start')

        if r is not None and r.status_code == 201:
            hostmasq = configuration['application']['fqdn']
            service_id = r.json()["id"]
            route = {
                "protocols" : ["http"],
                "hosts": [hostmasq],
                "paths": [f"/{service['name']}"],
            }
            r = requests.post(url=f"http://{configuration['application']['kong']}/services/{service_id}/routes", json=route)
            if r.status_code == 201:
                log.debug("MEP registry service is added in the kong database")
                log.info(f"Registry service swagger defination --> http://{hostmasq}/{service['name']}/v1/ui")
                break
            else:
                raise Exception(f"Cannot push the route for the following MEP registry service reason {r.text} status_code {r.status_code}")
                sys.exit(1)
        else: 
            if r is not None:
                raise Exception(f"Cannot push the MEP registry service in kong database reason {r.text} status_code {r.status_code}")
                sys.exit(1)
            else:
                log.info(f"Waiting for oai-mep-gateway to start")
        i +=1
        time.sleep(1)

def main():
    initialize_mep(configuration)
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'OAI Multi-access Edge Computing Platform '}, pythonic_params=True)
    app.run(port=configuration['application']['port'],threaded=True)

if __name__ == '__main__':
    main()
