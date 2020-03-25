# GoogleCloud GKE Example

## Prerequisites:

  * Cloudify Manager with Latest GCP and Kubernetes Plugins.

### Creating secrets

Replace <value> with actual values, without the <>

```shell
cfy secrets create gcp_credentials -f </path/to/service_account.json>
cfy secrets create gcp_zone -s <google_zone>
```


### Running the example

```shell
cfy install blueprint.yaml -i resource_prefix=<value>
```
