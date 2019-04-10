# HTTPD Webserver

This blueprint installs HTTPD webserver on an Azure VM.

### Prerequisites

First make sure that you have satisfied the global requirements in the [main README](../README.md).

* These additional secrets should exist on your manager:
  * `httpd_username`: Username for HTTPD VM. It is set during provisioning and used during configuration, "admin" is not allowed. `ubuntu` is recommended. You can set this up via the CLI: `cfy secrets create httpd_username -s [secret value]`.
  * `httpd_website`: Content of website file for HTTPD VM, it is set during provisioning and served after configuration. Exemplary website can be found under `Resources/website/index.html`.

## Provisioning

* Blueprint: The `azure.yaml` blueprint is responsible for the creation of an Ubuntu VM. It is connected to 2 networks:
  * Management
  * LAN

The networks' NICs are connected to the security group created in the network deployment. The networks and security group names are fetched from network deployment using `get_capability` intrinsic function.

* Inputs:
  * `image`: Image information. Default: `{'publisher': 'Canonical', 'offer': 'UbuntuServer', 'sku': '18.04-LTS', 'version': 'latest}'`.
  * `network_deployment_name`: Name of deployment responsible for creation resource group, security group and networks. Default: `VNFM-Networking-Prov-Azure-networks`.

### Installation

Upload the blueprint, create the deployment and execute install workflow in one command using the CLI:

```bash
cfy install  azure.yaml -b  \
    VNFM-HTTPD-Prov-Azure-vm
```

### Uninstalling

Uninstall the deployment:

```
cfy uninstall VNFM-HTTPD-Prov-Azure-vm
```

## Configuration

* Blueprint: The `azureapp.yaml` blueprint is responsible for starting HTTPD process on the target VM, `web_server` node is responsible for creating such server using the following command: `screen -dmS -X python3 -m http.server 8080`. The IP address of the target VM is fetched from VNFM-HTTPD-Prov-Azure-vm deployment using capabilities.

* Inputs:
  * `httpd_vm_deployment_name`: Name of HTTPD Provisioning deployment. Default: `VNFM-HTTPD-Prov-Azure-vm`.

### Install

`cfy install azureapp.yaml -b VNFM-HTTPD-Conf`

### Uninstall

`cfy uninstall VNFM-HTTPD-Conf`
