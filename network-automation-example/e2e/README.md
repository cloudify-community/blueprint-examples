# End-to-End Network Service - Commercial VNFs

This Blueprint describes the entire network service, by embedding all sub-blueprints describing the different components, and executing the provisioning, configurations, and chaining steps in the proper order.

For more information about particular steps, please go to the [main README](../README.md).

## Prerequisites:

Prior to installation please upload the below plugins and create the mentioned secrets.

### Plugins

Upload:
* **cloudify-azure-plugin** - Tested for version 2.1.1
* **cloudify-openstack-plugin** - Tested for version 3.0.0
* **cloudify-utilities-plugin** - Tested for version 1.12.5

This can be applied through the Cloudify manager user interface or using the CLI.
* To upload plugins using the Cloudify manager:
    * Browse to the *Cloudify Catalog* page and scroll to the *Plugins Catalog* widget. Select the relevant plugins and click *Upload*.
* To upload plugins using the CLI, run the following commands:
``cfy plugins upload https://github.com/cloudify-incubator/cloudify-utilities-plugin/releases/download/1.12.5/cloudify_utilities_plugin-1.12.5-py27-none-linux_x86_64-centos-Core.wgn -y https://github.com/cloudify-incubator/cloudify-utilities-plugin/releases/download/1.12.5/plugin.yaml``

``cfy plugins upload https://github.com/cloudify-cosmo/cloudify-openstack-plugin/releases/download/3.0.0/cloudify_openstack_plugin-3.0.0-py27-none-linux_x86_64-centos-Core.wgn -y https://github.com/cloudify-cosmo/cloudify-openstack-plugin/releases/download/3.0.0/plugin.yaml``

``cfy plugins upload https://github.com/cloudify-incubator/cloudify-azure-plugin/releases/download/2.1.1/cloudify_azure_plugin-2.1.1-py27-none-linux_x86_64-centos-Core.wgn -y https://github.com/cloudify-incubator/cloudify-azure-plugin/releases/download/2.1.1/plugin.yaml``

### Secrets

Create the below secrets in the secret store management:
* **Azure secrets:**
    * *azure_client_id* - Service Principal appId
    * *azure_client_secret* - Service Principal password
    * *azure_subscription_id* - Service Principal ID
    * *azure_tenant_id* - Service Principal tenant
    * *azure_location* - Specifies the supported Azure location for the resource
* **Openstack secrets:**
    * *openstack_username* - Keystone username
    * *openstack_password* - Keystone password
    * *openstack_tenant_name* - Keystone tenant name
    * *openstack_auth_url* - Keystone URL
    * *openstack_region* - Keystone region
* **Common secrets:**
    * *resource_prefix* - Prefix of every resource created at this deployment. You can set this up via the CLI: `cfy secrets create resource_prefix -s [secret_value]`
    * *resource_suffix* - Suffix of every resource created at this deployment. You can set this up via the CLI: `cfy secrets create resource_suffix -s [secret_value]`
    * *bigip_username* - Username for BIG IP VE. Relevant only for Azure - Openstack uses default credentials (uname: root, pwd: default). It is set during provisioning and used during configuration, "admin" is not allowed. You can set this up via the CLI: `cfy secrets create bigip_username -s [secret value]`.
    * *bigip_password* - Password for BIG IP VE. Relevant only for Azure - Openstack uses default credentials (uname: root, pwd: default). It is set during provisioning and used during configuration. The supplied password must be between 6-72 characters long and must satisfy at least 3 of password complexity requirements from the following: Contains an uppercase character, Contains a lowercase character, Contains a numeric digit, Contains a special character. Control characters are not allowed. . You can set this up via the CLI: `cfy secrets create bigip_password -s [secret value]`.
    * *bigip_license* - License key for BIG IP VE, it is being applied during configuration
    * *fortigate_username* - Username for Fortigate VM. It is set during provisioning and used during configuration, "admin" is not allowed. You can set this up via the CLI: `cfy secrets create fortigate_username -s [secret value]`. For OpenStack, it has to be set on default username: `admin`.
    * *fortigate_password* - Password for Fortigate VM. It is set during provisioning and used during configuration. The supplied password must be between 6-72 characters long and must satisfy at least 3 of password complexity requirements from the following: Contains an uppercase character, Contains a lowercase character, Contains a numeric digit, Contains a special character. Control characters are not allowed. . You can set this up via the CLI: `cfy secrets create fortigate_password -s [secret value]`. For OpenStack, it has to be set on empty password: ` `.
    * *fortigate_license* - Content of license file, its used during provisioning to license Fortigate
    * *webserver_username* - Username for webserver VM. It is set during provisioning and used during configuration, "admin" is not allowed. `ubuntu` is recommended. You can set this up via the CLI: `cfy secrets create webserver_username -s [secret value]`.
    * *webserver_website* - Content of website file for webserver VM, it is set during provisioning and served after configuration

