# FortiGate Firewall

This blueprint installs the NGFW Single VM on Azure or Openstack.

### Prerequisites

First make sure that you have satisfied the global requirements in the [main README](../README.md).

* These additional secrets should exist on your manager:
  * `fortigate_username`: Username for Fortigate VM. It is set during provisioning and used during configuration, "admin" is not allowed. You can set this up via the CLI: `cfy secrets create fortigate_username -s [secret value]`. For OpenStack, it has to be set on default username: `admin`.
  * `fortigate_password`: Password for Fortigate VM. It is set during provisioning and used during configuration. The supplied password must be between 6-72 characters long and must satisfy at least 3 of password complexity requirements from the following: Contains an uppercase character, Contains a lowercase character, Contains a numeric digit, Contains a special character. Control characters are not allowed. . You can set this up via the CLI: `cfy secrets create fortigate_password -s [secret value]`. For OpenStack, it has to be set on empty password: ` `.
  * `fortigate_license`: Content of license file, its used during provisioning to license Fortigate. You can set this up via the CLI: `cfy secrets create fortigate_license -s [secret value]`.

## Provisioning

* Blueprint: The `azure.yaml` and `openstack.yaml` blueprints are for FortiGate NGFW Single VM provisioning. This VM is connected to 3 networks:
  * Management
  * WAN
  * LAN

The networks' NICs are connected to the security group created in the network deployment. The networks and security group names are fetched from network deployment using `get_capability` intrinsic function.

* Azure inputs:
  * `fortigate_license_filename`: This is the name of the Fortigate license file. It will be uploaded to Fortigate VM with this name. It should have .lic file extension. Default: `FGVM02TM19000054.lic`.
  * `vm_size`: Name of Virtual Machine Size in Azure. Default: `Standard_B2s`.
  * `vm_os_family`: Default: `linux`.
  * `vm_image_publisher`: Name of the organization that created the image. Default: `fortinet`.
  * `vm_image_offer`: The name of a group of related images created by a publisher. Default: `fortinet_fortigate-vm_v5`
  * `vm_image_sku`: An instance of an offer, such as a major release of a distribution. Default: `fortinet_fg-vm`
  * `vm_image_version`: Version of the image. Default: `6.0.3`.
  * `azure_network_deployment_name`: Name of deployment responsible for creation resource group, security group and networks. Default: `VNFM-Networking-Prov-Azure-networks`.
* Openstack inputs:
  * `openstack_network_deployment_name` - Name of deployment responsible for router, security group and networks creation -
      default: `VNFM-Networking-Prov-Openstack-networks`
  * `flavor_id` - ID of the flavor in OpenStack - default: `5aaa5054-f7a4-4bbe-8b47-69da2308ecb2`
  * `image_id` - ID of the image in OpenStack - default: `20acb407-2a20-405e-9e19-360c0a705368`
  * `vnf_vm_name` - Name of VM - default: `fortigate`
  * `fortigate_license_filename` - Name of the Fortigate license file (It will be uploaded to Fortigate VM with this name). It should have .lic file extension. - default: `FGVM02TM19000054.lic`

### Install

Upload the blueprint, create the deployment and execute install workflow in one command using the CLI:

AZURE:
```bash
cfy install  azure.yaml -b  \
    VNFM-Fortigate-Prov-Azure-vm
```

OPENSTACK:
```bash
cfy install  openstack.yaml -b  \
    VNFM-Fortigate-Prov-Openstack-vm
```

### Uninstall

Uninstall the deployment:

AZURE:
```
cfy uninstall VNFM-Fortigate-Prov-Azure-vm
```

OPENSTACK:
```
cfy uninstall VNFM-Fortigate-Prov-Openstack-vm
```

## Configuration

The configuration requires the IP addresses of the VM created during provisioning, therefore the provisioning deployment name is required as an input. Exposed IP addresses are fetched using `get_capability` function: `{ get_capability: [ {get_input: prov_deployment_name}, wan_ip ] }`.

* Blueprint: The `<infrastructure>app.yaml` blueprint is responsible for applying base configuration for the newly created FortiGate VM. It configures all of the interfaces. It consists of one node:
  * `fortigate_vnf_config`: Applies base configuration for Fortigate (VNF name change and basic configuration to interfaces) using [fortigate-baseline.txt](Resources/templates/fortigate-baseline.txt) file.

* Inputs:
  * `fortigate_vm_deployment_name`: Name of Fortigate Provisioning deployment. Default: `VNFM-Fortigate-Prov-Azure-vm` or `VNFM-Fortigate-Prov-Openstack-vm`.

### Install

AZURE:
`cfy install azureapp.yaml -b VNFM-Fortigate-Conf`

OPENSTACK:
`cfy install openstackapp.yaml -b VNFM-Fortigate-Conf`

### Uninstall

`cfy uninstall VNFM-Fortigate-Conf`
