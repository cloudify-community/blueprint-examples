
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
  * Cloudify 4.5.5


## Pre-installation steps

Upload the required plugins:

  * [Openstack Plugin](https://github.com/cloudify-cosmo/cloudify-openstack-plugin/releases).

_Check the blueprint for the exact version of the plugin._


If you do not provide your own `deployment inputs` below, you must add these secrets to your Cloudify Manager `tenant`:

  * `username`
  * `password`
  * `tenant_name`
  * `url`
  * `region`, such as `RegionOne`.


Find the name of your Openstack Floating IP Network. You will need this value for the `external_network_name` input when you create your deployment.
