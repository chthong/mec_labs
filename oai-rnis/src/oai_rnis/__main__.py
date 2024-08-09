# Copyright © 2023 the OAI-RNIS Authors

# Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# Contact: netsoft@eurecom.fr

import os
import connexion
import logging


from oai_rnis.utils.datastore import DataStore
from oai_rnis.handlers.xApp import xApp
from oai_rnis.handlers.coreNetwork import CN
from oai_rnis.controllers.notificationService import NotificationService
from oai_rnis.utils import encoder
from oai_rnis.utils.util import configuration, log, registerRnis



def main():
    #load service configuration from json

    #instantiate a notification service object that will manage subscriptions and notifications
    notification_service = NotificationService()
    log.info(f"[Main] A new rnis app has been registered!\n{notification_service.infodump()}")

    #register an handler for a specific event
    #an handler receives the data structure submitted by the entity which pushed the new event
    #and a list of callbacks_uri referring subcriptions to that event
    #notification_service.register_handler(event="PDU_Enstablishment", handler=None)

    #instantiate a data repository service.
    #receives data from Core Network and RAN xApps and makes them available from NBI or notification services
    data_repository = DataStore(notification_service=notification_service)
    log.info(f"[Main] A new rnis app has been registered!\n{data_repository.infodump()}")

    ### Initialization (RNIS xApp and Core Network Notification Service)
    nxapps = []
    for node in configuration["rabbitMQ"]["nodes"]:
        xapp = xApp(broker_ip= node["brokerIp"],
                    broker_port=int(node["brokerPort"]),
                    user_name= node["userName"],
                    password= node["userPassword"],
                    storage=data_repository,
                    queue_name=node["queueName"])
        notification_service.add_internalsubscriber("NewCellSubscription", xapp)
        nxapps.append(xApp)

    cn_list = []
    #instantiate different Core Network object for each connected controller
    for node in configuration["coreNetwork"]["nodes"]:
        cn = CN(cn_ip=node["cnIp"],
                cn_port=int(node["cnPort"]),
                stats_endpoint=node["statsEndpoint"],
                amf_subscription_endpoint=node["amfSubscriptionEndpoint"],
                smf_subscription_endpoint=node["smfSubscriptionEndpoint"],
                storage=data_repository)
        try:
            cn.healthcheck()
            cn.subscribe_to_amf_events(['REGISTRATION_STATE_REPORT'])
            cn.subscribe_to_smf_events(['PDU_SES_EST'])
            cn_list.append(cn)
            if "pollingTimer" in node:
                cn.run(int(node["pollingTimer"]))
            else:
                cn.start_polling(int(configuration["coreNetwork"]["pollingTimer"]))
            log.info(f"[Main] A new rnis app has been registered!\n{cn.infodump()}")
        except Exception as e:
            log.error(e)

    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Radio Network Information Northbound API - 5G SA Interface Proposal'}, pythonic_params=True)
    app.app.config["data_repository"] = data_repository
    app.app.config["notification_service"]  = notification_service
    app.run(host=configuration['application']['host'],port=configuration['application']['port'], threaded=False)

if __name__ == '__main__':
    main()