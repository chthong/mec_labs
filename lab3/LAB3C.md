# Lab 3B : Network Slicing ( Simulated in Kubernetes )


* Login to ssh.cognitoz.my 
```sh 
ssh stuX@cognitoz.my

cd $HOME/mec_labs 

git pull 

```
>> X is your student number
>> git pull to sync any new changes from git server

### Overview
1. **Multus CNI** will enable pods to have multiple network interfaces.
2. **SR-IOV or VLAN** will be used to create separate network slices.
3. Each pod will be attached to multiple network interfaces corresponding to different network slices.

### Step 1: Set Up a Kubernetes Cluster

```bash 
kubectl create namespace labns
```

### Step 2: Install Multus CNI

Multus CNI allows Kubernetes pods to have multiple network interfaces. Install Multus on your cluster:

```bash
kubectl apply -f https://raw.githubusercontent.com/k8snetworkplumbingwg/multus-cni/master/deployments/multus-daemonset-thick.yml
```


### Step 3: Create VLAN-based Network Attachments

1. **Apply the configurations**:
   ```bash
   kubectl apply -f slice1-vlan.yaml
   kubectl apply -f slice2-vlan.yaml
   ```

### Step 4: Deploy Pods with Multiple Network Interfaces

We will now create pods with multiple network interfaces corresponding to the different network slices.

1. **Apply the configurations**:
   ```bash
   kubectl apply -f pod-a.yaml
   kubectl apply -f pod-b.yaml
   ```

### Step 5: Verify and Test the Network Slices

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

### Step 8: Cleanup

After completing your lab, you can clean up the resources:

```bash
kubectl delete -f pod-a.yaml

kubectl delete -f pod-b.yaml

kubectl delete -f slice1-vlan.yaml

kubectl delete -f slice2-vlan.yaml

kubectl delete namespace labns

kubectl delete -f https://raw.githubusercontent.com/k8snetworkplumbingwg/multus-cni/master/deployments/multus-daemonset-thick.yml
```