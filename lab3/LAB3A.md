# LAB3A  Explore Kubernetes Cluster 


Explore and Verify Kubernetes ( DO )
# Step 1 

1. Access hosted Linux System with your assigned username 


```sh

cat .kube/config 

kubectl get nodes 

kubectl get nodes -o wide

kubectl describe node <node_name>

```

# Step 2 

Open a SSH connection to worker node
 - replace node_name with your first worker node name 

```sh
kubectl get nodes 

kubectl debug node/<node_name> -it --image=mcr.microsoft.com/aks/fundamental/base-ubuntu:v0.0.11

root@inst1-aqhd0gso1-rsxhz:/# chroot /host

# crictl ps

# crictl images ls 

# systemctl status kubelet

# systemctl status containerd

# crictl ps | grep kube-proxy

# cat /etc/*rel*

# uname -a

# lscpu 

# free -h 

# exit

root@inst1-aqhd0gso1-rsxhz:/#  exit

kubectl get pods --field-selector status.phase!=Running 
NAME                                           READY   STATUS      RESTARTS   AGE
node-debugger-XXX                              0/1     Completed   0          13m

kubectl  delete pod node-debugger-XXX

```

# Step 3 

Explore all running Containers/Pods and Configurations
```sh

 kubectl get ns 

 kubectl get po -n kube-system

 kubectl get service 

 kubectl get deployments

 kubectl get daemonsets

 kubectl get replicasets 

 kubectl get statefulsets 

 kubectl get configmap 

 kubectl get secret 

 kubectl get storageclass 

 kubectl get pv

 kubectl get pvc

 kubectl get cronjobs

 kubectl get jobs

 kubectl get endpoints

```

# Step 4 

Deploy Simple App to Kubernetes
```sh
 kubectl get deployments

 kubectl get service 

 cd $HOME/mec_labs/lab3/

 kubectl apply -f voteapp.yaml 

 kubectl get service voteapp-frontend
** Browse to the external IP address to verify app is running

kubectl scale --replicas 7 deployment voteapp-frontend

kubectl get pod 

kubectl describe pod  <ANY_PENDING_POD>

kubectl delete -f voteapp.yaml

kubectl get service

kubectl get all 

cp voteapp.yaml voteapp_mod.yaml 

vim voteapp_mod.yaml    ( REMOVE CPU Request / Limit Entry )

kubectl apply -f voteapp_mod.yaml

kubectl apply -f voteapp_mod.yaml

kubectl get pod

kubectl scale --replicas 7 deployment  voteapp-frontend

kubectl get pod

```

# Step 5

Remove previously deployed App and verify there is no Service, Pod and Deployment defined 
```sh 

 kubectl delete -f voteapp.yaml 

 kubectl get deployments

 kubectl get svc

 kubectl get po

```

# Step 6 
```sh
kubectl cluster-info
curl https://xxxxx-aks-dns-xxxxxxx.hcp.southeastasia.azmk8s.io:443 -k

kubectl proxy & 

curl localhost:8001
curl http://localhost:8001/apis/batch
curl http://localhost:8001/api/v1/nodes/node1.example.local

jobs 
kill %1 
```
# Step 7 

```sh 
kubectl api-resources 

kubectl api-versions

kubectl config view

```

#### END