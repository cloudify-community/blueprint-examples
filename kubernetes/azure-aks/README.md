# Azure AKS Example

## Prerequisites:

  * Cloudify Manager with Latest Azure and Kubernetes Plugins.

### Creating secrets

Replace <value> with actual values, without the <>

```shell
cfy secrets create azure_subscription_id --secret-string <value>
cfy secrets create azure_tenant_id --secret-string <value>
cfy secrets create azure_client_id --secret-string <value>
cfy secrets create azure_client_secret --secret-string <value>
```


### Running the example

```shell
cfy install blueprint.yaml -i resource_group_name=<value> -i managed_cluster_name=<value>
-i public_key=<value> -i location=<your azure location>
```
the location input is optional("eastus2" is default value).