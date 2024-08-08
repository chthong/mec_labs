# Lab1A

# Step 

* Prepare System for Docker
* Login to local Ubuntu VM  ( Verify Connectivity and IP and Internet access )
* Default username: steve 
* Default password: -nil-

```sh 
sudo hostnamectl hostname edgeXX
```
>> Replace XX with your student number
>> Logout and relogin to verify system name

* Install Docker + cri-dockerd 

```sh
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done

curl -fsSL https://get.docker.com -o get-docker.sh

sh get-docker.sh

sudo docker version
```

# Step
* Setup non-root access for Docker Management 

```sh
sudo usermod -aG docker $USER

newgrp docker

docker run hello-world

docker ps  -a

docker rm -f <CONTAINER ID of hello-world> 
```

# Step 
* install cri-dockerd 
* This is needed for Edge Lab as Docker SHIM have been removed from upstream Kubernetes


```sh
wget https://github.com/Mirantis/cri-dockerd/releases/download/v0.3.14/cri-dockerd_0.3.14.3-0.ubuntu-jammy_amd64.deb

sudo dpkg -i cri-dockerd_0.3.14.3-0.ubuntu-jammy_amd64.deb

cri-dockerd --version

rm -rf cri-dockerd_0.3.14.3-0.ubuntu-jammy_amd64.deb
```
>> the cri-dockerd --version must return cri-dockerd 0.3.14 (683f70f)


# Step 
* Install CNI for Kubernetes Support 

```sh
cd mec_labs/lab1/

. install-cni.sh

```

# Step
* Build and Deploy simple web server docker containers 

```sh
cd $HOME/mec_labs/lab1/docker-web/

docker build -t webserver1 .
docker build -t webserver2 .
docker build -t webserver3 .

docker images 

docker network create mynetwork

docker run -d --name web1 --network mynetwork --hostname web1 webserver1
docker run -d --name web2 --network mynetwork --hostname web2 webserver2
docker run -d --name web3 --network mynetwork --hostname web3 webserver3

```

# Step
* Build and Deploy Load Balancer ( CNF - Containerized Network Function )

```sh
cd $HOME/mec_labs/lab1/docker-lb/

docker build -t my-load-balancer .

docker images 

docker run -d --name my-haproxy -p 80:80 --network mynetwork my-load-balancer

docker ps 

docker logs my-haproxy

curl localhost
```

# Step

* Run VPN Server CNF ( Containerized Network Function )

```sh
docker pull openvpn/openvpn-as

docker images

mkdir $HOME/vpn

docker run -d --name=openvpn-as --cap-add=NET_ADMIN -p 943:943 -p 443:443 -p 1194:1194/udp -v $HOME/vpn/:/openvpn openvpn/openvpn-as

docker logs openvpn-as | grep 'Auto-generated pass'

```
>> Login to <DOCKER-HOST-IP:/>
>> using the generated password, you can login to the CNF OpenVpn 
>> username : openvpn 


# Step
* Clean up the containers

```sh
docker ps -a 
docker rm -f <Container ID> 

docker network ls 
docker network rm <UNWANTED_NETWORK>

```
## END of Lab1A


# LAB1B
# Step
* Install docker-compose 

```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose version
```

# Step
* You will now install Open Baton 
* Project link:  
* Open Baton is an open source platform providing a comprehensive implementation of the ETSI NFV Management and Orchestration (MANO) specification.

* Open Baton provides multiple mechanisms for interoperating with different VNFM vendor solutions. It has a modular architecture which can be easily extended for supporting additional use cases.

* It integrates with OpenStack as standard de-facto VIM implementation, and provides a driver mechanism for supporting additional VIM types. It supports Network Service management either using the provided Generic VNFM and Juju VNFM, or integrating additional specific VNFMs. It provides several mechanisms (REST or PUB/SUB) for interoperating with external VNFMs.

* It can be combined with additional components (Monitoring, Fault Management, Autoscaling, and Network Slicing Engine) for building a unique MANO comprehensive solution.

* Project git: https://github.com/openbaton
* Project Doc: https://openbaton-docs.readthedocs.io/en/latest/

