#   Copyright 2023 OAI-MEP Authors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#   Contact: netsoft@eurecom.fr


from jinja2 import Environment, FileSystemLoader
import datetime
import six
import typing
import logging
import os
import yaml
import sys
from oai_mep.utils.database import MEPDB

CONFIG_FILE = str(os.getenv('CONFIG_FILE','../../../etc/configuration.yaml'))
MOUNT_CONFIG = str(os.getenv('MOUNT_CONFIG','no')).lower()

def read_yamlfile(filename):
    '''
    translates yaml to dict
    '''
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, filename)
    try:
        with open(filename) as f:
            v = yaml.safe_load(f)
        return v
    except Exception as e:
        print(f"Exception in reading the configuration file {e}")
        return

def render_config(CONFIG_FILE,MOUNT_CONFIG='no'):
    def render(filepath,values):
        env = Environment(loader=FileSystemLoader(os.path.dirname(filepath)))
        jinja_template = env.get_template(os.path.basename(filepath))
        template_string = jinja_template.render(env=values)
        return template_string
    #list of all the environment variables
    env_variables = {}
    for name, value in os.environ.items():
        env_variables.update({name:value})
    if MOUNT_CONFIG != "yes":
        output = render(CONFIG_FILE,env_variables)
        with open(CONFIG_FILE, "w") as fh:
            fh.write(output)
        print(f"Configuration file {CONFIG_FILE} is ready")
    else:
        print("Configuration file is mounted")

    return read_yamlfile(CONFIG_FILE)

#configuration
configuration = render_config(CONFIG_FILE,MOUNT_CONFIG)

mepdb = MEPDB(configuration)

##### Loger
log = logging.getLogger(__name__)

log_level = configuration['application']['loglevel'] 

if log_level == 'debug':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
elif log_level == 'info':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
elif log_level == 'error':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.ERROR)


#python upto 3.6
# def _deserialize(data, klass):
#     """Deserializes dict, list, str into an object.

#     :param data: dict, list or str.
#     :param klass: class literal, or string of class name.

#     :return: object.
#     """
#     if data is None:
#         return None

#     if klass in six.integer_types or klass in (float, str, bool):
#         return _deserialize_primitive(data, klass)
#     elif klass == object:
#         return _deserialize_object(data)
#     elif klass == datetime.date:
#         return deserialize_date(data)
#     elif klass == datetime.datetime:
#         return deserialize_datetime(data)
#     elif type(klass) == typing.GenericMeta:
#         if klass.__extra__ == list:
#             return _deserialize_list(data, klass.__args__[0])
#         if klass.__extra__ == dict:
#             return _deserialize_dict(data, klass.__args__[1])
#     else:
#         return deserialize_model(data, klass)


def _deserialize(data, klass):
    """Deserializes dict, list, str into an object.

    :param data: dict, list or str.
    :param klass: class literal, or string of class name.

    :return: object.
    """
    if data is None:
        return None

    if klass in six.integer_types or klass in (float, str, bool):
        return _deserialize_primitive(data, klass)
    elif klass == object:
        return _deserialize_object(data)
    elif klass == datetime.date:
        return deserialize_date(data)
    elif klass == datetime.datetime:
        return deserialize_datetime(data)
    elif hasattr(klass, '__origin__'):
        if klass.__origin__ == list:
            return _deserialize_list(data, klass.__args__[0])
        if klass.__origin__ == dict:
            return _deserialize_dict(data, klass.__args__[1])
    else:
        return deserialize_model(data, klass)


def _deserialize_primitive(data, klass):
    """Deserializes to primitive type.

    :param data: data to deserialize.
    :param klass: class literal.

    :return: int, long, float, str, bool.
    :rtype: int | long | float | str | bool
    """
    try:
        value = klass(data)
    except UnicodeEncodeError:
        value = six.u(data)
    except TypeError:
        value = data
    return value


def _deserialize_object(value):
    """Return a original value.

    :return: object.
    """
    return value


def deserialize_date(string):
    """Deserializes string to date.

    :param string: str.
    :type string: str
    :return: date.
    :rtype: date
    """
    try:
        from dateutil.parser import parse
        return parse(string).date()
    except ImportError:
        return string


def deserialize_datetime(string):
    """Deserializes string to datetime.

    The string should be in iso8601 datetime format.

    :param string: str.
    :type string: str
    :return: datetime.
    :rtype: datetime
    """
    try:
        from dateutil.parser import parse
        return parse(string)
    except ImportError:
        return string


def deserialize_model(data, klass):
    """Deserializes list or dict to model.

    :param data: dict, list.
    :type data: dict | list
    :param klass: class literal.
    :return: model object.
    """
    instance = klass()

    if not instance.swagger_types:
        return data

    for attr, attr_type in six.iteritems(instance.swagger_types):
        if data is not None \
                and instance.attribute_map[attr] in data \
                and isinstance(data, (list, dict)):
            value = data[instance.attribute_map[attr]]
            setattr(instance, attr, _deserialize(value, attr_type))

    return instance


def _deserialize_list(data, boxed_type):
    """Deserializes a list and its elements.

    :param data: list to deserialize.
    :type data: list
    :param boxed_type: class literal.

    :return: deserialized list.
    :rtype: list
    """
    return [_deserialize(sub_data, boxed_type)
            for sub_data in data]


def _deserialize_dict(data, boxed_type):
    """Deserializes a dict and its elements.

    :param data: dict to deserialize.
    :type data: dict
    :param boxed_type: class literal.

    :return: deserialized dict.
    :rtype: dict
    """
    return {k: _deserialize(v, boxed_type)
            for k, v in six.iteritems(data)}
