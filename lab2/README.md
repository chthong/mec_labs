# Lab2A

### Simulated MEC Platform 
* This MEC Platform will run on single machine spec 
* the VM used here is MEC-Platform Ubuntu Desktop Image
* Please make sure you stop/shutdown any other Virtual Machines  ( you can keep it running, but it will slow down the machine )

* username: droot 
* password: -nil-

  ![alt text](image.png)

* The Discovery and Registry Service (DaRS) is the heart of MEC platform. It exposes REST API for mp1 inferace to:

1. Register a new MEC service (post request)
2. Discover hosted MEC services (get request)
3. Filter hosted MEC services based on service-type  (get request)
4. Delete a hosted MEC service (delete request)


# Step 

* Clone the This REPO 
* Navigate to oic-mep 
* Download Docker Images ( Standalone )
* Start the MEC Platform ( MEP )


# Step 
* Add ip/name  172.29.248.3 oai-mep.org  to /etc/host 

```sh
sudo vim /etc/hosts 
172.29.248.3 oai-mep.org 

```


```sh
cd $HOME 

git clone https://github.com/stv707/mec_labs.git

cd $HOME/mec_labs/oai-mep/

docker-compose -f ci-scripts/docker-compose.yaml up -d
```
>> the images already been downloaded.


# Step 
* Verify the MECP is running 

```sh

docker ps 

docker-compose -f ci-scripts/docker-compose.yaml ps 

```
>> All container must show healthy 


# Step 
* View the MEC Platform API and Register new Service and Verify the new Service
* If you make any mistake, bring down the Containers and Bring them up again, this will reset the containers


1. access http://oai-mep.org/service_registry/v1/ui

![alt text](image-1.png)

2. in the swagger API, access GET /discover and select Try-it-out 

3. execute to view the list of service registered in MEC Platform 
    - your respons should be empty but CODE 200

4. Clear the execution 

5. go POST /register > Select Try Out > Clear the Sample JASON and copy and paste below JSON 

```sh 
{
  "description": "description",
  "endpoints": [
    {
      "description": "description",
      "method": "GET",
      "name": "name",
      "parameters": [
        {
          "name": "input_file",
          "type": "binary"
        }
      ],
      "path": "/transcode"
    }
  ],
  "host": "oai-mep.org",
  "name": "video-image-encoder",
  "path": "/v1/video",
  "port": 7898,
  "sid": "sid",
  "type": "AVEncoding"
}
```

6. Verify the RETRUN CODE is 201 ( Service Added Correctly )

7. Try to explore all other API 

>> ALL this API are MEC PLATFORM Spec by ETSI 
>> any MEC Vendor will have all this as per ETSI Spec


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