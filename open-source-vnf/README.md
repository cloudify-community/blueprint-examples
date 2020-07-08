# Open-source VNF Use Case

This series of blueprints installs an open-source VNF solution comprised of HTTPD, HAProxy, and a pfSense firewall on an Openstack cloud.

## Summary

Every VNF has a common provisioning step, loading the existing image on to the node. So each VNF inherits from a basic node type, which loads an image from OpenStack. This node type is defined in the 'connected_host' blueprint, so the different VNFs could be placed in different clouds (due to separate namespaced inputs). But that's not an issue, this could be changed to a regular yaml import.

The VNFs network is provisioned in a pre-step to the VNFs creation, so the networks can be constructed and tested out beforehand.

To connect each VNF to it's desired network connectivity, there is a need to connect to the running network deployment, this is achieved by using Component (which can be used by importing cloudify-utilities plugin). With that, the different network specifications can be set across the different VNFs, which is exposed via the Component node in the blueprints (also you can set in that node definition it will create the network if needed and create deployment chaining).

## Prerequisites

* Cloudify Manager 4.5.5

* These plugins should exist on your manager. (E.g. You can just run `cfy plugins bundle-upload`, which will satisfy all plugin requirements.):
  * [cloudify-fabric-plugin](https://github.com/cloudify-cosmo/cloudify-fabric-plugin/releases), version 1.5.1 or higher.
  * [cloudify-openstack-plugin](https://github.com/cloudify-cosmo/cloudify-openstack-plugin/releases), version 2.14.0 or higher.
  * [cloudify-utilities-plugin](https://github.com/cloudify-incubator/cloudify-utilities-plugin/releases), version 1.12.0 or higher.

* These secrets should exist on your manager:
  * `openstack_username`: Your Openstack username.
  * `openstack_password`: Your Openstack password.
  * `openstack_tenant_name`: Your Openstack tenant name.
  * `openstack_auth_url`: The v2.0 or v3 authorization endpoint URL for your Openstack API service.
  * `agent_key_private`: The content of an RSA private key. (E.g. You can upload this key from a file: `cfy secrets create agent_key_private -f ~/.ssh/id_rsa`).
  * `agent_key_public`: The content of an RSA public key. (E.g. You can upload this key from a file: `cfy secrets create agent_key_private -f ~/.ssh/id_rsa.pub`).

* You should also have the following information handy:
  * The ID of an Openstack image that has HAProxy installed on it.
  * The ID of an Openstack image that has httpd installed on it.
  * The ID of an Openstack image that has pfSense installed on it.
  * The ID of an Openstack flavors that satisfy the performance needs of these software components.

* Import the same content as `agent_key_public` to a new Keypair in Openstack named `agent_key_public`.

## Installation

After you have satisfied all of the prerequisites (uploaded plugins, created secrets, gathered inputs), initiate the following steps:

1. Upload to the Cloudify manager all the required blueprints:
    * `connected-host/openstack.yaml` as `connected-host-openstack`.
    * `network-topology/openstack.yaml` as `network-topology-openstack`.
    * `httpd/openstack.yaml` as `httpd-openstack`.
    * `haproxy/openstack.yaml` as `haproxy-openstack`.
    * `pfsense/openstack.yaml` as `pfsense-openstack`.
    * `service/openstack.yaml` as `service-openstack`.

1. Create a deployment with the `service-chaining` blueprint with the relevant inputs.

1. Collect the following details:
    * `host_string` of the HAProxy host.
    * `user` of the HAProxy host, if it is different from the default of `centos`.
    * `rest_endpoint` of the pfSense host.
    * `api_key` of the pfSense host.
    * `api_secret` of the pfSense host.

1. Install the HAProxy service configuration.
    1. Upload `haproxy/application.yaml` as `haproxy-app`.
    1. Create deployment with `haproxy-app` and inputs `host_string` and `user`.

1. Install the pfSense service configuration.
    1. Upload `pfsense/application.yaml` as `pfsense-app`.
    1. Create deployment with `pfsense-app` and inputs `rest_endpoint` and `api_key` and `api_secret`.
