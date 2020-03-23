# BIG-IP Load Balancer

This blueprint installs the BIG-IP load balancer on chosen infrastructure: Azure or OpenStack.

### Prerequisites

First make sure that you have satisfied the global requirements in the [main README](../README.md).

* These additional secrets should exist on your manager:
  * `bigip_username`: Username for BIG IP VE. Relevant only for Azure - Openstack uses default credentials (uname: root, pwd: default). It is set during provisioning and used during configuration, "admin" is not allowed. You can set this up via the CLI: `cfy secrets create bigip_username -s [secret value]`.
  * `bigip_password`: Password for BIG IP VE. Relevant only for Azure - Openstack uses default credentials (uname: root, pwd: default). It is set during provisioning and used during configuration. The supplied password must be between 6-72 characters long and must satisfy at least 3 of password complexity requirements from the following: Contains an uppercase character, Contains a lowercase character, Contains a numeric digit, Contains a special character. Control characters are not allowed. . You can set this up via the CLI: `cfy secrets create bigip_password -s [secret value]`.
  * `bigip_license`: License key for BIG IP VE. It is being applied during configuration. . You can set this up via the CLI: `cfy secrets create bigip_license -s [secret value]`.

## Provisioning

* Blueprint: The `azure.yaml` and `openstack.yaml` blueprints are responsible for creation BIG-IP Virtual Machine. This VM is connected to 3 networks:
  * Management
  * WAN
  * Public

Network's NICs are connected to security group created in network deployment.
Networks and security group names are fetched from network deployment using `get_capability` intrinsic function.

* Azure inputs:
  * `virtual_machine_size`: Name of Virtual Machine Size in Azure. Default: `Standard_A7`.
  * `virtual_machine_image_sku`:  An instance of an offer, such as a major release of a distribution. Default: `f5-big-all-1slot-byol`.
  * `virtual_machine_image_publisher`:  Name of the organization that created the image. Default: `f5-networks`.
  * `virtual_machine_image_offer`:  The name of a group of related images created by a publisher. Default: `f5-big-ip-byol`.
  * `azure_network_deployment_name`: Name of deployment responsible for creation resource group, security group and networks. Default: `VNFM-Networking-Prov-Azure-networks`.

* Openstack inputs:
  * *flavor_id* - ID of the flavor in OpenStack - default: `f7cfaaa8-e2db-4f9b-a65b-6a407f340960`
  * *vnf_vm_name* - Name of Virtual Machine - default: `bigip`
  * *image_id* - ID of the image in OpenStack - default: `6d8ff903-f35b-43df-b7c2-e219929924b9`
  * *openstack_network_deployment_name* - Name of the deployment responsible for router, security group and networks creation -
      default: `VNFM-Networking-Prov-Openstack-networks`.

### Install

Upload the blueprint, create the deployment and execute install workflow in one command using the CLI:

AZURE:
```bash
cfy install  azure.yaml -b  \
    VNFM-F5-Prov-Azure-vm
```

OPENSTACK:
```bash
cfy install  openstack.yaml -b  \
    VNFM-F5-Prov-Openstack-vm
```

### Uninstall

Uninstall the **VNFM-F5-Prov-Azure-vm** deployment:

AZURE:
```
cfy uninstall VNFM-F5-Prov-Azure-vm
```

OPENSTACK:
```
cfy uninstall VNFM-F5-Prov-Openstack-vm
```

## Configuration

The configuration requires the IP addresses of the VM created during provisioning, therefore the provisioning deployment name is required as an input. Exposed IP addresses are fetched using `get_capability` function: `{ get_capability: [ {get_input: prov_deployment_name}, wan_ip ] }`.

* Blueprint: The `<infrastructure>app.yaml` blueprint is responsible for licensing BIG IP with the provided registration key and applying VLAN configuration necessary for further LTM configuration. It consists of two nodes (+ one extra node in OpenStack deployment):
  * `check_mcpd_status`: (ONLY OPENSTACK) Checks if the MCPD services is already started, because it's necessary for applying the license succesfully.
    Uses [check_mcpd_status.txt](Resources/templates/openstack/check_mcpd_status.txt) file.
  * `license`: Applies license using [install_license.txt](Resources/templates/azure/install_license.txt) file for Azure and [install_license.txt](Resources/templates/openstack/install_license.txt) file for Openstack and revokes it using [revoke_license.txt](Resources/templates/azure/revoke_license.txt) for Azure and [revoke_license.txt](Resources/templates/openstack/revoke_license.txt) for Openstack.
  * `vlan_configuration`: Creates VLAN configuration on WAN and Public interfaces - using [vlan_config.txt](Resources/templates/azure/vlan_config.txt) for Azure and [vlan_config.txt](Resources/templates/openstack/vlan_config.txt) for Openstack, to apply it during install and [vlan_config_delete.txt](Resources/templates/azure/vlan_config_delete.txt) for Azure and [vlan_config_delete.txt](Resources/templates/openstack/vlan_config_delete.txt) for Openstack to tear it down during uninstall.

* Inputs:
  * `prov_deployment_name`: Name of BIG IP Provisioning deployment created in previous section. Default: `VNFM-F5-Prov-Azure-vm` or `VNFM-F5-Prov-Openstack-vm`.


### Install

AZURE:
`cfy install azureapp.yaml -b VNFM-F5-Conf`

OPENSTACK:
`cfy install openstackapp.yaml -b VNFM-F5-Conf`

### Uninstall

During uninstall the license is revoked so it can be used on different BIG IP VE or on the same one again. Also VLAN configuration is deleted.

`cfy uninstall VNFM-F5-Conf`
