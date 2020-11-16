# Helm 3 Example

This example demonstrates deployment of EKS cluster and install an Helm chart on top of it using Cloudify. 
## Prerequisites:

  * Cloudify Manager with latest AWS, Kubernetes, Utilities, Helm Plugins.

### Creating secrets

Create secrets according to your AWS credentials.

Replace <value> with actual values, without the <>

```shell
cfy secrets create aws_access_key_id --secret-string <value>
cfy secrets create aws_secret_access_key --secret-string <value>
```

Create secretes that will contain your kubernetes_config and kubernetes_token:
The values will be updated by eks blueprint that runs as a component, so actually the values given when creating those secrets will be overridden.

```shell
cfy secrets create kubernetes_config --secret-string <value>
cfy secrets create kubernetes_token --secret-string <value>
```

### Running the example
For example, in order to install bitnami/postgresql Helm chart:

```shell
cfy install blueprint.yaml -i repo_name=bitnami -i chart_name=postgresql
-i repo_url=https://charts.bitnami.com/bitnami 
```

### Install Helm chart on an existing cluster
The example above creates EKS cluster, If you want to use your own kubernetes cluster, look at these [Helm examples.](https://github.com/cloudify-incubator/cloudify-helm-plugin/tree/master/examples) 