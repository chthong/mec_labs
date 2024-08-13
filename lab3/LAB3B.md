# Lab 3B : MANO with Kubernetes

* VM Machine: MANOv15-base
* power on this machine ( make sure you turn off other machines )

# Step 
* rename the machine 
```sh 
sudo hostnamectl hostname osmXX 
```
>> XX is your student no. 
>> Logout and Login to verify name change

# Step 
* Install OSM (standard installation)

```sh
wget https://osm-download.etsi.org/ftp/osm-15.0-fifteen/install_osm.sh

chmod +x install_osm.sh

./install_osm.sh
```
>> If there is a prompt, read it and press Y to continue
>> it will take 7 minute 42seconds to install ETSI MONA ( Standard installation )


# Step 
* You can access to the UI in the following URL (user:admin, password: admin): http://1.2.3.4, replacing 1.2.3.4 by the IP address of your VM.
![alt text](image.png)

![alt text](image-1.png)


# Step 

* in the shell run the following to verify the installation of ETSI MANO

```sh
kubectl get all -n osm

kubectl -n osm get pods
```

# Step
* OSM client, a python-based CLI for OSM, will be available as well in the host machine. Via the OSM client, you can manage descriptors, NS and VIM complete lifecycle.

```sh
osm --help

```

# Step
* 


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