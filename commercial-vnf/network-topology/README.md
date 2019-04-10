# Network Topology

This blueprint installs the common infrastructure for the commercial VNF use case.

The following resources will be created:
  * In Azure:
    * `Resource group`: Group that is required to create any other resource in Azure.
    * `Management Network`: This network connects the Cloudify manager to all managed components.
    * `LAN network`: This network connects the firewall to the web server.
    * `WAN network`: This network connects the load balancer to the web server.
    * `Public network`: This is the public network accessible to the user. BIG IP exposes the web server on the Public network interface.
    * `Security group`: Security group for VNF NICs, defined by *network_security_group_rules* input.
  * In Openstack:
    * `Management Network` - This network connects the Cloudify manager to all managed components.
    * `LAN network` - This network connects the firewall to the web server.
    * `WAN network` - This network connects the load balancer to the web server.
    * `Public network` - This is the public network accessible to the user. BIG IP exposes the web server on the Public network interface.
    * `Security group` - Security group for VNF NICs, defined by *network_security_group_rules* input,
    * `Router` - Router, which allows to reach the management and public networks from the external network.

### Install

**Note: Only install this deployment once.** Other blueprints will reuse the existing deployment.

Upload the blueprint, create the deployment and execute install workflow in one command using the CLI:

AZURE:
```bash
cfy install  azure.yaml -b  \
    VNFM-Networking-Prov-Azure-networks
```

OPENSTACK:
```bash
cfy install  openstack.yaml -b  \
    VNFM-Networking-Prov-Openstack-networks
```

### Uninstall

Uninstall the deployment:

AZURE:
```
cfy uninstall VNFM-Networking-Prov-Azure-networks
```

OPENSTACK:
```
cfy uninstall VNFM-Networking-Prov-Openstack-networks
```
