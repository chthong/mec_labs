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

# coding: utf-8

#required python version Python +3.8.X 

from setuptools import setup, find_packages

NAME = "oai_mep"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py build && python setup.py install
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
               'importlib-metadata>=3', 
               'inflection==0.5.1', 
               'itsdangerous==2.0.1', 
               'Jinja2==3.0.3', 
               'jsonschema==4.0.0', 
               'MarkupSafe==2.0.1', 
               'packaging==21.3', 
               'pymongo==4.0.2', 
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

# Relative path issue in alpine
# with open("../requirements.txt") as requirement_file:
#     requirements = requirement_file.read().split()

setup(
   name=NAME,
   version=VERSION,
   description="OAI Multi-access Edge Computing Platform",
   author_email="netsoft@eurecom.fr",
   url="",
   keywords=["Swagger", "MEP"],
   install_requires=requirements,
   packages=find_packages(),
   package_data={'': ['swagger/swagger.yaml']},
   include_package_data=True,
   entry_points={
       'console_scripts': ['oai_mep=oai_mep.__main__:main']},
   long_description="""\
   Multi-access Edge Computing platforms (MEP) is a part of the ETSI MEC architecture. Our implementation of MEC platform allows different MEC applications to discover MEP hosted services and register their own service which can be discovered by other MEC applications. OAI MEP follows ETSI GS MEC 003 V3.1.1, MEC appications communicate with MEP via `mp1` interface and MEP communicate with Radio Access Network and Core Network components via `mp2` interface. This swagger defines the discovery and registry serivce of MEP.
   """
)
