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


import requests as req
import threading
import time
import logging
import json

from oai_rnis.models.plmnCN import Plmn
from oai_rnis.models.qos_flowCN import QosFlow
from oai_rnis.models.snssaiCN import Snssai
from oai_rnis.models.pdu_sessionCN import PDUSession

class CN:
    def __init__(self, cn_ip, cn_port, stats_endpoint, amf_subscription_endpoint, smf_subscription_endpoint, storage) -> None:
        self.__ip = cn_ip
        self.__port = cn_port
        self.__storage = storage
        self.__lock = threading.Lock()
        self.__stats_endpoint = stats_endpoint
        self.__stats = []
        self.__amf_subscription_endpoint = amf_subscription_endpoint
        self.__smf_subscription_endpoint = smf_subscription_endpoint

        self.__latestupdate = 0
        self.__pdu_sessions = {}
        self.__ts = time.localtime()
        self.__logger = logging.getLogger(f"[CM Handler]{self.__ip}:{self.__port}")


    #if storage is not set then retrieved values won't be persistent
    @property
    def storage(self):
        return self.__storage

    @storage.setter
    def storage(self, db_instance):
        self.__storage = db_instance

    @property
    def stats(self):
        return self.__stats

    @property
    def pdu_sessions(self):
        return self.__pdu_sessions


    def healthcheck(self):
        r = req.get(f"http://{self.__ip}:{self.__port}{self.__stats_endpoint}",timeout=5)
        if r.status_code == 200:
            self.__logger.info("[CM Handler] healthcheck passed!")
        else:
            self.__logger.error(f"[CM Handler] Not able to reach the core network manager reason {r.text}")
            raise Exception("[CM Handler] No hearthbeat from the mp2 interface")


    def __thread_poller(self,timer):
        while True:
            try:
                r = req.get(f"http://{self.__ip}:{self.__port}{self.__stats_endpoint}")
                if r.status_code == 200:
                    r_dict = json.loads(r.text)
                    for event in r_dict["AMF"]["notifications"]:
                        for report in event["reportList"]:
                            if report["type"] == "REGISTRATION_STATE_REPORT":
                                if self.__storage.find_registration_log(report["supi"]) is None or self.__storage.find_registration_log(report["supi"])["timestamp"] < int(report["timeStamp"]):
                                    #find the rmState
                                    for rmInfo in report["rmInfoList"]:
                                        if rmInfo["rmState"] == "REGISTERED":
                                                self.__logger.info("[CM Handler] A new UE-AMF context has been created")
                                                self.__logger.info("[CM Handler] UE has registered")
                                                #TODO decide if user is active or not. Now considereing like amf event is always for registration

                                        elif rmInfo["rmState"] == "DEREGISTERED":
                                                self.__logger.info("[CM Handler] A UE-AMF context has been released")
                                                self.__logger.info("[CM Handler] UE has deregistered")
                                                #TODO decide if user is active or not. Now considereing like amf event is always for registration
                                                gnbid = 0
                                                if 'gnbid' in report.keys():
                                                    gnbid = report['gnbid']
                                                self.__storage.pushUEStatus(False,report["supi"],report["amfUeNgapId"],gnbid,report["timeStamp"])

                                        else:
                                            self.__logger.info("[CM Handler] Unknown user session status")
                                            #TODO decide if user is active or not. Now considereing like amf event is always for registration
                                            break
                                        gnbid = 0 # hardcoded
                                        self.__storage.pushUEStatus(rmInfo["rmState"] == "REGISTERED",report["supi"],report["amfUeNgapId"],gnbid,report["timeStamp"])
                    
                    for event in r_dict["SMF"]["notifications"]:
                        local_ts = 0
                        for notif in event["eventNotifs"]:
                            if self.__storage.is_supi_registered(notif["supi"]) and (notif["supi"] not in self.__storage.pdu_sessions or notif["pduSeId"] not in self.__storage.pdu_sessions[notif["supi"]]  or self.__storage.pdu_sessions[notif["supi"]][notif["pduSeId"]].timestamp < int(notif["timeStamp"])):
                                if notif["event"] == "PDU_SES_EST":
                                    snssai = Snssai(sd = notif["snssai"]["sd"], sst=notif["snssai"]["sst"])
                                    plmn = Plmn(mcc=notif["supi"][0:3] , mnc=notif["supi"][3:5])
                                    pdu_session = PDUSession(
                                        id = notif["pduSeId"],
                                        supi = notif["supi"],
                                        plmn = plmn,
                                        type= notif["pduSessType"],
                                        ue_ip= notif["adIpv4Addr"],

                                        timestamp = int(notif["timeStamp"])
                                    )
                                elif "customized_data" in notif:
                                    #new data incoming
                                    #then parse the pdu session and push it to the list
                                    data = notif["customized_data"]
                                    plmn = Plmn(mcc=data["plmn"]["mcc"], mnc=data["plmn"]["mnc"])
                                    qos_flows = []
                                    for qos_flow in data["qos_flow"]:
                                        qos = QosFlow(an_addr=qos_flow["an_addr"][data["pdu_session_type"].lower()], qfi=qos_flow["qfi"], upf_addr=qos_flow["upf_addr"][data["pdu_session_type"].lower()])
                                        qos_flows.append(qos)
                                    snssai = Snssai(sd = data["snssai"]["sd"], sst=data["snssai"]["sst"])
                                    pdu_session = PDUSession(
                                        id = notif["pduSeId"],
                                        type= data["pdu_session_type"],
                                        plmn= plmn,
                                        qos_flows=qos_flows,
                                        snssai=snssai,
                                        supi= notif["supi"],
                                        ue_ip= data["ue_ipv4_addr"],
                                        timestamp = int(notif["timeStamp"])
                                    )
                                    #is a new UE?
                                else:
                                    break
                                if notif["supi"] not in self.__storage.pdu_sessions:
                                    self.__logger.info("[CM Handler] A new UE-SMF context has been created")
                                    #is this a new PDU Session?
                                if notif["pduSeId"] not in self.__storage.pdu_sessions:
                                    self.__logger.info(f"[CM Handler] A new pdu session has been created for {notif['supi']}")
                                else:
                                    self.__logger.info(f"[CM Handler] A pdu session has been updated for {notif['supi']}")
                                self.__logger.debug(f"[CM Handler] pushing data to storage {notif['supi']}")
                                self.__storage.pushPduSession(pdu_session)
                                #update stats variable or db

                self.__logger.debug("[CM Handler] Quering mp2 for updates")
            except Exception as e:
                self.__logger.error(f"[CM Handler] mp2 not available reason {e}")
            time.sleep(timer)

    def subscribe_to_amf_events(self, events):
        for event in events:
            body = {
                "event": event
            }
            r = req.post(url=f"http://{self.__ip}:{self.__port}{self.__amf_subscription_endpoint}",json=body)
            self.__logger.debug("[CM Handler] Subscription to amf events")
        return True

    def subscribe_to_smf_events(self, events):
        for event in events:
            body = {
                "event": event
            }
            r = req.post(url=f"http://{self.__ip}:{self.__port}{self.__smf_subscription_endpoint}",json=body)
            self.__logger.debug("[CM Handler] Subscription to smf events")
        return True


    def infodump(self):
        return f"\n\t\tservice type: rnisApp \n\
                service name: CN \n\
                cn IP:{self.__ip}\n\
                cn port:{self.__port}\n\
                active: True \n\
                workers: 1 \n\
                storage: default\n"

    def run(self, timer):
        self.__poller = threading.Thread(target=lambda: self.__thread_poller(timer))
        self.__poller.start()
