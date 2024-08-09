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
# coding: utf-8

import sys

if sys.version_info < (3, 7):
    import typing

    def is_generic(klass):
        """ Determine whether klass is a generic class """
        return type(klass) == typing.GenericMeta

    def is_dict(klass):
        """ Determine whether klass is a Dict """
        return klass.__extra__ == dict

    def is_list(klass):
        """ Determine whether klass is a List """
        return klass.__extra__ == list

else:

    def is_generic(klass):
        """ Determine whether klass is a generic class """
        return hasattr(klass, '__origin__')

    def is_dict(klass):
        """ Determine whether klass is a Dict """
        return klass.__origin__ == dict

    def is_list(klass):
        """ Determine whether klass is a List """
        return klass.__origin__ == list