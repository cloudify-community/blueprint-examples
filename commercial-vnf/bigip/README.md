# BIG-IP Load Balancer

This blueprint installs the BIG-IP load balancer on Azure.

### Prerequisites

First make sure that you have satisfied the global requirements in the [main README](../README.md).

* These additional secrets should exist on your manager:
  * `bigip_username`: Username for BIG IP VE. It is set during provisioning and used during configuration, "admin" is not allowed. You can set this up via the CLI: `cfy secrets create bigip_username -s [secret value]`.
  * `bigip_password`: Password for BIG IP VE. It is set during provisioning and used during configuration. The supplied password must be between 6-72 characters long and must satisfy at least 3 of password complexity requirements from the following: Contains an uppercase character, Contains a lowercase character, Contains a numeric digit, Contains a special character. Control characters are not allowed. . You can set this up via the CLI: `cfy secrets create bigip_password -s [secret value]`.
  * `bigip_license`: License key for BIG IP VE. It is being applied during configuration. . You can set this up via the CLI: `cfy secrets create bigip_license -s [secret value]`.

## Provisioning

* Blueprint: The `infrastructure.yaml` blueprint is responsible for creation BIG-IP Virtual Machine. This VM is connected to 3 networks:
  * Management
  * WAN
  * Public

Network's NICs are connected to security group created in network deployment.
Networks and security group names are fetched from network deployment using `get_capability` intrinsic function.

* Inputs:
  * `virtual_machine_size`: Name of Virtual Machine Size in Azure. Default: `Standard_A7`.
  * `virtual_machine_image_sku`:  An instance of an offer, such as a major release of a distribution. Default: `f5-big-all-1slot-byol`.
  * `virtual_machine_image_publisher`:  Name of the organization that created the image. Default: `f5-networks`.
  * `virtual_machine_image_offer`:  The name of a group of related images created by a publisher. Default: `f5-big-ip-byol`.
  * `azure_network_deployment_name`: Name of deployment responsible for creation resource group, security group and networks. Default: `VNFM-Networking-Prov-Azure-networks`.

### Installation

Upload the blueprint, create the deployment and execute install workflow in one command using the CLI:

```bash
cfy install  infrastructure.yaml -b  \
    VNFM-F5-Prov-Azure-vm
```

###Uninstalling

Uninstall the **VNFM-F5-Prov-Azure-vm** deployment:

```
cfy uninstall VNFM-F5-Prov-Azure-vm
```

## Configuration

The configuration requires the IP addresses of the VM created during provisioning, therefore the provisioning deployment name is required as an input. Exposed IP addresses are fetched using `get_capability` function: `{ get_capability: [ {get_input: prov_deployment_name}, wan_ip ] }`.

* Blueprint: The `application.yaml` blueprint is responsible for licensing BIG IP with the provided registration key and applying VLAN configuration necessary for further LTM configuration. It consists of two nodes:
  * `license`: Applies license using [install_license.txt](Resources/templates/install_license.txt) file and revokes it using [revoke_license.txt](Resources/templates/revoke_license.txt).
  * `vlan_configuration`: Creates VLAN configuration on WAN and Public interfaces - using [vlan_config.txt](Resources/templates/vlan_config.txt) to apply it during install and [vlan_config_delete.txt](Resources/templates/vlan_config_delete.txt) to tear it down during uninstall.

* Inputs:
  * `prov_deployment_name`: Name of BIG IP Provisioning deployment created in previous section. Default: `VNFM-F5-Prov-Azure-vm`.


### Install

`cfy install application.yaml -b VNFM-F5-Conf`

### Uninstall

During uninstall the license is revoked so it can be used on different BIG IP VE or on the same one again. Also VLAN configuration is deleted.

`cfy uninstall VNFM-F5-Conf`
