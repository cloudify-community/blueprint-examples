# Network Service

This blueprint installs a service chain by creating forwarding rules on the VNFs (Fortigate and BIG IP).

## Prerequisites:

First make sure that you have satisfied the global requirements in the [main README](../README.md) as well as installed the following deployments:

  * *BIG IP Provisioning & Configuration*: See [instructions](../bigip/README.md).
  * *Fortigate Provisioning & Configuration*: See [instructions](../fortigate/README.md).
  * *webserver Provisioning & Configuration*: See [instructions](../webserver/README.md).

## Service creation

IP addresses are fetched using `get_capability` function.

* Blueprint: The `service.yaml` blueprint is responsible for orchestrating the service chaining. It consists of two nodes:
  * `fg_port_forwarding`: Prepares NAT rules and policies, which are required to perform the service chain. [fortigate-portforward-start.txt](Resources/templates/fortigate-portforward-start.txt) file is used to apply configuration during installation and [fortigate-portforward-stop.txt](Resources/templates/fortigate-portforward-stop.txt) to delete it during uninstall.
  * `ltm_config`: Creates load balancing rule responsible for passing traffic from app (exposed on WAN fortigate interface) to BIG-IP Public interface using [ltm_config.txt](Resources/templates/azure/ltm_config.txt) file on Azure and [ltm_config.txt](Resources/templates/openstack/ltm_config.txt) file on Openstack to apply configuration and [ltm_config_stop.txt](Resources/templates/azure/ltm_config_stop.txt) file on Azure and [ltm_config_stop.txt](Resources/templates/openstack/ltm_config_stop.txt) file on Openstack to delete it during uninstall.

* Inputs:
  * `f5_prov_deployment_name`: The name of the BIG IP Provisioning deployment, used to get management and Public IPs from BIG IP VE. Default: `VNFM-F5-Prov-Azure-vm`.
  * `fg_prov_deployment_name`: The name of the Fortigate Provisioning deployment, used to get management and WAN IPs from Fortigate VM. Default: `VNFM-Fortigate-Prov-Azure-vm`.
  * `webserver_prov_deployment_name`: The name of the webserver Provisioning deployment, used to fetch webserver LAN interface IP. Default: `VNFM-webserver-Prov-Azure-vm`.
  * `lb_public_port`: Load balancer public network port on which the service is exposed. Default: `8080`.
  * `wan_port`: Fortigate WAN port on which the service is going to be exposed. Default: `8080'`.

### Install

To apply service configuration execute:

AZURE:
``cfy install azure_service.yaml -b NS-LB-Firewall-F5-Fortigate-webserver``

OPENSTACK:
``cfy install openstack_service.yaml -b NS-LB-Firewall-F5-Fortigate-webserver``

### Service validation

After service creation You should be able to display web server exposed on Public interface of BIG-IP. The URL is available on *web_server* deployment output.

### Uninstall

To tear down service configuration execute:

``cfy uninstall NS-LB-Firewall-F5-Fortigate-HTTP``
