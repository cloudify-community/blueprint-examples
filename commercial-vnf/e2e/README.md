# End-to-End Network Service - Commercial VNFs

This Blueprint describes the entire network service, by embedding all sub-blueprints describing the different components, and executing the provisioning, configurations, and chaining steps in the proper order.

For more information about particular steps, please go to the [main README](../README.md).

## Prerequisites:

Prior to installation please upload the below plugins and create the mentioned secrets.

### Plugins

Upload:
* **cloudify-azure-plugin** - Tested for version 2.1.1
* **cloudify-openstack-plugin** - Tested for version 2.14.7
* **cloudify-utilities-plugin** - Tested for version 1.12.5

This can be applied through the Cloudify manager user interface or using the CLI.
* To upload plugins using the Cloudify manager:
    * Browse to the *Cloudify Catalog* page and scroll to the *Plugins Catalog* widget. Select the relevant plugins and click *Upload*.
* To upload plugins using the CLI, run the following commands:
``cfy plugins upload https://github.com/cloudify-incubator/cloudify-utilities-plugin/releases/download/1.12.5/cloudify_utilities_plugin-1.12.5-py27-none-linux_x86_64-centos-Core.wgn -y https://github.com/cloudify-incubator/cloudify-utilities-plugin/releases/download/1.12.5/plugin.yaml``

``cfy plugins upload https://github.com/cloudify-cosmo/cloudify-openstack-plugin/releases/download/2.14.7/cloudify_openstack_plugin-2.14.7-py27-none-linux_x86_64-centos-Core.wgn -y https://github.com/cloudify-cosmo/cloudify-openstack-plugin/releases/download/2.14.7/plugin.yaml``

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
    * *keystone_username* - Keystone username
    * *keystone_password* - Keystone password
    * *keystone_tenant_name* - Keystone tenant name
    * *keystone_url* - Keystone URL
    * *keystone_region* - Keystone region
* **Common secrets:**
    * *bigip_username* - Username for BIG IP VE. Relevant only for Azure - Openstack uses default credentials (uname: root, pwd: default). It is set during provisioning and used during configuration, "admin" is not allowed. You can set this up via the CLI: `cfy secrets create bigip_username -s [secret value]`.
    * *bigip_password* - Password for BIG IP VE. Relevant only for Azure - Openstack uses default credentials (uname: root, pwd: default). It is set during provisioning and used during configuration. The supplied password must be between 6-72 characters long and must satisfy at least 3 of password complexity requirements from the following: Contains an uppercase character, Contains a lowercase character, Contains a numeric digit, Contains a special character. Control characters are not allowed. . You can set this up via the CLI: `cfy secrets create bigip_password -s [secret value]`.
    * *bigip_license* - License key for BIG IP VE, it is being applied during configuration
    * *fortigate_username* - Username for Fortigate VM. It is set during provisioning and used during configuration, "admin" is not allowed. You can set this up via the CLI: `cfy secrets create fortigate_username -s [secret value]`. For OpenStack, it has to be set on default username: `admin`.
    * *fortigate_password* - Password for Fortigate VM. It is set during provisioning and used during configuration. The supplied password must be between 6-72 characters long and must satisfy at least 3 of password complexity requirements from the following: Contains an uppercase character, Contains a lowercase character, Contains a numeric digit, Contains a special character. Control characters are not allowed. . You can set this up via the CLI: `cfy secrets create fortigate_password -s [secret value]`. For OpenStack, it has to be set on empty password: ``.
    * *fortigate_license* - Content of license file, its used during provisioning to license Fortigate
    * *httpd_username* - Username for HTTPD VM. It is set during provisioning and used during configuration, "admin" is not allowed. `ubuntu` is recommended. You can set this up via the CLI: `cfy secrets create httpd_username -s [secret value]`.
    * *httpd_website* - Content of website file for HTTPD VM, it is set during provisioning and served after configuration

You can create those with the following cfy commands:\
``cfy secrets create azure_client_id -s <azure_client_id>``\
``cfy secrets create azure_client_secret -s <azure_client_secret>``\
``cfy secrets create azure_subscription_id -s <azure_subscription_id>``\
``cfy secrets create azure_tenant_id -s <azure_tenant_id>``\
``cfy secrets create azure_location -s <azure_location>``\
``cfy secrets create keystone_username -s <keystone_username>``\
``cfy secrets create keystone_password -s <keystone_password>``\
``cfy secrets create keystone_tenant_name -s <keystone_tenant_name>``\
``cfy secrets create keystone_url -s <keystone_url>``\
``cfy secrets create keystone_region -s <keystone_region>``\
``cfy secrets create bigip_username -s <bigip_username>``\
``cfy secrets create bigip_password -s <bigip_password>``\
``cfy secrets create bigip_license -s <bigip_license>``\
``cfy secrets create fortigate_username -s <fortigate_username>``\
``cfy secrets create fortigate_password -s <fortigate_password>``\
``cfy secrets create fortigate_license -f <path to a fortigate license>``\
``cfy secrets create httpd_username -s <httpd_username>``\
``cfy secrets create httpd_website -s <httpd_website>``

### Inputs

* *network_prov_name* - The name of the common network resources provisioning deployment - default: VNFM-Networking-Prov-Azure-networks
* *f5_prov_name* - The name of the BIG IP Provisioning deployment - default: VNFM-F5-Prov-Azure-vm
* *f5_conf_name* - The name of the BIG IP Configuration deployment - default: VNFM-F5-Conf
* *fg_prov_name* - The name of the Fortigate Provisioning deployment - default: VNFM-Fortigate-Prov-Azure-vm
* *fg_conf_name* - The name of the Fortigate Configuration deployment - default: VNFM-Fortigate-Conf
* *httpd_prov_name* - The name of the HTTPD Provisioning deployment - default: VNFM-HTTPD-Prov-Azure-vm
* *httpd_conf_name* - The name of the HTTPD Configuration deployment - default: VNFM-HTTPD-Conf
* *service_prov_name* - The name of the service provisioning deployment - default: NS-LB-Firewall-F5-Fortigate-HTTPD


### Installation

To apply the service configuration execute:

AZURE:
``cfy install azure_e2e.yaml -b VNFM-E2E-F5-Fortigate-HTTPD``

OPENSTACK:
``cfy install openstack_e2e.yaml -b VNFM-E2E-F5-Fortigate-HTTPD``

### Service validation

Once all steps had been performed, you should be able to access the web page displayed by the web service by accessing the ip of the load balancer (This IP will be the output of the service deployment flow, and will be titled *web_server*).

### Uninstalling

To tear down the service configuration execute:

``cfy uninstall VNFM-E2E-F5-Fortigate-HTTPD``
