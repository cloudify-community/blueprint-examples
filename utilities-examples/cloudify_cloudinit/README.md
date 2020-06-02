# Cloudify Utilities: Cloud-Init

Cloud-Init is the standard for configuration of cloud instances. See
[examples](http://cloudinit.readthedocs.io/en/latest/topics/examples.html).

For more information, read the [documentation](https://github.com/cloudify-incubator/cloudify-utilities-plugin/blob/master/cloudify_cloudinit/README.md).

## Examples

### example 1:

blueprint [aws.yaml](./aws.yaml)

On this example we use the cloud init on aws.

Provide the following secrets:
 * aws_access_key_id
 * aws_secret_access_key
 
### example 2:

blueprint [simple.yaml](./simple.yaml)

Use cloud init to install packeges on centos machine.