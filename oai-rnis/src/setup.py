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

from setuptools import setup, find_packages

NAME = "oai_rnis"
VERSION = "2.1.1"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

requirements= ['attrs==21.4.0', 
               'certifi==2021.10.8', 
               'charset-normalizer==2.0.12', 
               'click==8.0.*', 
               'clickclick==20.10.2', 
               'connexion==2.13.0', 
               'Flask==2.0.3', 
               'Flask-PyMongo==2.3.0', 
               'idna==3.3', 
               'pika==1.3.1',
               'importlib-metadata>=3', 
               'inflection==0.5.1', 
               'itsdangerous==2.0.1', 
               'Jinja2==3.0.3', 
               'jsonschema==4.0.0', 
               'MarkupSafe==2.0.1', 
               'packaging==21.3', 
               'pyparsing==3.0.7', 
               'pyrsistent==0.18.0', 
               'python-dateutil==2.6.0', 
               'PyYAML==6.0', 
               'requests==2.27.1', 
               'six==1.16.0', 
               'swagger-spec-validator==2.7.4', 
               'swagger-ui-bundle==0.0.9', 
               'urllib3==1.26.9', 
               'Werkzeug==2.0.0', 
               'zipp==3.6.0']

# #Relative path issue in alpine
# with open("../requirements.txt") as requirement_file:
#     requirements = requirement_file.read().split()

setup(
    name=NAME,
    version=VERSION,
    description="Radio Network Information Northbound API - 5G SA Interface Proposal",
    author_email="netsoft@eurecom.fr",
    url="",
    keywords=["Swagger", "RNIS", "5G"],
    install_requires=requirements,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['oai_rnis=oai_rnis.__main__:main']},
    long_description="""\
    Radio Network Information Service allows MEC Apps to obtain Radio and Network Level Information about UEs connected to the 5G Network
    """
)