You can create those with the following cfy commands:\
``cfy secrets create azure_client_id -s <azure_client_id>``\
``cfy secrets create azure_client_secret -s <azure_client_secret>``\
``cfy secrets create azure_subscription_id -s <azure_subscription_id>``\
``cfy secrets create azure_tenant_id -s <azure_tenant_id>``\
``cfy secrets create azure_location -s <azure_location>``\
``cfy secrets create _username -s <openstack_username>``\
``cfy secrets create openstack_password -s <openstack_password>``\
``cfy secrets create openstack_tenant_name -s <openstack_tenant_name>``\
``cfy secrets create openstack_auth_url -s <openstack_auth_url>``\
``cfy secrets create openstack_region -s <openstack_region>``\
``cfy secrets create bigip_username -s <bigip_username>``\
``cfy secrets create bigip_password -s <bigip_password>``\
``cfy secrets create bigip_license -s <bigip_license>``\
``cfy secrets create fortigate_username -s <fortigate_username>``\
``cfy secrets create fortigate_password -s <fortigate_password>``\
``cfy secrets create fortigate_license -f <path to a fortigate license>``\
``cfy secrets create webserver_username -s <webserver_username>``\
``cfy secrets create webserver_website -s <webserver_website>``

### Inputs

* *external_network_id* - (ONLY OPENSTACK) The ID of the existing external network
* *network_prov_name* - The name of the common network resources provisioning deployment - default: VNFM-Networking-Prov-Azure-networks
* *f5_prov_name* - The name of the BIG IP Provisioning deployment - default: VNFM-F5-Prov-Azure-vm
* *f5_conf_name* - The name of the BIG IP Configuration deployment - default: VNFM-F5-Conf
* *fg_prov_name* - The name of the Fortigate Provisioning deployment - default: VNFM-Fortigate-Prov-Azure-vm
* *fg_conf_name* - The name of the Fortigate Configuration deployment - default: VNFM-Fortigate-Conf
* *webserver_prov_name* - The name of the webserver Provisioning deployment - default: VNFM-webserver-Prov-Azure-vm
* *webserver_conf_name* - The name of the webserver Configuration deployment - default: VNFM-webserver-Conf
* *service_prov_name* - The name of the service provisioning deployment - default: NS-LB-Firewall-F5-Fortigate-webserver


### Install

To apply the service configuration execute:

AZURE:
``cfy install azuree2e.yaml -b VNFM-E2E-F5-Fortigate-webserver``

OPENSTACK:
``cfy install openstacke2e.yaml -b VNFM-E2E-F5-Fortigate-webserver``

### Service validation

Once all steps had been performed, you should be able to access the web page displayed by the web service by accessing the ip of the load balancer (This IP will be the output of the service deployment flow, and will be titled *web_server*).

### Uninstall

To tear down the service configuration execute:

``cfy uninstall VNFM-E2E-F5-Fortigate-webserver``
