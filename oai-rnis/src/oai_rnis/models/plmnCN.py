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


class Plmn:
    def __init__(self, mcc, mnc):
        self.__mcc = mcc
        self.__mnc = mnc

    @property
    def mcc(self):
        return self.__mcc
    
    @property
    def mnc(self):
        return self.__mnc

    def __eq__(self, __o: object) -> bool:
        return (self.__mcc == __o.mcc) and (self.__mnc == __o.mnc)