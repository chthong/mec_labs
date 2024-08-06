# Lab1A

# Step 

* Prepare System for Docker
* Login to local Ubuntu System ( Verify Connectivity and IP and Internet access )

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
```

# Step 
* install cri-dockerd 
* This is needed as Docker SHIM have been removed from upstream Kubernetes


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



# Step

```sh

```

# Step



```sh

```

END