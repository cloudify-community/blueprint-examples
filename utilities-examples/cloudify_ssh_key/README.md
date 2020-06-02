# Cloudify Utilities: SSH Key

This plugin enables a user to create a private and public key.

### Notes

- Tested with Cloudify Manager 4.0+.
- For Cloudify Manager 4.0 and above: Private key can be stored in secret store.

For more information about this plugin read the [documentation.](https://docs.cloudify.co/5.0.5/working_with/official_plugins/configuration/utilities/key/)

## Examples:

-[create-secret-agent-key.yaml](./create-secret-agent-key.yaml)
-[create_secret_agent_key_using_exising_secret.yaml](./create_secret_agent_key_using_exising_secret.yaml)
-[create-key-and-store-in-path.yaml](./create-key-and-store-in-path.yaml)

## example 1  

blueprint: create-secret-agent-key.yaml

This basic example covers a trivial scenario:
- Create and store a private key in secret store.
- Create and store a public  key in secret store.

1. Install:

```shell
$ cfy install create-secret-agent-key.yaml -i agent_key_name=my_key
...
$ cfy secrets list
Listing all secrets...

Secrets:
+----------------------------+--------------------------+--------------------------+------------+----------------+------------+-----------------+
|            key             |        created_at        |        updated_at        | visibility |  tenant_name   | created_by | is_hidden_value |
+----------------------------+--------------------------+--------------------------+------------+----------------+------------+-----------------+
|       my_key_private       | 2020-05-27 07:21:55.629  | 2020-05-27 07:21:55.629  |   tenant   | default_tenant |   admin    |      False      |
|       my_key_public        | 2020-05-27 07:21:55.686  | 2020-05-27 07:21:55.686  |   tenant   | default_tenant |   admin    |      False      |
+----------------------------+--------------------------+--------------------------+------------+----------------+------------+-----------------+

```

Notice the secrets were created.


2. Uninstall:

```shell
$  cfy uninstall cloudify-ssh-key
$ cfy secrets list

```
Notice the secrets were deleted.

## example 2 
 
blueprint: create_secret_agent_key_using_exising_secret.yaml
 
This example demonstrates a use of "use_secrets_if_exist" property.

1. Install first example:

```shell
$ cfy install create-secret-agent-key.yaml -i agent_key_name=my_key
...
$ cfy secrets list
Listing all secrets...

Secrets:
+----------------------------+--------------------------+--------------------------+------------+----------------+------------+-----------------+
|            key             |        created_at        |        updated_at        | visibility |  tenant_name   | created_by | is_hidden_value |
+----------------------------+--------------------------+--------------------------+------------+----------------+------------+-----------------+
|       my_key_private       | 2020-05-27 07:21:55.629  | 2020-05-27 07:21:55.629  |   tenant   | default_tenant |   admin    |      False      |
|       my_key_public        | 2020-05-27 07:21:55.686  | 2020-05-27 07:21:55.686  |   tenant   | default_tenant |   admin    |      False      |
+----------------------------+--------------------------+--------------------------+------------+----------------+------------+-----------------+

```

2. Install the example:

```shell
$ cfy install create_secret_agent_key_using_exising_secret.yaml -i agent_key_name=my_key -b example2
...
$ cfy secrets list
Listing all secrets...

Secrets:
+----------------------------+--------------------------+--------------------------+------------+----------------+------------+-----------------+
|            key             |        created_at        |        updated_at        | visibility |  tenant_name   | created_by | is_hidden_value |
+----------------------------+--------------------------+--------------------------+------------+----------------+------------+-----------------+
|       my_key_private       | 2020-05-27 07:21:55.629  | 2020-05-27 07:21:55.629  |   tenant   | default_tenant |   admin    |      False      |
|       my_key_public        | 2020-05-27 07:21:55.686  | 2020-05-27 07:21:55.686  |   tenant   | default_tenant |   admin    |      False      |
+----------------------------+--------------------------+--------------------------+------------+----------------+------------+-----------------+

```
Notice that our second example node uses the secrets that exists in the manager(See public_key_export runtime property).

3. Uninstall the example:
```shell
$ cfy uninstall example2
```

Notice the secrets were Not deleted!

3. Uninstall the first example:

```shell
$ cfy uninstall cloudify-ssh-key
```
Notice the secrets deleted.


## example 3  

blueprint: create-key-and-store-in-path.yaml

This example demonstrates generating ssh keys(private and public) and store them in a given path.


1. Install the example:

```shell
$ cfy install  create-key-and-store-in-path.yaml -i private_key_path=<path> -i public_key_path=<path>

```
Check the key files exist in the paths.


**Note**:

For more use cases, see [virtual-machine examples](https://github.com/cloudify-community/blueprint-examples/tree/master/virtual-machine).
