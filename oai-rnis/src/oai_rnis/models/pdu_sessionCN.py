# Copyright © 2023 the MEP-OAI Authors

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
# API Version: 0.0.1
# Contact: netsoft@eurecom.fr

class PDUSession:
    def __init__(self,id,supi, timestamp, type=None, plmn=None, qos_flows=None, snssai=None,  ue_ip=None):
        self.__type = type
        self.__id = id
        self.__plmn = plmn
        self.__qos_flows = qos_flows
        self.__snssai = snssai
        self.__supi = supi
        self.__ue_ip = ue_ip
        self.__timestamp = timestamp

    @property
    def type(self):
        return self.__type

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def id(self):
        return self.__id

    @property
    def plmn(self):
        return self.__plmn
    
    @property
    def qos_flows(self):
        return self.__qos_flows
    
    @property
    def snssai(self):
        return self.__snssai

    @property
    def supi(self):
        return self.__supi
    
    @property
    def ue_ip(self):
        return self.__ue_ip