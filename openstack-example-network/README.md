
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
  * Cloudify 4.2


## Pre-installation steps

Upload the required plugins:

  * [Openstack Plugin](https://github.com/cloudify-cosmo/cloudify-openstack-plugin/releases).

_Check the blueprint for the exact version of the plugin._


If you do not provide your own `deployment inputs` below, you must add these secrets to your Cloudify Manager `tenant`:

  * `keystone_username`
  * `keystone_password`
  * `keystone_tenant_name`
  * `keystone_url`
  * `region`, such as `RegionOne`.


Find the name of your Openstack Floating IP Network. You will need this value for the `external_network_name` input when you create your deployment.

## Installation

On your Cloudify Manager, navigate to `Local Blueprints` select `Upload`.

[Right-click and copy URL](https://github.com/cloudify-examples/openstack-example-network/archive/master.zip). Paste where it says `Enter blueprint url`. Provide a blueprint name, such as `examples-network` in the field labeled `blueprint name`. Select `simple-blueprint.yaml` from `Blueprint filename` menu.

After the new blueprint has been created, click the `Deploy` button.

Navigate to `Deployments`, find your new deployment, select `Install` from the `workflow`'s menu. At this stage, you may provide your own values for any of the default `deployment inputs`.


## Uninstallation

Navigate to the deployment and select `Uninstall`. When the uninstall workflow is finished, select `Delete deployment`.