```sh
 mkdir $HOME/obaton
 cd $HOME/obaton 

 curl -o docker-compose.yml https://raw.githubusercontent.com/openbaton/bootstrap/master/docker-compose.yml
```

# Step
* Examine the docker-compose.yaml file and change any Password variables to your own password

```sh
more docker-compose.yaml

vim docker-compose.yaml
```

# Step
* Verify the syntax of docker-compose.yaml 

```sh
docker-compose config --quiet && printf "OK\n" || printf "ERROR\n"
```

# Step
* Bring up all the containers for NFVO 

```sh

export HOST_IP=YOUR_LOCAL_IP 

docker-compose up -d
```
>> YOUR_LOCAL_IP is the ip address of the VM ethernet interface
>> Download and Up will take 5 ~ 7 Minute

# Step
* once images are downloaded and started run logs to verify everything is running
```sh
docker-compose ps

docker-compose logs -f 
```
>> Control+C after reviewing the Logs, then rerun docker-compose ps

# Step
* After completing the installation, you should be able to reach the dashboard of the NFVO at the following url: http://your-ip-here:8080

* When accessing the dashboard, you will be prompted for a username and password. The first access can only be done with the super user ("admin") created during the installation process (the default value is "openbaton")

* register a new pop of type docker

* Manage PopS > PoP Instances > Register a New PoP > File Input 

```sh
{
  "name": "Local-VIM-Docker",
  "authUrl": "unix:///var/run/docker.sock",
  "tenant": "1.32",
  "username": "admin",
  "password": "openbaton",
  "type": "docker",
  "location": {
    "name": "Berlin",
    "latitude": "52.525876",
    "longitude": "13.314400"
  }
}

```
# Step
* You will go through the deployment of Iperf client and server in two different Docker containers.
* This is a Simulated MANO Deployment 
* in Real Life this is deployed to OpenStack VIM / Enterprise Docker/Containers that supports API based MANO 


```sh
cd $HOME/mec-labs/lab1/docker-iperfclient 

docker build -t iperfclient .

cd $HOME/mec-labs/lab1/docker-iperfserver

docker build -t iperfserver .
```

# Step
* After this, you need to refresh the VIM on order to see the new images: go to Manage PoPs→PoP instances→ID and click on the two round arrows close to the name. This will trigger the Vim refresh.


* Afterwards, you need to create a NSD. From the NFVO dashboard, go to Catalogue→NS Descriptors→On Board NSD→Upload JSON and paste this JSON content:

```sh 
{
  "name": "docker Iperf",
  "vendor": "fokus",
  "version": "0.1-ALPHA",
  "vld": [{
    "name": "new-network"
  }],
  "vnfd": [{
    "name": "server",
    "vendor": "TUB",
    "version": "0.2",
    "lifecycle_event": [

    ],
    "configurations": {
      "configurationParameters": [],
      "name": "server-configuration"
    },
    "virtual_link": [{
      "name": "new-network"
    }],
    "vdu": [{
      "vm_image": [
        "iperfserver:latest"
      ],
      "scale_in_out": 2,
      "vnfc": [{
        "connection_point": [{
          "virtual_link_reference": "new-network"
        }]
      }]
    }],
    "deployment_flavour": [{
      "flavour_key": "m1.small"
    }],
    "type": "server",
    "endpoint": "docker"
  }, {
    "name": "client",
    "vendor": "TUB",
    "version": "0.2",
    "lifecycle_event": [

    ],
    "configurations": {
      "configurationParameters": [],
      "name": "server-configuration"
    },
    "virtual_link": [{
      "name": "new-network"
    }],
    "vdu": [{
      "vm_image": [
        "iperfclient:latest"
      ],
      "scale_in_out": 2,
      "vnfc": [{
        "connection_point": [{
          "virtual_link_reference": "new-network"
        }]
      }]
    }],
    "deployment_flavour": [{
      "flavour_key": "m1.small"
    }],
    "type": "client",
    "endpoint": "docker"
  }],
  "vnf_dependency": [{
    "source": {
      "name": "server"
    },
    "target": {
      "name": "client"
    },
    "parameters": [
      "hostname"
    ]
  }]
}
```
# Step

* Launch NSD 

>> Beyond this, help yourself to explore the VNFO 


END