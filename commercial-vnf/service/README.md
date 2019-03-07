# Network Service

This blueprint installs a service chain by creating forwarding rules on the VNFs (Fortigate and BIG IP).

## Prerequisites:

First make sure that you have satisfied the global requirements in the [main README](../README.md) as well as installed the following deployments:

  * *BIG IP Provisioning & Configuration*: See [instructions](../bigip/README.md).
  * *Fortigate Provisioning & Configuration*: See [instructions](../fortigate/README.md).
  * *HTTPD Provisioning & Configuration*: See [instructions](../httpd/README.md).

## Service creation

IP addresses are fetched using `get_capability` function.

* Blueprint: The `service.yaml` blueprint is responsible for orchestrating the service chaining. It consists of two nodes:
  * `fg_port_forwarding`: Prepares NAT rules and policies, which are required to perform the service chain. [fortigate-portforward-start.txt](Resources/templates/fortigate-portforward-start.txt) file is used to apply configuration during installation and [fortigate-portforward-stop.txt](Resources/templates/fortigate-portforward-stop.txt) to delete it during uninstall.
  * `ltm_config`: Creates load balancing rule responsible for passing traffic from app (exposed on WAN fortigate interface) to BIG-IP Public interface using [ltm_config.txt](Resources/templates/ltm_config.txt) file to apply configuration and [ltm_config_stop.txt](Resources/templates/ltm_config_stop.txt) to delete it during uninstall.

* Inputs:
  * `f5_prov_deployment_name`: The name of the BIG IP Provisioning deployment, used to get management and Public IPs from BIG IP VE. Default: `VNFM-F5-Prov-Azure-vm`.
  * `fg_prov_deployment_name`: The name of the Fortigate Provisioning deployment, used to get management and WAN IPs from Fortigate VM. Default: `VNFM-Fortigate-Conf`.
  * `httpd_prov_deployment_name`: The name of the HTTPD Provisioning deployment, used to fetch HTTPD LAN interface IP. Default: `VNFM-HTTPD-Prov-Azure-vm`.
  * `lb_public_port`: Load balancer public network port on which the service is exposed. Default: `8080`.
  * `wan_port`: Fortigate WAN port on which the service is going to be exposed. Default: `8080'`.

### Installation

To apply service configuration execute:

``cfy install service.yaml -b NS-LB-Firewall-F5-Fortigate-HTTPD``

### Service validation

After service creation You should be able to display web server exposed on Public interface of BIG-IP. The URL is available on *web_server* deployment output.

### Uninstalling

To tear down service configuration execute:

``cfy uninstall NS-LB-Firewall-F5-Fortigate-HTTP``
