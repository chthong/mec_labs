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

from os import environ as env
import requests as reqs
from oai_mep.models.service import Service
from oai_mep.utils.util import *

class KongConnector(object):
    """
        The connector can be initialized from envirnmental variables or directly by passing 
        host and port to the constructor.
        If none of them are provided an exception is raised.
    """
    def __init__(self, configuration, from_env: bool=False, host: str=None, port: str=None):
        self.configuration = configuration
        self.url = configuration['application']['kong']
        self._fqdn = configuration['application']['fqdn']

    def add_service(self, service: Service):
        """
            To add a service 2 requests are needed:
                1- push a new service to kong with its upstream
                2- create a route towards the service
            Overall, 2 HTTP requests are needed, 3 in case a test is required
        """
        
        body = {
            "name": service.name,
            "host": service.host,
            "port": service.port
        }
        r = reqs.post(url=f"http://{self.url}/services", json=body)
        if r.status_code == 201:
            hostmasq = self._fqdn
            r_dict = r.json()
            service_id = r_dict["id"]
            r_body = {
                "protocols" : ["http"],
                #TODO: explore all endpoints and add info about possible methods
                "hosts": [hostmasq],
                "paths": [f"/{service.name}"],
            }
            rr = reqs.post(url=f"http://{self.url}/services/{service_id}/routes", json=r_body)
            if rr.status_code == 201:
                return service_id
            else:
                raise Exception("Cannot push the route for the following service")
        else: 
            raise Exception("Cannot push the following service to the MP1 Gateway")

    def remove_service(self, service):
        if service is None:
            raise Exception("Null Service Exception")
        r = reqs.get(url=f"http://{self.url}/services")
        if r.status_code != 200:
            raise Exception("Cannot retrieve services list from the MP1 Gateway")
        
        #look for the service id which is needed to remove it
        #REMIND: name is unique within the services collection
        sid = None
        for serv in r.json()['data']:
            print(service.name)
            if serv['name'] == service.name:
                sid = serv['id']
                print(serv['id'])
        
        if sid is None:
            raise Exception("The required service has not been found inside the MP1 Database")
        
        #remove the route for the service before removing it
        #STEP1 retrieve the route id

        r = reqs.get(url=f"http://{self.url}/services/{sid}/routes")        
        if r.status_code != 200:
            raise Exception("Cannot retrieve routes list from the MP1 Gateway")
        routes = r.json()['data']
        for route in routes:
            r = reqs.delete(url=f"http://{self.url}/services/{sid}/routes/{route['id']}")
            if r.status_code != 204:
                raise Exception(f"Cannot delete route{route['id']}from the MP1 Gateway")
        
        #STEP2 remove the service
        r = reqs.delete(url=f"http://{self.url}/services/{sid}")
        if r.status_code != 204:
                raise Exception(f"Cannot delete service{sid}from the MP1 Gateway")
        return