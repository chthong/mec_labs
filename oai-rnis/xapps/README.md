<table style="border-collapse: collapse; border: none;">
  <tr style="border-collapse: collapse; border: none;">
    <td style="border-collapse: collapse; border: none;">
      <a href="http://www.openairinterface.org/">
         <img src="../docs/images/oai_final_logo.png" alt="" border=3 height=50 width=150>
         </img>
      </a>
    </td>
    <td style="border-collapse: collapse; border: none; vertical-align: center;">
      <b><font size = "5">OpenAirInterface RNIS xApp</font></b>
    </td>
  </tr>
</table>



**TABLE OF CONTENTS**

1.  [RNIS xApp](#1-rnis-xapp)
2.  [Working](#2-working)
3.  [How to use](#3-how-to-use)

## 1. RNIS xApp

RNIS xApp is designed (following the O-RAN definition) using FlexRIC SDK. It interacts with FlexRIC to collect a set of predefined metrics from RAN.

RNIS xApp collect below metrics:


|Metrics    |Information                          |
|-----------|-------------------------------------|
|cqi        |channel quality                      |
|rsrp       |Reference Signal Received Power      |
|mcs_ul     |Modulation and Coding Scheme uplink  |
|mcs_dl     |Modulation and Coding Scheme downlink|
|phr        |Power Headroom Report                |
|bler_ul    |Block Error Rate  uplink             |
|bler_dl    |Block Error Rate  downlink           |
|errors_dl  |errors downlink                      |
|errors_ul  |errors uplink                        |
|data_ul    |data transmitted  uplink             |
|data_dl    |data transmitted  downlink           |
|amf_ngap_id|ID of the UE in AMF                  |
|snr        |Signal to Noise Ratio                |


The each `metrics` is sent in below json format

```
{
	"kpi": kpi-name,
	"source": source-of-the-kpi,
	"timestamp": timestamp,
	"unit": unit-of-the-kpi,
	"value": value-of-the-kpi,
	"labels": {
		"amf_ue_ngap_id": <>,
	}
}
```


## 2. Working

The xApp is stateless it collects RAN metrics via FlexRIC SQLite and sends it to RabbitMQ Broker for interested consumers. In `config.ini` the xApp users have to specify `RabbitMq` host related information and FlexRIC `SQLite` information

Example

```
[XAPP]
RemoteRabbitMqAddress = 172.21.16.115
RemoteRabbitMqPort = 5672
SQliteDBPath = /path/to/xapp/db/
SQliteDBName = xapp_mep_db1
```

## 3. How to use

To use the xApp you need a running RabbitMq instance and FlexRIC connected to oai-gnb. Here is a quick tutorial on setting up FlexRIC with `oai-gNB`. We will provide instructions for baremetal and docker based setup, later we will use docker-compose to instantiate components.

### 3.1 Baremetal Setup

#### 3.1.1 Setup OAI-gNB
The build and the deployment processes are presented in details in the documentation found [here](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/doc/BUILD.md)

For the sake of simplicity, we just give the commands to build the version that is compatible with the MEP platform.

We use a branch that is compatible with the RNIS. Below the command to clone, checkout, install the prerequisites and build OAI:

``` bash
git clone https://gitlab.eurecom.fr/oai/openairinterface5g.git oai
cd oai/
git checkout mep-compatible
cd cmake_targets
./build_oai -I -w USRP -i  #this will install some dependencies, and its done once
./build_oai  --gNB -c -C -w USRP --ninja
```

These commands assume that you will use OAI with a USRP.

Run the gNB with the a an adequate config file. (don't forget to change the AMF address)
```bash
cd ran_build/build
sudo ./nr-softmodem -O /path/to/config/file/oai-b210-remote-cn.conf --sa -E --continuous-tx
```
`nr-softmodem` process would be running by now

#### 3.1.2 Setup FlexRIC
We used FlexRIC release 1.0.0 deployed on the same machine as OAI. The build and deployment process are documented in the [official repo](https://gitlab.eurecom.fr/mosaic5g/flexric/-/blob/master/README.md?plain=0#flexric). Here we are providing a snippet

After the compilation, and to test the proper connection between FlexRIC and OAI, FlexRIC needs to run first using the command:

```bash
./build/examples/ric/nearRT-RIC
```

Then OAI on an other terminal :

```bash
sudo ./nr-softmodem -O /path/to/config/file/oai-b210-remote-cn.conf --sa -E --continuous-tx
```

By now you should see logs that indicates a new connection in FlexRIC's terminal.

Once the connection is tested, we can now run the xApp that will collect the RAN data using FlecRIC's SDK

#### 3.1.3 Setup RNIS xApp

To prepare the setup environment just run the shell script
```bash
./setup-xapp.sh
```

Now you will need to install the python3 requirements with the command :

```bash
pip3 install -r requirements.txt
```

#### 3.1.4 Configuration
To run the xApp with flexric you will need to specify the SQLite database directory `db` and the database name that will be used by FlexRIC in the configuration file with the command:

```shell
nano /usr/local/etc/flexric/flexric.conf
```

The content should be something like :

```
[NEAR-RIC]
NEAR_RIC_IP = 127.0.0.1

[XAPP]
DB_PATH = /flexric/db/
DB_NAME = xapp_rnis_db
```

For the xApp configuration you will need to specify in `config.ini` file the following:

-  `RemoteRabbitmqAddress` : ip address of RabbitMQ broker used with the MEP platform.
-  `RemoteRabbitmqAddress` : port to communicate with the broker of the MEP platform.
-  `SQliteDBPath` : should be the same as the one in FlexRIC's config file `DB_PATH` key.
-  `SQliteDBName` : should be the same as the one in FlexRIC's config file `DB_NAME` key.


#### 3.1.5 Running all the components
Now that every thing is ready start by running FlexRIC then the gNB and finally the xApp.

By now if a user is connected to the gNodeB, the xApp should be pulling data from FlexRIC's db parsing and pushing it to the broker.

### 3.2 Docker Setup

#### 3.2.1 Build OAI-gNB (optional)
The build and the deployment processes are presented in details in the documentation found [here](https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/doc/BUILD.md)

For the sake of simplicity, we just give the commands to build the version that is compatible with the MEP platform.

We use a branch that is compatible with the RNIS. Below the command to clone, checkout, and build the docker images of the gNB and the UE:

``` bash
git clone https://gitlab.eurecom.fr/oai/openairinterface5g.git oai
cd oai/
git checkout mep-compatible
docker build -f ./docker/Dockerfile.base.ubuntu18 -t ran-base:latest .
docker build -f ./docker/Dockerfile.build.ubuntu18 -t ran-build:latest .
docker build -f ./docker/Dockerfile.gNB.ubuntu18 -t oaisoftwarealliance/oai-gnb:mep-compatible .
```

#### 3.2.2 Build FlexRIC and xAPP Container Image (Optional)

You can pull the flexric docker container image from the official oai docker hub account `oaisoftwarealliance` or you can build it yourself using the command

```
# The command assume you are in xapps/ folder 
docker build -t oaisoftwarealliance/oai-flexric:1.0 -f ../docker/Dockerfile.flexric.ubuntu18.04 . --no-cache
```
At the moment rnis-xapp is inside the same flexric container image 


#### 3.2.4 Start the Setup

If you want to test the xApp individually then you don't need a running rnis instance. The rnis xApp will push metrics automatically to the rabbitMq broker

There is a small order on how to play with the setup

NOTE: We assume you are running the command from this directory i.e `xapps`

1. Start the core network 

```shell
docker-compose -f ../ci-scripts/docker-compose-core-network.yaml up -d
```

Wait till the time all the containes are healthy

2. Start RabbitMq

```shell
docker-compose -f ../ci-scripts/docker-compose.yaml up -d rabbitmq
```

3. Start the oai-rfsim-gnb, oai-rfsim-nrue and oai-flexric

```shell
docker-compose -f ../ci-scripts/docker-compose-ran.yaml up -d oai-gnb oai-nr-ue oai-flexric
```
Wait till the time all the containers are healthy

4. Start the oai-rnis-xapp 

```shell
docker-compose -f ../ci-scripts/docker-compose-ran.yaml up -d oai-rnis-xapp
```

5. Open the RabbitMq Gui http://localhost:15672/ with user/password `user` and `password` in queues you will see `rnis-xapp`. You can also checked the published messages in the logs of `oai-rnis-xapp`. `docker logs oai-rnis-xapp`

6. To stop everything 

```shell
docker-compose -f ../ci-scripts/docker-compose-core-network.yaml down -t2
docker-compose -f ../ci-scripts/docker-compose.yaml down -t2
docker-compose -f ../ci-scripts/docker-compose-ran.yaml down -t2
docker volume rm ci-scripts_shared_lib
```