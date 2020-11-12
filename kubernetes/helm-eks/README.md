# Amazon EKS Example

## Prerequisites:

  * Cloudify Manager with Latest AWS and Kubernetes Plugins.

### Creating secrets

Create secrets according to your AWS credentials.
and name of already created keypair

Replace <value> with actual values, without the <>

```shell
cfy secrets create aws_access_key_id --secret-string <value>
cfy secrets create aws_secret_access_key --secret-string <value>
cfy secrets create aws_keypair --secret-string <value>
```


### Running the example

```shell
cfy install blueprint.yaml -i eks_cluster_name=eks_cluster -i eks_nodegroup_name=eks_node_group
-i service_account_name=examples-user -i service_account_namespace=default
```
