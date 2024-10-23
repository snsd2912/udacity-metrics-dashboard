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

- Forward port to localhost
```
kubectl --namespace monitoring port-forward svc/prometheus-grafana --address 0.0.0.0 3000:80
```
- Navigate to localhost:3000 on localhost
- Login with username:admin/password:prom-operator

## Update scrape config

- As we install Grafana and Prometheus in a different namespace with our application. We need to create `ServiceMonitor` resources to allow Prometheus scrape data from other namespace. To do so:

+ Step 1: Update `kube-prometheus-stack` config to allow Prometheus scrape data from other namespace:
```
helm show values prometheus-community/kube-prometheus-stack --namespace monitoring --kubeconfig /etc/rancher/k3s/k3s.yaml > prometheus-default-values.yaml
```

Update `prometheus-default-values.yaml` file to:
```
scrapeConfigSelector:
  matchLabels:
    release: prometheus
```

Update the kube-prometheus-stack with new config:
```
helm upgrade prometheus prometheus-community/kube-prometheus-stack --namespace monitoring -f prometheus-default-values.yaml --kubeconfig /etc/rancher/k3s/k3s.yaml
```

+ Step 2: Create Service Monitor for each service, make sure that each ServiceMonitor has the same labels has define in `scrapeConfigSelector`. In this case is ```release: prometheus```.

+ Step 3: Expose prometheus target to local and check if the new targets is applied.

```
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus  --address 0.0.0.0  9090:9090
kubectl port-forward svc/backend-service --address 0.0.0.0 8081:8081
```

Access at http://localhost:9090/targets.

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

## Install Jaeger instace

- Install Jaeger using the official document [here](https://tyk.io/docs/product-stack/tyk-gateway/advanced-configurations/distributed-tracing/open-telemetry/otel_jaeger_k8s/).

- Verify:
```
kubectl get jaegers -n observability
```

- Forward port:
```
kubectl port-forward -n observability  service/jaeger-all-in-one-query --address 0.0.0.0 16686:16686
```

## Install MongoDB

- Follow this document to install MongoDB on K8s cluster: https://medium.com/@tanmaybhandge/mongodb-from-basics-to-deployment-on-kubernetes-c1ced7143a6c

- Get secret string:
```
kubectl get secret example-mongodb-admin-admin -o json | jq -r '.data | with_entries(.value |= @base64d)'

{
  "connectionString.standard": "mongodb://my-user:YWRtaW4%3D@example-mongodb-0.example-mongodb-svc.default.svc.cluster.local:27017,example-mongodb-1.example-mongodb-svc.default.svc.cluster.local:27017,example-mongodb-2.example-mongodb-svc.default.svc.cluster.local:27017/admin?replicaSet=example-mongodb&ssl=false",
  "connectionString.standardSrv": "mongodb+srv://my-user:YWRtaW4%3D@example-mongodb-svc.default.svc.cluster.local/admin?replicaSet=example-mongodb&ssl=false",
  "password": "YWRtaW4=",
  "username": "my-user"
}
```