# Setting up Observability

## Installing Grafana and Prometheus
With Helm installed, it is much easier to install Grafana and Prometheus.

These are the lines of code you will want to run:

```
kubectl create namespace monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
# helm repo add stable https://kubernetes-charts.storage.googleapis.com # this is deprecated
helm repo add stable https://charts.helm.sh/stable
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --kubeconfig /etc/rancher/k3s/k3s.yaml
```

Following along with what you saw in the video, install Prometheus and Grafana with Helm. You may have noticed that I installed some CRDs in the video. In version 0.4.2 of the operator, it was needed. As of this update, we are on version 0.7 which no longer needs those CRDs which is why you won't see the command here any longer.

## Install Jaeger

We will now install Jaeger Tracing to our cluster. Run the below code to create the "observability" namespace and install the Jaeger components:

```
kubectl create namespace observability
# Please use the latest stable version
export jaeger_version=v1.28.0 
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/${jaeger_version}/deploy/crds/jaegertracing.io_jaegers_crd.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/${jaeger_version}/deploy/service_account.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/${jaeger_version}/deploy/role.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/${jaeger_version}/deploy/role_binding.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/${jaeger_version}/deploy/operator.yaml
```

## Grant Cluster wide Permissions to Jaeger
Because you want to observe other namespaces, you'll need to go ahead and give Jaeger cluster wide visibility. In the real world, you may limit visibility to specific namespaces, but it isn't unheard of to give yourself cluster visibility.

Run the below commands:
```
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/${jaeger_version}/deploy/cluster_role.yaml
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/${jaeger_version}/deploy/cluster_role_binding.yaml
```


## Install MongoDB

Apply the MongoDB CRDs. Populate the <version> placeholder and run the following kubectl command to deploy your chosen version of the CRDs to your Kubernetes cluster:
```
kubectl apply -f https://raw.githubusercontent.com/mongodb/mongodb-enterprise-kubernetes/<version>/crds.yaml
```

kubectl get secret example-mongodb-admin-admin -o json | jq -r '.data | with_entries(.value |= @base64d)'

{
  "connectionString.standard": "mongodb://my-user:YWRtaW4%3D@example-mongodb-0.example-mongodb-svc.default.svc.cluster.local:27017,example-mongodb-1.example-mongodb-svc.default.svc.cluster.local:27017,example-mongodb-2.example-mongodb-svc.default.svc.cluster.local:27017/admin?replicaSet=example-mongodb&ssl=false",
  "connectionString.standardSrv": "mongodb+srv://my-user:YWRtaW4%3D@example-mongodb-svc.default.svc.cluster.local/admin?replicaSet=example-mongodb&ssl=false",
  "password": "YWRtaW4=",
  "username": "my-user"
}

mongodb://my-user:YWRtaW4%3D@example-mongodb-1.example-mongodb-svc.default.svc.cluster.local:27017