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

kubectl get nodes 
** REPLACE THE NODENAME from THE OUTPUT 

curl http://localhost:8001/api/v1/nodes/NODENAME 

```
# Step 7 

```sh 
kubectl api-resources 

kubectl api-versions

kubectl config view

```

# Kubernetes API based access [ Why Kubernetes is the perfect platform for MEC ]


### **1. Start `kubectl proxy`**
First, start the `kubectl proxy` to enable API access via `localhost:8001`:
```bash
kubectl proxy &
```
This will start the proxy in the background and open port `8001` for API access.

### **2. Create a Namespace**
Let's create a namespace called `my-lab`:
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"apiVersion": "v1", "kind": "Namespace", "metadata": {"name": "my-lab"}}' \
http://localhost:8001/api/v1/namespaces
```

### **3. Create a Pod (nginx)**
Create a pod named `nginx-pod` in the `my-lab` namespace running the `nginx` image:
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{
  "apiVersion": "v1",
  "kind": "Pod",
  "metadata": {
    "name": "nginx-pod",
    "namespace": "my-lab"
  },
  "spec": {
    "containers": [
      {
        "name": "nginx-container",
        "image": "nginx",
        "ports": [
          {
            "containerPort": 80
          }
        ]
      }
    ]
  }
}' http://localhost:8001/api/v1/namespaces/my-lab/pods
```

### **4. Create a LoadBalancer Service for the Pod**
Create a LoadBalancer service to expose the `nginx-pod`:
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{
  "apiVersion": "v1",
  "kind": "Service",
  "metadata": {
    "name": "nginx-service",
    "namespace": "my-lab"
  },
  "spec": {
    "selector": {
      "name": "nginx-pod"
    },
    "ports": [
      {
        "protocol": "TCP",
        "port": 80,
        "targetPort": 80
      }
    ],
    "type": "LoadBalancer"
  }
}' http://localhost:8001/api/v1/namespaces/my-lab/services
```

### **5. Verify the API Calls**
Verify that the namespace, pod, and service were created successfully:
- **Namespace**:
  ```bash
  curl http://localhost:8001/api/v1/namespaces/my-lab
  ```
- **Pod**:
  ```bash
  curl http://localhost:8001/api/v1/namespaces/my-lab/pods/nginx-pod
  ```
- **Service**:
  ```bash
  curl http://localhost:8001/api/v1/namespaces/my-lab/services/nginx-service
  ```

### **6. Delete the Resources Using the API**
Delete the pod, service, and namespace using the following `curl` commands:

- **Delete the Pod**:
  ```bash
  curl -X DELETE http://localhost:8001/api/v1/namespaces/my-lab/pods/nginx-pod
  ```
- **Delete the Service**:
  ```bash
  curl -X DELETE http://localhost:8001/api/v1/namespaces/my-lab/services/nginx-service
  ```
- **Delete the Namespace**:
  ```bash
  curl -X DELETE http://localhost:8001/api/v1/namespaces/my-lab
  ```

### **7. Create a Deployment Using `stv707/kubia:v14` with 4 Replicas**
Create a deployment named `kubia-deployment` with 4 replicas:
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{
  "apiVersion": "apps/v1",
  "kind": "Deployment",
  "metadata": {
    "name": "kubia-deployment",
    "namespace": "my-lab"
  },
  "spec": {
    "replicas": 4,
    "selector": {
      "matchLabels": {
        "app": "kubia"
      }
    },
    "template": {
      "metadata": {
        "labels": {
          "app": "kubia"
        }
      },
      "spec": {
        "containers": [
          {
            "name": "kubia-container",
            "image": "stv707/kubia:v14",
            "ports": [
              {
                "containerPort": 8080
              }
            ]
          }
        ]
      }
    }
  }
}' http://localhost:8001/apis/apps/v1/namespaces/my-lab/deployments
```

### **8. Scale the Deployment to 8 Replicas**
Scale the `kubia-deployment` to 8 replicas:
```bash
curl -X PATCH -H "Content-Type: application/merge-patch+json" \
-d '{"spec": {"replicas": 8}}' \
http://localhost:8001/apis/apps/v1/namespaces/my-lab/deployments/kubia-deployment
```

### **9. Verify the Scaling**
Verify that the deployment now has 8 replicas:
```bash
curl http://localhost:8001/apis/apps/v1/namespaces/my-lab/deployments/kubia-deployment
```

### **Conclusion**
This step-by-step guide demonstrates how to interact with Kubernetes via the API using `kubectl proxy` and `curl`. You’ve created a namespace, pod, service, deployment, scaled the deployment, and cleaned up the resources, all using API calls. This setup can be very useful for learning and automation purposes.

#### END