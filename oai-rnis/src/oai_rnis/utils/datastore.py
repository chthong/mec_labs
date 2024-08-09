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

import threading
import logging

class DataStore():
    def __init__(self, notification_service):
        self.__users = {}
        self.__pdusessions = {}
        self.__cells = {}
        self.__lock = threading.Lock()
        self.__notification_service = notification_service
        self.__logger = logging.getLogger("DataConvergenceApp")


    def pushPduSession(self, pdusession):
        with self.__lock:
            if pdusession.supi not in self.__pdusessions:
                self.__pdusessions[pdusession.supi] = {}
                self.__logger.info("a new pdu session has been pushed")
                # is this a new PDU Session?
            if pdusession.id not in self.__pdusessions[pdusession.supi]:
                # TODO notification procedure for RabEstNotification
                self.__notification_service.new_event(event = "RabEstSubscription", data = pdusession)
            else:
                self.__notification_service.new_event(event = "RabModSubscription", data = pdusession)
            self.__pdusessions[pdusession.supi][pdusession.id] = pdusession
        return

    def pushUEStatus(self, isRegistered, supi, ngap_id, gnbid, timestamp):
        with self.__lock:
            if "imsi-" in supi:
                supi = supi.replace("imsi-", "")
            #save a ue state. It is done a priori and it is kept also when ue deregister... unless until the core network will expose also obsolete stats.
            #in this way we can avoid to push old stats by knowing the latest one we pushed
            self.__users[supi] = {"ngap_id": ngap_id, "gnb_id":gnbid, "is_registered": isRegistered, "timestamp": int(timestamp) }
            if isRegistered:
                #if a user register, we want to track its cell and the ue itself
                if gnbid not in self.__cells:
                        self.__notification_service.new_event("NewCellSubscription", gnbid)
                        self.__cells[gnbid] = {}
                #add user to the cell
                if ngap_id not in self.__cells[gnbid]:
                    self.__cells[gnbid][ngap_id] = {"supi": supi, "kpi":{}}
                    self.__logger.debug("user " + str(supi)+ "connected to cell "+ str(gnbid))
                    self.__logger.debug(self.__cells)
            else:
                #if user unregister we remove it from the cell
                #remove user from the cell
                for session in self.get_ue_sessions(supi):
                    self.__notification_service.new_event(event = "RabRelSubscription", data = session)
                if gnbid in self.__cells and ngap_id  in self.__cells[gnbid]:
                    self.__cells[gnbid].pop(ngap_id)
                if supi in self.__pdusessions:
                    self.__pdusessions.pop(supi)
                self.__logger.debug("user" + str(supi) + "disconnected from cell "+ str(gnbid))
                self.__logger.debug(self.__cells)


    def pushKPI(self, cell, kpi):
        if cell in self.__cells and int(kpi["labels"]["amf_ue_ngap_id"]) in self.__cells[cell]:
            user = self.ngap2supi(int(kpi["labels"]["amf_ue_ngap_id"]),cell)
            #the KPI refers to an user tracked by RNIS so we store the KPI
            self.__cells[cell][int(kpi["labels"]["amf_ue_ngap_id"])]["kpi"][kpi["kpi"]] = kpi
            self.__logger.debug("A new KPI message for "+str(kpi["labels"]["amf_ue_ngap_id"]) +" at cell "+ str(cell)+ " has been pushed")
            #notify the event
            self.__notification_service.new_event(event = "NrMeasRepUeSubscription", data = [cell, self.supi2ips(user), self.ue_kpis(user)])
        else:
                #the KPI refers to an user of which we have no information, so we drop it
                self.__logger.debug("A new KPI message for "+str(kpi["labels"]["amf_ue_ngap_id"]) +" at cell "+ str(cell)+ " has been dropped because it belongs to an untracked user)")

        return

    def is_supi_registered(self, supi):
        return supi in self.__users and self.__users[supi]["is_registered"]
        
    @property
    def plmns(self):
        plmns = []
        unique = True
        for supi in self.__pdusessions:
            pdu_sessions = self.__pdusessions[supi]
            for id, pdu_session in pdu_sessions.items():
                plmn_frompdu = pdu_session.plmn
                for plmn in plmns:
                    if plmn == plmn_frompdu:
                        unique = False
                if unique:
                    plmns.append(plmn_frompdu)
        return plmns

    @property
    def users(self):
        users_dict = {}
        for supi in self.__pdusessions:
            users_dict[supi] = []
            for id,pdu_session in self.__pdusessions[supi].items():
                users_dict[supi].append({pdu_session.type: pdu_session.ue_ip})
        return users_dict

    @property
    def pdu_sessions(self):
        sessions = self.__pdusessions
        return sessions


    @property
    def cell_users(self):
        cells = self.__cells
        return cells

    def find_registration_log(self, supi):
        if "imsi-" in supi:
            supi = supi.replace("imsi-","")
        if supi in self.__users:
            return self.__users[supi]
        return None

    def ngap2supi(self, ngap_id, cell):
        if cell in self.__cells and ngap_id in self.__cells[cell]:
            return self.__cells[cell][ngap_id]["supi"]

    def supi2ngap(self, supi):
        if supi in self.__users and self.__users[supi]["is_registered"]:
            return  self.__users[supi]["ngap_id"]

    def ue_kpis(self, supi):
        if supi in self.__users: 
            gnb_id = self.__users[supi]["gnb_id"]
            ngap_id = self.__users[supi]["ngap_id"]
            kpis = self.__cells[int(gnb_id)][int(ngap_id)]["kpi"]
            return kpis
        else:
            return []

    def supi2ips(self, supi):
        ips = []
        if supi in self.__pdusessions:
            for pdu_id in self.__pdusessions[supi]:
                if self.__pdusessions[supi][pdu_id].ue_ip is not None or "":
                    ips.append(self.__pdusessions[supi][pdu_id].ue_ip)
        return ips


    def get_ue_sessions(self, supi):
        if supi in self.__pdusessions:
            return  self.__pdusessions[supi]

    def infodump(self):
        return "\n\t\tservice type: rnisApp \n\
                service name: Data Convergence Repository \n\
                active: True \n\
                workers: 0 \n\
                storage: local\n"
