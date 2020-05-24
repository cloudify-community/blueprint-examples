
# Openstack Example Network

### Resources Created

  * A `external_network`.
  * A `public_network`.
  * A `private_network`.
  * A `public_network_router`.
  * A `public_subnet`.
  * A `private_subnet`.


## Compatibility

Tested with:
  * Cloudify 5.0.5


## Pre-installation steps

Upload the required plugins:

  * [Openstack Plugin](https://github.com/cloudify-cosmo/cloudify-openstack-plugin/releases).

_Check the blueprint for the exact version of the plugin._


If you do not provide your own `deployment inputs` below, you must add these secrets to your Cloudify Manager `tenant`:

  * `openstack_username`
  * `openstack_password`
  * `openstack_tenant_name`
  * `openstack_auth_url` - v3 authentication url. 
  * `openstack_region`, such as `RegionOne`.

Find the name of your Openstack Floating IP Network. You will need this value for the `external_network_name` input when you create your deployment.

In case that project_domain_name, project_domain_name is not "default" please provide them as inputs.

**Note:** if you are using v2 authentication url remove user_domain_name and project_domain_name
from client_config_dict. 

**Example**:
`cfy install blueprint.yaml -i external_network_id=ext-net -i user_domain_name=<value> -i project_domain_name=<value>`