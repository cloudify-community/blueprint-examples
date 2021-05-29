# Azure AKS Monitor Example

## Prerequisites:

  * Cloudify Manager with Latest Azure, Kubernetes, Utilities and Cloudify-web-monitoring Plugins.


### Description:

This example deploys AKS cluster and install a simple flask application that you can change the response time of URL,
and create a monitor deployment that will measure HTTP server response time and will trigger a scale up workflow
if that response time is above a threshold. The workflow will scale the cluster in AKS adding a worker to it.
After the cooldown timer has passed and the low threshold is reached Cloudify will trigger a scale down workflow for AKS cluster.


### Creating secrets

Replace <value> with actual values, without the <>

```shell
cfy secrets create azure_subscription_id --secret-string <value>
cfy secrets create azure_tenant_id --secret-string <value>
cfy secrets create azure_client_id --secret-string <value>
cfy secrets create azure_client_secret --secret-string <value>
```

### Running the example

To install the AKS cluster that we will be monitoring :

```shell
cfy install cluster.yaml -b Cluster
```

To install the monitoring deployment that will be triggered every 1 minute and check the response time for the URL :

```shell
cfy install monitor.yaml -b Monitor -i cluster_deployment_name='Cluster'
```

### Trigger Scale Up/Scale Down


You can change the response time of URL , by accessing flask_app_endpoint output URL :

append `/change/{number of seconds to add to response time}`

for example :

`/change/2` which adds 2 seconds to the response time and that will trigger scale up

then :

`/change/0` which returns the response time back to normal and that will trigger scale down
