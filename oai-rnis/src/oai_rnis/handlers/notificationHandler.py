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

import time
import requests
from oai_rnis.controllers.rnis import subscriptions_delete, subscriptions_put
from oai_rnis.models.associate_id import AssociateId
from oai_rnis.models.ecgi import Ecgi
from oai_rnis.models.rab_mod_notification import RabModNotification
from oai_rnis.models.rab_mod_notification_erab_qos_parameters import RabModNotificationErabQosParameters
from oai_rnis.models.rab_mod_notification_erab_qos_parameters_qos_information import RabModNotificationErabQosParametersQosInformation
from oai_rnis.models.rab_est_notification import RabEstNotification
from oai_rnis.models.rab_est_notification_erab_qos_parameters import RabEstNotificationErabQosParameters
from oai_rnis.models.rab_est_notification_erab_qos_parameters_qos_information import RabEstNotificationErabQosParametersQosInformation
from oai_rnis.models.rab_est_notification_temp_ue_id import RabEstNotificationTempUeId
from oai_rnis.models.time_stamp import TimeStamp

def handle_rabEstNotification(data, subscriptions):
    #default sends a post to each callback_ui
    for sub in subscriptions:
        uri = sub["subscription"]["callbackReference"]
        ass_id = AssociateId(
            type = 1 if data.type == "IPV4" else 2,
            value = data.ue_ip
        )
        ecgi = Ecgi(
            cell_id= None,
            plmn=data.plmn
        )
        for qos_flow in data.qos_flows:
            qosParam = RabEstNotificationErabQosParameters(
                qci = qos_flow.qfi,
                qos_information=RabEstNotificationErabQosParametersQosInformation(
                    erab_gbr_dl = None,
                    erab_gbr_ul= None,
                    erab_mbr_dl = None,
                    erab_mbr_ul = None
                )
            )
        data= RabEstNotification(associate_id=ass_id, ecgi=ecgi, erab_id=data.id, erab_qos_parameters=qosParam,temp_ue_id=RabEstNotificationTempUeId(None, None), time_stamp=TimeStamp())
        try:
            requests.post(url =uri, data= data)
        except requests.exceptions.RequestException:  # This is the correct syntax
            print("Notification cannot be delivered to subscriber")
    return

def handle_rabModNotification(data, subscriptions):
    #default sends a post to each callback_ui
    for sub in subscriptions:
        uri = sub["subscription"]["callbackReference"]
        ass_id = AssociateId(
            type = 1 if data.type == "IPV4" else 2,
            value = data.ue_ip
        )
        ecgi = Ecgi(
            cell_id= None,
            plmn=data.plmn
        )
        for qos_flow in data.qos_flows:
            qosParam = RabEstNotificationErabQosParameters(
                qci = qos_flow.qfi,
                qos_information=RabEstNotificationErabQosParametersQosInformation(
                    erab_gbr_dl = None,
                    erab_gbr_ul= None,
                    erab_mbr_dl = None,
                    erab_mbr_ul = None
                )
            )
        data = RabModNotification(associate_id=ass_id, ecgi=ecgi, erab_id=data.id, erab_qos_parameters=qosParam, time_stamp=TimeStamp())
        try:
            requests.post(url =uri, data= data)
        except requests.exceptions.RequestException:  # This is the correct syntax
            print("Notification cannot be delivered to subscriber")
    return


#TODO implement standard notification
def handle_nrMeasRepUeNotification(data, subscriptions):
    #retrieve data from parameter
    cell_id = data[0]
    ips = data[1]
    kpis = data[2]
    associate_ids = []
    for ip in ips:
        associate_ids.append(ip)

    body = {
        "AssociateId": associate_ids,
        "CellId": cell_id,
        "Report": kpis,
        "TimeStamp": time.time()
    }
    for sub in subscriptions:
        uri = sub["subscription"]["callbackReference"]
        try:
            requests.post(url =uri, json= body)
        except requests.exceptions.RequestException:  # This is the correct syntax
            print("Notification cannot be delivered to subscriber")



def handle_NewCellSubscription(cell_id, subscribers):
    for subscriber in subscribers:
        subscriber.pushCell(cell_id)
    return