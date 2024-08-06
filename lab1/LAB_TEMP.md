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


```

# Step

```sh

```

# Step


```sh

```



# Step

```sh

```

# Step



```sh

```

END