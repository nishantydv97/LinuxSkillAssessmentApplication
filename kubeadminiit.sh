#!/bin/bash
sudo su
swapoff -a \
&& kubeadm  reset \
&& kubeadm init --pod-network-cidr=10.244.0.0/16 \
&& mkdir -p $HOME/.kube \
&& sudo cp -i  /etc/kubernetes/admin.conf $HOME/.kube/config \
&& sudo chown  $(id -u):$(id -g) $HOME/.kube/config \
&& kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/v0.10.0/Documentation/kube-flannel.yml \
&& kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml \
&& echo Dashboard installed in your pc hit  command kubectl proxy  and  visit http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/
