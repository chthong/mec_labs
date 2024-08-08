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


from email import message
from sqlite3 import connect
import connexion
from itsdangerous import NoneAlgorithm
from oai_mep.controllers.kongConnector import KongConnector
from oai_mep.models.api_response import ApiResponse  # noqa: E501
from oai_mep.models.service import Service  # noqa: E501
from oai_mep.utils.util import *

def add_service(body):  # noqa: E501
    """Register a new service

     # noqa: E501

    :param service: Service object that needs to be added to the registry
    :type service: dict | bytes

    :rtype: None
    """
    try:
        if connexion.request.is_json:
            service = Service.from_dict(connexion.request.get_json())  # noqa: E501
            _id = mepdb.new_service(connexion.request.get_json())
            if(_id is not None):
                kc = KongConnector(configuration)
                kc.add_service(service)
                return mepdb.get_service_byId(_id), 201
            else:
                return ApiResponse(
                    code = 409,
                    type = "Error",
                    message= "The submitted service already exists"
                ), 409
    except Exception as e:
        return ApiResponse(
                        code = 500,
                        type = "Internal Server Error",
                        message= str(e)
                    ), 500

def delete_service(service_id):  # noqa: E501
    """Deregister a service

     # noqa: E501

    :param service_uri:
    :type service_uri: str

    :rtype: None
    """
    try:
        to_delete = mepdb.get_service_byId(service_id)
        to_delete =  Service.from_dict(to_delete)
        if to_delete is None:
            return ApiResponse(
                code = 404,
                type = "Not Found",
                message = "The resource has not been found"
            ), 404
        kc = KongConnector(configuration)
        kc.remove_service(to_delete)

        if mepdb.del_service(service_id = service_id):
            return ApiResponse (
                code = 200,
                type = "Succesful",
                message= "The service has been correctly deleted"
            )
        else:
            return ApiResponse (
                code = 404,
                type = "Error",
                message= "Cannot find the requested service"
            ), 404
    except Exception as e:
        return ApiResponse(
            code = 500,
            type = "Internal Server Error",
            message= str(e)
        ), 500

def get_services():  # noqa: E501
    """Lists all registered services

    Returns all the available services # noqa: E501


    :rtype: List[Service]
    """
    services = mepdb.get_services_db(type = None)
    return services


def get_services_by_type(service_type):  # noqa: E501
    """Find services belonging to the requested category

    Returns a list of services which belongs to a certain category  # noqa: E501

    :param service_type: Type of services to return
    :type service_type: str

    :rtype: List[Service]
    """
    services = mepdb.get_services_db(type = service_type)
    return services