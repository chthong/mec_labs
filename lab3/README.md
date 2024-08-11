#  Explore Kubernetes Cluster 


Explore and Verify Kubernetes ( DO )
# Step 1 

1. Access hosted Linux System with your assigned username 
2. Add your assigned kubeconfig.yaml to .kube/config 


```sh

User@vmXXX#> cat .kube/config 

User@vmXXX#> kubectl get nodes 

User@vmXXX#> kubectl get nodes -o wide

User@vmXXX#> kubectl describe node <node_name>

```

# Step 2 

Open a SSH connection to worker node
 - replace node_name with your first worker node name 

```sh
User@vmXXX#> kubectl get nodes 

User@vmXXX#> kubectl debug node/<node_name> -it --image=mcr.microsoft.com/aks/fundamental/base-ubuntu:v0.0.11

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

User@vmXXX#> kubectl get pods --field-selector status.phase!=Running 
NAME                                           READY   STATUS      RESTARTS   AGE
node-debugger-XXX                              0/1     Completed   0          13m

User@vmXXX#> kubectl  delete pod node-debugger-XXX

```

# Step 3 

Explore all running Containers/Pods and Configurations
```sh

User@vmXXX#>  kubectl get ns 

User@vmXXX#>  kubectl get po -n kube-system

User@vmXXX#>  kubectl get service 

User@vmXXX#>  kubectl get deployments

User@vmXXX#>  kubectl get daemonsets

User@vmXXX#>  kubectl get replicasets 

User@vmXXX#>  kubectl get statefulsets 

User@vmXXX#>  kubectl get configmap 

User@vmXXX#>  kubectl get secret 

User@vmXXX#>  kubectl get storageclass 

User@vmXXX#>  kubectl get pv

User@vmXXX#>  kubectl get pvc

User@vmXXX#>  kubectl get cronjobs

User@vmXXX#>  kubectl get jobs

User@vmXXX#>  kubectl get endpoints

```

# Step 4 

Deploy Simple App to Kubernetes
```sh
User@vmXXX#>  kubectl get deployments

User@vmXXX#>  kubectl get service 

User@vmXXX#>  kubectl apply -f voteapp.yaml 

User@vmXXX#>  kubectl get service voteapp-frontend
** Browse to the external IP address to verify app is running

```

# Step 5

Remove previously deployed App and verify there is no Service, Pod and Deployment defined 
```sh 

User@vmXXX#>  kubectl delete -f voteapp.yaml 

User@vmXXX#>  kubectl get deployments

User@vmXXX#>  kubectl get svc

User@vmXXX#>  kubectl get po

```

#### END