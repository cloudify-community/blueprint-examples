# GoogleCloud GKE Example

## Prerequisites:

  * Cloudify Manager with Latest GCP and Kubernetes Plugins.

### Creating secrets

Replace <value> with actual values, without the <>

```shell
cfy secrets create gcp_credentials -f </path/to/service_account.json>
```


### Running the example

```shell
cfy install blueprint.yaml -i resource_prefix=<value>
```
gcp zone also can be passed as input(if not passed the default zone will serve as the program zone).
In order to pass the zone, add "-i zone=<your_zone>" to the command above.