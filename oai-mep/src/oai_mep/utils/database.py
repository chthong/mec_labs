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



from bson import ObjectId
import pymongo

class MEPDB(object):
    """MEP database pointer.
    """
    def __init__(self, configuration):
        self.configuration = configuration
        self.db_client = pymongo.MongoClient(configuration['database']['host'], int(configuration['database']['port']),username=configuration['database']['user'],password=configuration['database']['password'])
        if configuration['database']['reset'] == 'yes':
            self.db_client.drop_database(configuration["database"]['name'])
            print("Reseted the Database")
        self.db = self.db_client[configuration['database']['name']]
        # create collections and indexes
        self.db_collection_services = self.db["services"]
        self.db_collection_services.create_index("uid", unique=True)


    def get_service_byId(self,service_id):
        hostmasq = self.configuration['application']['fqdn']
        gateway_port = self.configuration['application']['port']
        service = self.db_collection_services.find_one({"_id": ObjectId(service_id)})
        service['sid'] = str(service["_id"])
        service.pop("_id")
        #convert the app upstream url to the rev-proxied url on the mp1 interface
        service['host'] = hostmasq
        service['port'] = gateway_port
        service['path'] = "/" + service['name'] + service['path']
        return service

    def get_services_db(self,type:  str):
        filter = None if type == None else {"type": type}
        services = self.db_collection_services.find()
        hostmasq = self.configuration['application']['fqdn']
        gateway_port = self.configuration['application']['port']
        sv =[]
        for service in services:
            service['sid'] = str(service["_id"])
            service.pop("_id")
            #convert the app upstream url to the rev-proxied url on the mp1 interface
            service['host'] = hostmasq
            service['port'] = gateway_port
            service['path'] = "/" + service['name'] + service['path']
            sv.append(service)
        return sv

    def del_service(self,service_id: str):
        if service_id == False:
            return False
        else:
            res = self.db_collection_services.delete_one({"_id":ObjectId(service_id)})
            if res.deleted_count > 0:
                return True
            else:
                return False

    def new_service(self,service):
        if len(list(self.db_collection_services.find({ "$or": [ { "name": service["name"] }, { "$and" : [{"host": service["host"]},{ "port": service["port"]},{ "path": service["path"]}]}]}))) > 0:
            return None
        return str(self.db_collection_services.insert_one(service).inserted_id)