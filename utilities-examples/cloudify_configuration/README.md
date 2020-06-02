# Cloudify Utilities: Configuration

## Configuration plugin manual for VCPE solution

For more information on configuration plugin read the [documentation](https://github.com/cloudify-incubator/cloudify-utilities-plugin/tree/master/cloudify_configuration).

**Example:**

[Simple example](./simple.yaml)

# Provided workflow

## configuration_update

Workflow for update all nodes with types from `node_types_to_update` by values from `configuration_node_id`. Executes cloudify.interfaces.lifecycle.is_alive workflow **only on relevant nodes**, configure operation on the configuration_loader node provided in configuration_node_id paramter, preconfigure operation on every connected node to configuration_loader and finally cloudify.interfaces.lifecycle.update.


**Parameters:**
* `params`: list of parameters.
* `configuration_node_id`: type of configuration node, by default: `configuration_loader`.
* `node_types_to_update`: list of node types for update in workflow, by default: `juniper_node_config`, `fortinet_vnf_type`.
* `merge_dict`: boolean parameter

## cloudify.interfaces.lifecycle.is_alive

Interface needs to implement operations needed to check if node that we want to configure is accessable to get updated. Unavailability can be handled in a few ways - performing operations that get back node to operability or raising NonRecoverableError that will stop execution of the workflow.  

## cloudify.interfaces.lifecycle.update

Interface implementing operation executing on the configuration update.