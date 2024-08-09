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

class QosFlow:
    def __init__(self, an_addr, qfi, upf_addr):
        self.__an_addr = an_addr
        self.__qfi = qfi
        self.__upf_addr = upf_addr
    
    @property
    def an_addr(self):
        return self.__an_addr
    
    @property
    def qfi(self):
        return self.__qfi
    
    @property
    def upf_addr(self):
        return self.__upf_addr