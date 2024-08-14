# Lab 3B : Network Slicing ( Simulated in Kubernetes )


* Login to ssh.cognitoz.my 
```sh 
ssh stuX@cognitoz.my

```
>> X is your student number


### Overview
1. **Multus CNI** will enable pods to have multiple network interfaces.
2. **SR-IOV or VLAN** will be used to create separate network slices.
3. Each pod will be attached to multiple network interfaces corresponding to different network slices.

### Step 1: Set Up a Kubernetes Cluster

Ensure you have a Kubernetes cluster running.

### Step 2: Install Multus CNI

Multus CNI allows Kubernetes pods to have multiple network interfaces. Install Multus on your cluster:

```bash
kubectl apply -f https://raw.githubusercontent.com/k8snetworkplumbingwg/multus-cni/master/deployments/multus-daemonset-thick.yml
```


### Step 3: Create VLAN-based Network Attachments (if not using SR-IOV)

For those without SR-IOV hardware, VLANs can be used to create isolated network slices.

#### a. Create NetworkAttachmentDefinitions

**Create a VLAN-based network slice** using the `NetworkAttachmentDefinition` resource in Kubernetes.

1. **VLAN 10** (e.g., slice1):
   Create a file named `slice1-vlan.yaml`:
   ```yaml
   apiVersion: "k8s.cni.cncf.io/v1"
   kind: NetworkAttachmentDefinition
   metadata:
     name: slice1-vlan
     namespace: labns
   spec:
     config: '{
       "cniVersion": "0.3.1",
       "type": "macvlan",
       "mode": "bridge",
       "master": "eth0",
       "ipam": {
         "type": "static",
         "addresses": [
           {
             "address": "192.168.10.100/24",
             "gateway": "192.168.10.1"
           }
         ]
       }
     }'
   ```

2. **VLAN 20** (e.g., slice2):
   Create a file named `slice2-vlan.yaml`:
   ```yaml
   apiVersion: "k8s.cni.cncf.io/v1"
   kind: NetworkAttachmentDefinition
   metadata:
     name: slice2-vlan
     namespace: labns
   spec:
     config: '{
       "cniVersion": "0.3.1",
       "type": "macvlan",
       "mode": "bridge",
       "master": "eth0",
       "ipam": {
         "type": "static",
         "addresses": [
           {
             "address": "192.168.20.100/24",
             "gateway": "192.168.20.1"
           }
         ]
       }
     }'
   ```

3. **Apply the configurations**:
   ```bash
   kubectl apply -f slice1-vlan.yaml
   kubectl apply -f slice2-vlan.yaml
   ```

### Step 4: Deploy Pods with Multiple Network Interfaces

We will now create pods with multiple network interfaces corresponding to the different network slices.

1. **Create a YAML file for `pod-a`** with connections to both network slices:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: pod-a
     namespace: labns
     annotations:
       k8s.v1.cni.cncf.io/networks: '[{ "name": "slice1-vlan" }, { "name": "slice2-vlan" }]'
   spec:
     containers:
     - name: busybox
       image: radial/busyboxplus:curl
       command: ['sh', '-c', 'sleep 3600']
       stdin: true
       tty: true
   ```

2. **Create a YAML file for `pod-b`** with connections to both network slices:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: pod-b
     namespace: labns
     annotations:
       k8s.v1.cni.cncf.io/networks: '[{ "name": "slice1-vlan" }, { "name": "slice2-vlan" }]'
   spec:
     containers:
     - name: busybox
       image: radial/busyboxplus:curl
       command: ['sh', '-c', 'sleep 3600']
       stdin: true
       tty: true
   ```

3. **Apply the configurations**:
   ```bash
   kubectl apply -f pod-a.yaml
   kubectl apply -f pod-b.yaml
   ```

### Step 6: Verify and Test the Network Slices

1. **Check the Network Interfaces** in the pods to ensure they are attached to both slices:
   ```bash
   kubectl exec -n labns pod-a -- ip a
   kubectl exec -n labns pod-b -- ip a
   ```

2. **Test Connectivity** between the pods in different slices:

   - **Ping from `pod-a` to `pod-b` on `slice1`**:
     ```bash
     kubectl exec -n labns pod-a -- ping 192.168.10.100
     ```

   - **Ping from `pod-a` to `pod-b` on `slice2`**:
     ```bash
     kubectl exec -n labns pod-a -- ping 192.168.20.100
     ```

   This will verify the connectivity across different network slices.

### Step 7: Cleanup

After completing your lab, you can clean up the resources:

```bash
kubectl delete -f pod-a.yaml
kubectl delete -f pod-b.yaml
kubectl delete -f slice1-vlan.yaml
kubectl delete -f slice2-vlan.yaml
kubectl delete namespace labns
```