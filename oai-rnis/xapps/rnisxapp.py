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

import pika #external dependency
import json
import xapp_sdk as ric
import time
import configparser
import sys
import traceback
import logging
import threading

#  getting config parameters from config.ini
config_file_name = 'config.ini'
config = configparser.ConfigParser()
config.read(config_file_name)

log_level = config['XAPP']['LogLevel']

if log_level == 'debug':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
elif log_level == 'info':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
elif log_level == 'error':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.ERROR)


################### northbound part of the xApp ######################

# function to parse raw kpis to json object
def json_payload(kpi,timestamp,value,ue_id,source="RAN",unit=None):
    a = { "kpi": kpi,
         "source": source,
         "timestamp": timestamp,
         "unit": unit,
         "value": value,
         "labels": {
             "amf_ue_ngap_id": ue_id
            }
        }
    return json.dumps(a)


####################
#### MAC INDICATION CALLBACK
####################

#  MACCallback class is defined and derived from C++ class mac_cb
class MACCallback(ric.mac_cb):
    # Define Python class 'constructor'
    def __init__(self):
        # Call C++ base class constructor
        ric.mac_cb.__init__(self)
            #Establish the connection with the broker
        try :
            self.remote_rabbitmq_ip = config['XAPP']['RemoteRabbitMqAddress']
            self.remote_rabbitmq_port = config['XAPP']['RemoteRabbitMqPort']
            self.remote_rabbitmq_user = config['XAPP']['RemoteRabbitMqUsername']
            self.remote_rabbitmq_password = config['XAPP']['RemoteRabbitMqPassword']
        except Exception as e:
            traceback.print_exc()
            logging.error(f"Error while reading configuration elements from {config_file_name}")
            sys.exit(1)

        self.credentials = pika.PlainCredentials(username=self.remote_rabbitmq_user, password=self.remote_rabbitmq_password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.remote_rabbitmq_ip,port=self.remote_rabbitmq_port,credentials=self.credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='rnis_xapp',durable=True)
        # Override C++ method: virtual void handle(swig_mac_ind_msg_t a) = 0;
    def handle(self, ind):
        # Print swig_mac_ind_msg_t
        for ue in range(len(ind.ue_stats)):
            #print("calling handle")
            tmp_payload_list = []
            # creating the json object for the KPI
            tmp_payload_list.append(json_payload(kpi='cqi',timestamp=ind.tstamp,value=ind.ue_stats[ue].wb_cqi,ue_id=ind.ue_stats[ue].dl_mcs2,source="RAN"))
            # we receive -RSRP  from the RAN because MAC SM uses unsigned int and can not transport negative values
            tmp_payload_list.append(json_payload(kpi='rsrp',timestamp=ind.tstamp,value=-1*ind.ue_stats[ue].ul_mcs2,unit="dBm",ue_id=ind.ue_stats[ue].dl_mcs2,source="RAN"))
            tmp_payload_list.append(json_payload(kpi='mcs_ul',timestamp=ind.tstamp,value=ind.ue_stats[ue].ul_mcs1,ue_id=ind.ue_stats[ue].dl_mcs2,source="RAN"))
            tmp_payload_list.append(json_payload(kpi='mcs_dl',timestamp=ind.tstamp,value=ind.ue_stats[ue].dl_mcs1,ue_id=ind.ue_stats[ue].dl_mcs2,source="RAN"))
            tmp_payload_list.append(json_payload(kpi='phr',timestamp=ind.tstamp,value=ind.ue_stats[ue].phr,ue_id=ind.ue_stats[ue].dl_mcs2,source="RAN"))
            tmp_payload_list.append(json_payload(kpi='bler_ul',timestamp=ind.tstamp,value=ind.ue_stats[ue].ul_bler,ue_id=ind.ue_stats[ue].dl_mcs2,source="RAN"))
            tmp_payload_list.append(json_payload(kpi='bler_dl',timestamp=ind.tstamp,value=ind.ue_stats[ue].dl_bler,ue_id=ind.ue_stats[ue].dl_mcs2,source="RAN"))
            tmp_payload_list.append(json_payload(kpi='data_ul',timestamp=ind.tstamp,value=ind.ue_stats[ue].ul_aggr_bytes_sdus,ue_id=ind.ue_stats[ue].dl_mcs2,source="RAN"))
            tmp_payload_list.append(json_payload(kpi='data_dl',timestamp=ind.tstamp,value=ind.ue_stats[ue].dl_aggr_bytes_sdus,ue_id=ind.ue_stats[ue].dl_mcs2,source="RAN"))
            tmp_payload_list.append(json_payload(kpi='snr',timestamp=ind.tstamp,value=ind.ue_stats[ue].pucch_snr,unit="dBm",ue_id=ind.ue_stats[ue].dl_mcs2,source="RAN"))
            try:
                for payload in tmp_payload_list:
                    self.channel.basic_publish(exchange='',routing_key='rnis_xapp',body=payload)
            except Exception as e:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.remote_rabbitmq_ip,port=self.remote_rabbitmq_port,credentials=self.credentials))
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue='rnis_xapp',durable=True)                    

def connection_flexric():
    ric.init()
    conn = ric.conn_e2_nodes()
    assert(len(conn) > 0)
    for i in range(0, len(conn)):
        logging.info("Global E2 Node [" + str(i) + "]: PLMN MCC = " + str(conn[i].id.plmn.mcc))
    return conn



def main():
    try:
        conn = connection_flexric()
        mac_hndlr = []
        for i in range(0, len(conn)):
            mac_cb = MACCallback()
            hndlr = ric.report_mac_sm(conn[i].id, ric.Interval_ms_10, mac_cb)
            mac_hndlr.append(hndlr)
            time.sleep(1)
        while True:    
         time.sleep(10)     
    except Exception:
        logging.error('Error while executing the xApp')
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
