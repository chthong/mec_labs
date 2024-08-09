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

import flask
from flask import request, jsonify
import socket   
import json
import requests
collected_data = {}

hostname=socket.gethostname()   
ip_addr= "192.168.70.1" #socket.gethostbyname(hostname)  
port = 30020

print(f"Dashboard URL --> http://{ip_addr}:{port}/dashboard")

### create a subscription for receiving l2 measurements
sub_endpoint = "http://192.168.79.169:8080/v2/subscriptions"
sub_body ={
  "callbackReference": f"http://{ip_addr}:{port}/subscriptions/l2meas-200",
  "filterCriteriaNrMrs": {},
  "subscriptionType": "NrMeasRepUeSubscription",
  "expiryDeadline": {
    "nanoSeconds": 12133423,
    "seconds": 123124234
  }
}
requests.post(url =sub_endpoint, json=sub_body)
print("Subscribed to RNIS")

app = flask.Flask(__name__)

@app.route('/subscriptions/l2meas-200', methods=[ 'POST'])
def receive_notification():
    if request.method == 'POST':
        content = request.get_json(force=True)
        print(content)
        kpis = content["Report"]
        for aid in content["AssociateId"]:
            if aid not in collected_data:
                collected_data[aid] = {}
            for kpi in kpis:
                collected_data[aid]["kpi"] = kpi
                #collected_data[aid]["value"] =  kpi["value"]
                #collected_data[aid]["timestamp"] =  kpi["timestamp"]
    return "OK"

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return "<h1> Network Monitoring Dashboard</h1> " + json.dumps(collected_data)


app.config["DEBUG"] = False
app.run(host=ip_addr,port=port)