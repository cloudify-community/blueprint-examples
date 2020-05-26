# Cloudify Utilities: Secrets

## Description
Added support for create, read, update and delete operation for complex secrets from the blueprint level.

It is often needed to switch between few DCs during resources provisioning.
For instance we may have to provision the same blueprint as 3 deployment in 3 different data centers with Openstack.
So far we needed to e.g. add prefix or suffix to each of secrets being a parts of *openstack_config*.
To change credentials (data center location) and make new deployment we needed to change secret key prefix / suffix manually in the blueprint (*get_secret* intrinsic function invocations).

*Secrets plugin* can do this automatically - you need only to specify name of DC location.

With *secrets plugin* you can:
* Perform CRUD operation on secrets from the blueprint
* Read / write complex structures (dictionaries) as one secret (JSON serialization)
* Switch dynamically between few variants of the same secret (credentials, data center locations related params etc.) 


For more information about secrets plugin(node types) read the [documentation.](https://github.com/cloudify-incubator/cloudify-utilities-plugin/blob/master/cloudify_secrets/README.md)

## Examples

[Write Example](./write-secret-blueprint.yaml)

[Read Example](./read-secret-blueprint.yaml)

Both examples mentioned show how plugin works:

1) List current secrets:

    ```
    cfy secrets list
    ```
    
2) Install write example blueprint:

    ```
    cfy install write-secret-blueprint.yaml -b write_secrets_test
    ```

3) Check already created secrets:

    ```
    cfy secrets list
    ```

    For each secret execute:
    
    ```
    cfy secrets get <secret name>
    ```

4) Install read example blueprint 

    ```
    cfy install read-secret-blueprint.yaml -b read_secrets_test -vv
    ```

5) Check outputs of read example deployment (should contain some secrets dump)

    ```
    cfy deployments outputs read_secrets_test
    ```
    
6) Uninstall read example deployment

    ```
    cfy uninstall read_secrets_test
    ```
    
7) Uninstall read example deployment

    ```
    cfy uninstall write_secrets_test
    ```
    
8) Check secrets - notice that secrets with *do_not_delete* flag set should still be present

    ```
    cfy secrets list
    ```
    
9) Delete these secrets

    ```
    cfy secrets delete openstack_config__lab1_tenantA
    cfy secrets delete openstack_config__lab1_tenantB    
    cfy secrets delete openstack_config__lab2_tenantA
    ``` 
