# Commercial VNF Use Case

Upon completion of this example we will have a complete running network service.

![ns](https://user-images.githubusercontent.com/30900001/52050834-12889e00-2552-11e9-9a68-452e92cc7014.png)

This series of blueprints demonstrates how to install a simple network service consisting of a load balancer and a firewall. To make it a tad more interesting we will be deploying a simple web service to allow for complete user experience. All of the examples are currently implemented only for Azure and OpenStack.

**Note!**
The infrastructures used in this example are Microsoft Azure or OpenStack, and the demonstrated VNFs are:
  * F5 BIG-IP VE (Load balancer)
  * Fortigate (Firewall)
  * Httpd (Web Server)

## Common Prerequisites:

* Cloudify Manager 4.5.5, for more info: [Cloudify-Getting-Started](https://cloudify.co/download/).

* These plugins should exist on your manager. (E.g. You can just run `cfy plugins bundle-upload`, which will satisfy all plugin requirements.):
  * [cloudify-azure-plugin](https://github.com/cloudify-cosmo/cloudify-openstack-plugin/releases), version 2.1.1 or higher.
  * [cloudify-openstack-plugin](https://github.com/cloudify-cosmo/cloudify-openstack-plugin/releases), version 2.14.7 or higher.
  * [cloudify-utilities-plugin](https://github.com/cloudify-incubator/cloudify-utilities-plugin/releases), version 1.12.5 or higher.

* These secrets should exist on your manager:
  * **FOR AZURE:**
    * `azure_client_id`: Service Principal appId. You can set this up via the CLI: `cfy secrets create azure_client_id -s [secret value]`.
    * `azure_client_secret`: Service Principal password. You can set this up via the CLI: `cfy secrets create azure_client_secret -s [secret value]`.
    * `azure_subscription_id`: Service Principal ID. You can set this up via the CLI: `cfy secrets create azure_subscription_id -s [secret value]`.
    * `azure_tenant_id`: Service Principal tenant. You can set this up via the CLI: `cfy secrets create azure_tenant_id -s [secret value]`.
    * `azure_location`: Specifies the supported Azure location for the resource. You can set this up via the CLI: `cfy secrets create azure_location -s [secret value]`.
    * `agent_key_private`: The content of an RSA private key. (E.g. You can upload this key from a file: `cfy secrets create agent_key_private -f ~/.ssh/id_rsa`).
    * `agent_key_public`: The content of an RSA public key. (E.g. You can upload this key from a file: `cfy secrets create agent_key_private -f ~/.ssh/id_rsa.pub`).
  * **FOR OPENSTACK:**:
    * *keystone_username* - Username used for authentication in Keystone service. You can set this up via the CLI: ``cfy secrets create keystone_username -s <keystone_username>``
    * *keystone_password* - Password used for authentication in Keystone service. You can set this up via the CLI: ``cfy secrets create keystone_password -s <keystone_password>``
    * *keystone_tenant_name* - Name of the tenant in OpenStack. You can set this up via the CLI: ``cfy secrets create keystone_tenant_name -s <keystone_tenant_name>``
    * *keystone_url* - URL used for authentication in Keystone service. You can set this up via the CLI: ``cfy secrets create keystone_url -s <keystone_url>``
    * *keystone_region* - Name of the region in OpenStack. You can set this up via the CLI: ``cfy secrets create keystone_region -s <keystone_region>``


## Installation

The installation is broken into a few basic steps. Go to the relevant README and progress through these steps in the correct order.

1. [Prepare the environment](network-topology/README.md##Installation): Create networks, a resource group, and a security group.
1. Provisioning of the VNFs:
  1. [Provision the load balancer](bigip/README.md##Provisioning) and setup basic settings.
  1. [Provision the firewall](fortigate/README.md##Provisioning) and configure its network interfaces and the network settings.
  1. [Provision the web server](httpd/README.md##Provisioning) instance, configure it, and setup basic web content.
1. Compose the service flow by:
  1. [Configuration the load balancer](bigip/README.md##Configuration) and setup basic settings.
  1. [Configuration the firewall](fortigate/README.md##Configuration) and configure its network interfaces and the network settings.
  1. [Configuration the web server](httpd/README.md##Configuration) instance, configure it, and setup basic web content.
1. [Create service](service/README.md) The last step creates a service chain of connected network services (Load Balancer, Firewall and Web Server). In this case service chaining consists of port forwarding rule on Fortigate and load balancing rule on BIG IP in order to pass traffic through.
