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


from oai_rnis.models.link_type import LinkType
from oai_rnis.handlers.notificationHandler import handle_rabModNotification, handle_rabEstNotification, handle_NewCellSubscription, handle_nrMeasRepUeNotification
from oai_rnis.models.ca_reconf_subscription_links import CaReconfSubscriptionLinks
from oai_rnis.utils.util import configuration, RNIS_URL
import threading
import logging
import queue

class NotificationService():
    def __init__(self) -> None:
        self.__handlers = {}
        #set default handlers
        self.__handlers["RabEstSubscription"] = handle_rabModNotification
        self.__handlers["RabModSubscription"] = handle_rabEstNotification
        self.__handlers["NewCellSubscription"] = handle_NewCellSubscription
        self.__handlers["NrMeasRepUeSubscription"] = handle_nrMeasRepUeNotification
        self.__lock = threading.Lock()
        self.__subscriptions = {}
        self.__eventQueue = queue.Queue(maxsize=5000)
        self.__subscriptions["CellChangeSubscription"] = {"latest": 0, "subscriptions":[]}
        self.__subscriptions["RabEstSubscription"] = {"latest": 0, "subscriptions":[]}
        self.__subscriptions["RabModSubscription"] = {"latest": 0, "subscriptions":[]}
        self.__subscriptions["RabRelSubscription"] = {"latest": 0, "subscriptions":[]}
        self.__subscriptions["MeasRepUeSubscription"] = {"latest": 0, "subscriptions":[]}
        self.__subscriptions["NrMeasRepUeSubscription"] = {"latest": 0, "subscriptions":[]}
        self.__subscriptions["MeasTaSubscription"] = {"latest": 0, "subscriptions":[]}
        self.__subscriptions["CaReconfSubscription"] = {"latest": 0, "subscriptions":[]}
        self.__subscriptions["NGBearerSubscription"] = {"latest": 0, "subscriptions":[]}
        self.__subscriptions["NewCellSubscription"] = {"latest": 0, "subscriptions":[]}
        self.__logger = logging.getLogger("NotificationService")
        #set up worker thread
        threading.Thread(target=lambda: self.__notify()).start()

    def get_subscriptions(self):
        with self.__lock:
            return self.__subscriptions

    def add_internalsubscriber(self, event_type, subscriber):
        with self.__lock:
            if event_type not in  self.__subscriptions:
                return
            else:
                self.__subscriptions[event_type]["latest"] = self.__subscriptions[event_type]["latest"] + 1
                self.__subscriptions[event_type]["subscriptions"].append(subscriber)
                self.__logger.info(f"[Notification Service] new subscriber for {event_type}")

    def add_subscription(self, subscription):
        with self.__lock:
            _type = subscription["subscriptionType"]
            if _type not in self.__subscriptions:
                raise Exception("Event not supported by Notification Service")
            #generate subscription reference
            subid =  _type.lower() + "_" +  str(self.__subscriptions[_type]["latest"])
            if RNIS_URL is not None:
                rnis_host = RNIS_URL
            else:
                rnis_host = f"http://{configuration['application']['host']}{configuration['application']['port']}/{configuration['application']['versionEndpoint']}"
            link = f"{rnis_host}/subscriptions/{subid}"
            subscription["_links"] = CaReconfSubscriptionLinks(
                LinkType(
                    href=link
                )
            )
            #store the subscription
            self.__subscriptions[_type]["latest"] = self.__subscriptions[_type]["latest"] + 1
            self.__subscriptions[_type]["subscriptions"].append({"id":  subid, "subscription": subscription})
            self.__logger.info(f"Notification Service] new subscriber for{_type}")

            return subscription

    def mod_subscription(self, ref_url, new_subscription):
        return

    def del_subscription(self, ref_url):
        for _type in self.__subscriptions:
            for sub in self.__subscriptions[_type]["subscriptions"]:
                if sub["id"] == ref_url:
                    self.__subscriptions[_type]["subscriptions"].remove(sub)
                    return True
        return False

    def __send_notification(self, ref_url, data):
        return

    def register_handler(self, event, handler):
        with self.__lock:
            self.__handlers[event] = handler

    def new_event(self, event, data):
        #push a new event to the queue
        try:
            self.__eventQueue.put([event, data], block=False)
        except queue.Full:
            self.__logger.warning(f"[Event Management] Event queue is full, discarding event")

    def __notify(self):
        while True:
            tp = self.__eventQueue.get()
            event = tp[0]
            data = tp[1]
            self.__logger.debug(f"[Event Management] new event seen {event}")
            if event in self.__handlers:
                if self.__handlers[event] is None:
                    self.__logger.error(f"[Event Management] no handler defined for {event}")
                    return
                self.__logger.debug(f"[Event Management] handling {event}")
                self.__handlers[event](data, self.__subscriptions[event]["subscriptions"])
            else:
                self.__logger.error(f"[Event Management] {event} is an unknown event type")
            self.__eventQueue.task_done()

    def infodump(self):
        return "\n\t\tservice type: rnisApp \n\
                service name: Notification Service \n\
                active: True \n\
                workers: 1 \n\
                storage: default\n"