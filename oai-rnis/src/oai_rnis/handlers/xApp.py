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
import pika
import json
import logging
import functools

class xApp:
    def __init__(self=None, broker_ip=None, broker_port=None ,storage=None, user_name = None, password = None, queue_name = None):
        self.__ip = broker_ip
        self.__port = broker_port
        self.__cell_ids = []
        self.__user_name = user_name
        self.__password = password
        self.__queue_name = queue_name
        self.__credentials = pika.PlainCredentials(username=self.__user_name, password=self.__password)
        self.storage = storage
        self.__Data_Repository = None
        self.__logger = logging.Logger(f"[RNIS xApp] {broker_ip}:{broker_port}")
        self.__channels = []

    #create connection and channel with the broker
    def create_channel(self, cell_id):
        channel = self.__connection.channel()
        #channel.exchange_declare()
        #queue_name = self.create_queue(channel, cell_id)
        queue_name = self.__queue_name
        self.consume(channel,queue_name,cell_id)
        self.__logger.info("[RNIS xApp] Created new channel to consume " + str(cell_id))
        self.__channels.append(channel)
        return channel

    def __newCellCallback(self, cell_id):
        try:
            self.__connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.__ip, port = self.__port, credentials=self.__credentials))
        except Exception as e:
            self.__logger.error("[RNIS xApp] Cannot connect to broker")
            return None
        if cell_id not in self.__cell_ids:
            self.__cell_ids.append(cell_id)
            self.create_channel(cell_id)

    def pushCell(self,cell_id):
        #dirty fix to avoid xapp client to stall the notification service
        threading.Thread(target=lambda: self.__newCellCallback(cell_id=cell_id)).start()
        self.__logger.info(f"[RNIS xApp] Received NewCellSubscription notification - cell:{cell_id}")

    #create queue in order to be able to read msgs
    def create_queue(self, channel, cell_id):
        queue_name = self.__queue_name
        queue = channel.queue_declare(queue_name, exclusive=True, durable=True)
        channel.queue_bind(
           queue = queue_name, )
        self.__logger.debug(f"[RNIS xApp] Created a queue {queue_name} to read the messages")
        return queue_name

    #method to effectively start to consume messages
    def consume(self, channel, queue_name, cell_id):
        custom_callback = functools.partial(callback, args=(self,cell_id))
        channel.basic_consume(queue=queue_name, on_message_callback=custom_callback, auto_ack=True)
        channel.start_consuming()

def callback(channel, method, properties, body, args):
        kpi_data = json.loads(body.decode('UTF-8'))
        args[0].storage.pushKPI(args[1], kpi_data)