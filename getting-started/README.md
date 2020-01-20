# Cloudify Getting Started

This is a suite of blueprints that demonstrates how to design a Cloudify blueprint, while separating the infrastructure layer and the application layer.

There are three components to this getting started guide:

  - Infrastructure blueprints (there is a separate blueprint for AWS, Azure, Openstack, and GCP).
  - JBoss Application blueprint
  - Nodejs Application bluepring


## Requirements

  - You will need a Cloudify Manager v5.0.5 or higher.

  - The following plugins should be installed on your Cloudify Manager, however you may skip the Cloud plugin if the Cloud is not relevant to you.

    - [ ] `cloudify-aws-plugin`, version 2.3.0 or higher.
    - [ ] `cloudify-azure-plugin`, version 2.1.7 or higher.
    - [ ] `cloudify-gcp-plugin`, version 1.4.4 or higher.
    - [ ] `cloudify-openstack-plugin`, version 3.2.2 or higher.
    - [ ] `cloudify-utilites-plugin`, version 1.14.0 or higher.
    - [ ] `cloudify-fabric-plugin`, version 1.5.3 or higher.

  - You will need to create the following secrets, however, you may skip the Cloud secrets if the Cloud is not relevant to you.

    - Common:
      - [ ] `agent_key_public`: Public key content, e.g: `cfy secrets create -u agent_key_public -f ~/.ssh/id_rsa.pub`.
      - [ ] `agent_key_private`: Private key content, e.g: `cfy secrets create -u agent_key_private -f ~/.ssh/id_rsa`.

    - AWS, see [AWS Access Key](https://aws.amazon.com/blogs/security/wheres-my-secret-access-key/).
      - [ ] `aws_access_key_id` AWS Access Key, e.g.: `cfy secrets create -u aws_access_key_id -s ...................`.
      - [ ] `aws_secret_access_key`: AWS Secret Access Key, e.g.: `cfy secrets create -u aws_secret_access_key -s ...................`.
      - [ ] `aws_region_name`: AWS region name Key, e.g.: `cfy secrets create -u aws_region_name -s us-east-1`.
      - [ ] `ec2_region_endpoint`: AWS region endpoint, e.g.: `cfy secrets create -u ec2_region_endpoint -s ec2.us-east-1.amazonaws.com`.
      - [ ] `aws_availability_zone` AWS availability zone, e.g.: `cfy secrets create -u aws_availability_zone -s eu-central-1b`.

    - Azure, see [Azure Plugin Configuration](https://docs.cloudify.co/5.0.0/working_with/official_plugins/infrastructure/azure/#providing-credentials-as-secrets):
      - [ ] `azure_subscription_id`: Azure subscription ID: `cfy secrets create -u azure_subscription_id -s 00000000-0000-0000-0000-000000000000`.
      - [ ] `azure_tenant_id`: Azure subscription ID: `cfy secrets create -u azure_tenant_id -s 00000000-0000-0000-0000-000000000000`.
      - [ ] `azure_client_id`: Azure subscription ID: `cfy secrets create -u azure_client_id -s 00000000-0000-0000-0000-000000000000`.
      - [ ] `azure_client_secret`: Azure subscription ID: `cfy secrets create -u azure_client_secret -s ...........`.
      - [ ] `azure_location`: Azure subscription ID: `cfy secrets create -u azure_location -s westeurope`.

    - GCP, see [GCP Plugin Configuration](https://docs.cloudify.co/5.0.0/working_with/official_plugins/infrastructure/gcp/).
      - [ ] `gcp_client_x509_cert_url`: A GCP Service Account Client Cert URL: `cfy secrets create gcp_client_x509_cert_url -s client_cert_url`
      - [ ] `gcp_client_email`: A GCP Service Account client email: `cfy secrets create gcp_client_email -s client_email`
      - [ ] `gcp_client_id`: A GCP Service Account Client ID: `cfy secrets create gcp_client_id -s client_id`
      - [ ] `gcp_project_id`: A GCP Project ID: `cfy secrets create gcp_project_id -s project_id`
      - [ ] `gcp_private_key_id`: A GCP Project Private Key ID: `cfy secrets create gcp_private_key_id -s private_key_id`
      - [ ] `gcp_private_key`: A GCP project Private Key: `cfy secrets create gcp_private_key -f ./path/to/private-key`.
      - [ ] `gcp_region`: A GCP Region such as `us-east1`: `cfy secrets create gcp_region -s private_key_id`
      - [ ] `gcp_zone`: A GCP Zone such as `us-east1-b`: `cfy secrets create gcp_zone -s zone`

    - Openstack, see [Openstack RC File](https://docs.openstack.org/zh_CN/user-guide/common/cli-set-environment-variables-using-openstack-rc.html), although sourcing is not enough, these values must be created as secrets:
      - [ ] `openstack_auth_url`: Openstack Auth URL: `cfy secrets create -u openstack_auth_url -s https://my.openstack.com:5000/v2.0`
      - [ ] `openstack_project_name`: Openstack Project Name: `cfy secrets create -u openstack_project_name -s project`
      - [ ] `openstack_tenant_name`: Openstack Tenant Name: `cfy secrets create -u openstack_tenant_name -s tenant`
      - [ ] `openstack_username`: Openstack Username: `cfy secrets create -u openstack_username -s janedoe`
      - [ ] `openstack_password`: Openstack Password: `cfy secrets create -u openstack_password -s peacelove`
      - [ ] `openstack_region`: Openstack Region Name: `cfy secrets create -u openstack_region -s RegionOne`
      - [ ] `openstack_external_network`: The ID of the floating IP network that you will use to connect to the internet.
      - [ ] `base_image_id`: The image ID of a Centos 7 that supports Cloud Init.
      - [ ] `base_flavor_id`: The flavor ID of an Openstack flavor that is appropriate for your Centos 7 "base_image_id".

## Steps


### Via the Cloudify CLI

After you have uploaded you plugins to your Cloudify Manager and created your secrets (see ["requirements" above](#Requirements)), you will need to upload the application blueprint to your Cloudify Manager.

Find the blueprint URL, which is located (here)[https://github.com/cloudify-community/blueprint-examples/releases]. Search for a zip package named "getting-started-X.X.X.zip", where "X.X.X" is some number like "5.0.0-15".

Copy the URL and paste it in the following command in place of <BLUEPRINT URL>:

```shell
cfy blueprints upload -b getting-started <BLUEPRINT URL>
```

You must now gather the inputs to your deployment.

```shell
cfy deployments create -b getting-started
```

You should now execute the install workflow, which will actually create all of the resources including the application.

```shell
cfy executions start install -d getting-started
```

