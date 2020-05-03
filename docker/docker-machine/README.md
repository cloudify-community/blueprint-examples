# Cloudify Docker Example

This example blueprint that demonstrates how to install docker on a machine, while separating the infrastructure layer and the application layer.

There are Two components to this blueprint:

  - Infrastructure blueprints (there is a separate blueprint for AWS, Azure, OpenStack and GCP). These blueprints are not directly deployed, rather, the application blueprint leverages infrastructure blueprints to deploy the application on the Cloud of the user's choice. These infrastructure blueprints are available separately under `virtual-machine` example.
  - Docker Application Node

## Requirements

If you have already ensured these requirements are met, skip to [installation steps](#installation-steps).

- [ ] You will need a Cloudify Manager v5.0.5 or higher. See [install Cloudify Manager](#install-cloudify-manager-with-docker).

- [ ] You must install the following plugins on your Cloudify Manager, however you may skip the Cloud plugin if the Cloud is not relevant to you.

    - [ ] `cloudify-aws-plugin`, version 2.3.0 or higher, see [releases](https://github.com/cloudify-cosmo/cloudify-aws-plugin/releases).
    - [ ] `cloudify-azure-plugin`, version 2.1.7 or higher, see [releases](https://github.com/cloudify-cosmo/cloudify-azure-plugin/releases).
    - [ ] `cloudify-gcp-plugin`, version 1.4.4 or higher, see [releases](https://github.com/cloudify-cosmo/cloudify-gcp-plugin/releases).
    - [ ] `cloudify-openstack-plugin`, version 3.2.2 or higher, see [releases](https://github.com/cloudify-cosmo/cloudify-openstack-plugin/releases).
    - [ ] `cloudify-utilites-plugin`, version 1.14.0 or higher, see [releases](https://github.com/cloudify-incubator/cloudify-utilities-plugin/releases).
    - [ ] `cloudify-fabric-plugin`, version 1.5.3 or higher, see [releases](https://github.com/cloudify-cosmo/cloudify-fabric-plugin/releases).

To learn how to upload plugins, see [uploading plugins](#how-to-upload-plugins).

- [ ] You must create the following secrets, however, you may skip those cloud secrets that are not for your cloud.

    - [ ] If you wish to use AWS, please create the [required AWS secrets](#aws-secrets-checklist).
    - [ ] If you wish to use Azure, please create the [required Azure secrets](#azure-secrets-checklist).
    - [ ] If you wish to use GCP, please create the [required GCP secrets](#gcp-secrets-checklist).
    - [ ] If you wish to use Openstack, please create the [required Openstack secrets](#openstack-secrets-checklist).

To learn how to create secrets, see [creating secrets](#how-to-create-secrets).

## Installation steps

First you will need to make sure that you have the latest getting-started blueprint. These are located at [Blueprint Examples Releases](https://github.com/cloudify-community/blueprint-examples/releases). Look for the zip archive with a name similar to __getting-started-5.0.5-24.zip__. Copy the link URL. You will need it to complete these steps.

There are two methods to install the getting started application:

1. [Install getting started with the CLI](#install-getting-started-with-the-cli).
1. [Install getting started with the UI](#install-getting-started-with-the-ui).

#### Install Docker with the CLI

Upload the blueprint to you Cloudify Manager with the following command:

```shell
cfy blueprints upload [BLUEPRINT URL] -b [BLUEPRINT ID]
```

You can provide any ID you like for the blueprint. You will need it in the following steps.

Create the deployment on your Cloudify Manager with the following command:

```shell
cfy deployments create -b [BLUEPRINT ID]
```

Execute the install workflow on your deployment:

```shell
cfy executions start install -d [BLUEPRINT ID]
```

#### Install Docker with the UI

Select **Local Blueprints** from the menu on the left.

On the right side of the local blueprints page, select **Upload**.

Paste the URL of the blueprint package in the **URL** field. Provide any name you like.

Select *mc-docker.yaml* from the **Blueprint YAML file** menu.

You can leave the **Blueprint icon** field blank. It is only for decoration.

Click **Upload**.

The blueprint should appear in the blueprint list under the name you provided.

On the right, you will see a rocket icon. Select, the rocket icon and you will enter the create deployment dialog.

Provide a name you like in the **Deployment name** field.

You can skip the **Site name** field.

Provide values for any inputs that you would like to change.

Click **Deploy**.

The blueprint should appear in the deployment list under the name you provided.

You can now select **Install** from the workflow menu under your deployment.

# Appendix

### Install Cloudify Manager with Docker

If you have Docker, you can install a Cloudify Manager with the following command:

```shell
sudo docker run --name cfy_manager_local -d --restart unless-stopped -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --security-opt seccomp:unconfined --cap-add SYS_ADMIN -p 80:80 -p 8000:8000 cloudifyplatform/community-cloudify-manager-aio
```

### How to upload plugins

There are two methods to upload a plugin on your Cloudify manager:

1. [Uploading plugins with the Cloudify CLI](#Uploading-plugins-with-the-cloudify-cli).
1. [Uploading plugins with the Cloudify UI](#Uploading-plugins-with-the-cloudify-ui).

[Return to requirements](#requirements).

#### Uploading plugins with the Cloudify CLI

If you know the path or URL of the Cloudify Plugin Wagon and Plugin YAML, then you may run the following command:

```shell
cfy plugins upload [URL OR PATH TO PLUGIN WAGON] -y [URL OR PATH TO PLUGIN YAML]
```

#### Uploading plugins with the Cloudify UI

Select **System Resources** from the menu on the left.

Find the **Plugins** widget. By default, this is the first widget on the system resources page.

Click on **Upload**.

Paste the URL of a plugin wagon in the **Wagon file** field.

Paste the URL of the plugin YAML in the **YAML file** field.

Click **Upload**.

### How to create secrets

There are two methods to create a secret on your Cloudify manager:

1. [Create secrets with the Cloudify CLI](#Creating-secrets-with-the-cloudify-cli).
1. [Create secrets with the Cloudify UI](#Creating-secrets-with-the-cloudify-ui).

[Return to requirements](#requirements).

#### Creating secrets with the Cloudify CLI

You can create secrets with the following CLI commands.

If the secret content is a string:

```shell
cfy secrets create [SECRET NAME] -s [SECRET CONTENT]
```

If the secret content is in a file, for example if the secret is a RSA key:

```shell
cfy secrets create [SECRET NAME] -f [PATH TO FILE CONTAINING SECRET CONTENT]
```

#### Creating secrets with the Cloudify UI

Select **System Resources** from the menu on the left.

Find the **Plugins** widget. By default, this is the first widget on the system resources page.

Click on **Secrets**.

Provide the secret key in the **Secret key** field.

Provide the secret value in the **Secret value** field. Alternately, provide a local file path in the **Get secret value from file** menu.

Click **Create**.

#### AWS secrets checklist

If you are an AWS user, you must create the following secrets:

  - [ ] `aws_access_key_id` AWS Access Key, e.g.: `cfy secrets create -u aws_access_key_id -s ...................`.
  - [ ] `aws_secret_access_key`: AWS Secret Access Key, e.g.: `cfy secrets create -u aws_secret_access_key -s ...................`.
  - [ ] `aws_region_name`: AWS region name Key, e.g.: `cfy secrets create -u aws_region_name -s us-east-1`.
  - [ ] `ec2_region_endpoint`: AWS region endpoint, e.g.: `cfy secrets create -u ec2_region_endpoint -s ec2.us-east-1.amazonaws.com`.
  - [ ] `aws_availability_zone` AWS availability zone, e.g.: `cfy secrets create -u aws_availability_zone -s eu-central-1b`.

If you need help locating your credentials, read about [AWS Access Key](https://aws.amazon.com/blogs/security/wheres-my-secret-access-key/).

[Return to requirements](#requirements).

#### Azure secrets checklist

If you are an Azure user, you must create the following secrets:

  - [ ] `azure_subscription_id`: Azure subscription ID: `cfy secrets create -u azure_subscription_id -s 00000000-0000-0000-0000-000000000000`.
  - [ ] `azure_tenant_id`: Azure subscription ID: `cfy secrets create -u azure_tenant_id -s 00000000-0000-0000-0000-000000000000`.
  - [ ] `azure_client_id`: Azure subscription ID: `cfy secrets create -u azure_client_id -s 00000000-0000-0000-0000-000000000000`.
  - [ ] `azure_client_secret`: Azure subscription ID: `cfy secrets create -u azure_client_secret -s ...........`.
  - [ ] `azure_location`: Azure subscription ID: `cfy secrets create -u azure_location -s westeurope`.

If you need help locating your credentials, read about [Azure Plugin Configuration](https://docs.cloudify.co/5.0.0/working_with/official_plugins/infrastructure/azure/#providing-credentials-as-secrets):

[Return to requirements](#requirements).

#### GCP secrets checklist

If you are a GCP user, you must create the following secrets:
  - [ ] `gcp_credentials`: A GCP service account key in JSON format. **Hint: Create this secret from a file:** `cfy secrets create gcp_credentials -f ./path/to/JSON key`.
  - [ ] `gcp_zone`: A GCP Zone such as `us-east1-b`: `cfy secrets create gcp_zone -s zone`

If you need help locating your credentials, read about [GCP Plugin Configuration](https://docs.cloudify.co/5.0.0/working_with/official_plugins/infrastructure/gcp/).

[Return to requirements](#requirements).

#### Openstack secrets checklist

If you are an Openstack user, you must create the following secrets:

  - [ ] `openstack_auth_url`: Openstack Auth URL: `cfy secrets create -u openstack_auth_url -s https://my.openstack.com:5000/v2.0`
  - [ ] `openstack_project_name`: Openstack Project Name: `cfy secrets create -u openstack_project_name -s project`
  - [ ] `openstack_tenant_name`: Openstack Tenant Name: `cfy secrets create -u openstack_tenant_name -s tenant`
  - [ ] `openstack_username`: Openstack Username: `cfy secrets create -u openstack_username -s janedoe`
  - [ ] `openstack_password`: Openstack Password: `cfy secrets create -u openstack_password -s peacelove`
  - [ ] `openstack_region`: Openstack Region Name: `cfy secrets create -u openstack_region -s RegionOne`
  - [ ] `openstack_external_network`: The ID of the floating IP network that you will use to connect to the internet.
  - [ ] `base_image_id`: The image ID of a Centos 7 that supports Cloud Init.
  - [ ] `base_flavor_id`: The flavor ID of an Openstack flavor that is appropriate for your Centos 7 "base_image_id".

If you need help locating your credentials, read about [Openstack RC File](https://docs.openstack.org/zh_CN/user-guide/common/cli-set-environment-variables-using-openstack-rc.html), although sourcing is not enough, these values must be created as secrets:

[Return to requirements](#requirements).

add command to install the infra+app blueprints
