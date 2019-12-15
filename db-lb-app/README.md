# DB-LB-APP

This is a suite of blueprints that demonstrates how several deployments can work together to build an application.

The components are:
  - `db`: a MariaDB cluster.
  - `lb`: an HAProxy load balancer.
  - `drupal`: an application.


## Requirements

  - Cloudify Manager 4.5.5 or higher.
  - Plugins:
    - `cloudify-aws-plugin`
    - `cloudify-azure-plugin`
    - `cloudify-gcp-plugin`
    - `cloudify-openstack-plugin v3`
    - `cloudify-utilites-plugin`
    - `cloudify-ansible-plugin`
  - Secrets:
    - Common:
      - `agent_key_public`: Public key content, e.g: `cfy secrets create -u agent_key_public -f ~/.ssh/id_rsa.pub`.
      - `agent_key_private`: Private key content, e.g: `cfy secrets create -u agent_key_private -f ~/.ssh/id_rsa`.
    - AWS:
      - `aws_access_key_id` AWS Access Key, e.g.: `cfy secrets create -u aws_access_key_id -s ...................`.
      - `aws_secret_access_key`: AWS Secret Access Key, e.g.: `cfy secrets create -u aws_secret_access_key -s ...................`.
      - `aws_region_name`: AWS region name Key, e.g.: `cfy secrets create -u aws_region_name -s us-east-1`.
      - `ec2_region_endpoint`: AWS region endpoint, e.g.: `cfy secrets create -u ec2_region_endpoint -s ec2.us-east-1.amazonaws.com`.
      - `aws_availability_zone` AWS availability zone, e.g.: `cfy secrets create -u aws_availability_zone -s eu-central-1b`.
    - Azure:
      - `azure_subscription_id`: Azure subscription ID: `cfy secrets create -u azure_subscription_id -s 00000000-0000-0000-0000-000000000000`.
      - `azure_tenant_id`: Azure subscription ID: `cfy secrets create -u azure_tenant_id -s 00000000-0000-0000-0000-000000000000`.
      - `azure_client_id`: Azure subscription ID: `cfy secrets create -u azure_client_id -s 00000000-0000-0000-0000-000000000000`.
      - `azure_client_secret`: Azure subscription ID: `cfy secrets create -u azure_client_secret -s ...........`.
      - `azure_location`: Azure subscription ID: `cfy secrets create -u azure_location -s westeurope`.
    - GCP:
      - `gcp_client_x509_cert_url`: A GCP Service Account Client Cert URL: `cfy secrets create gcp_client_x509_cert_url -s client_cert_url`
      - `gcp_client_email`: A GCP Service Account client email: `cfy secrets create gcp_client_email -s client_email`
      - `gcp_client_id`: A GCP Service Account Client ID: `cfy secrets create gcp_client_id -s client_id`
      - `gcp_project_id`: A GCP Project ID: `cfy secrets create gcp_project_id -s project_id`
      - `gcp_private_key_id`: A GCP Project Private Key ID: `cfy secrets create gcp_private_key_id -s private_key_id`
      - `gcp_private_key`: A GCP project Private Key: `cfy secrets create gcp_private_key -f ./path/to/private-key`.
      - `gcp_region`: A GCP Region such as `us-east1`: `cfy secrets create gcp_region -s private_key_id`
      - `gcp_zone`: A GCP Zone such as `us-east1-b`: `cfy secrets create gcp_zone -s zone`
    - Openstack:
      - `openstack_auth_url`: Openstack Auth URL: `cfy secrets create -u openstack_auth_url -s https://my.openstack.com:5000/v2.0`
      - `openstack_project_name`: Openstack Project Name: `cfy secrets create -u openstack_project_name -s project`
      - `openstack_tenant_name`: Openstack Tenant Name: `cfy secrets create -u openstack_tenant_name -s tenant`
      - `openstack_username`: Openstack Username: `cfy secrets create -u openstack_username -s janedoe`
      - `openstack_password`: Openstack Password: `cfy secrets create -u openstack_password -s peacelove`
      - `openstack_region`: Openstack Region Name: `cfy secrets create -u openstack_region -s RegionOne`

## Steps

### Install the network deployment

Get the [latest release](https://github.com/cloudify-community/blueprint-examples/releases) of our example network blueprints.

For example, if you are an AWS user:

  `cfy install https://github.com/cloudify-community/blueprint-examples/releases/download/4.5.5-4/aws-example-network.zip -n blueprint.yaml -b aws`

If you are an Azure user:

  `cfy install https://github.com/cloudify-community/blueprint-examples/releases/download/4.5.5-4/azure-example-network.zip -n blueprint.yaml -b azure`

If you are an GCP user:

  `cfy install https://github.com/cloudify-community/blueprint-examples/releases/download/4.5.5-4/gcp-example-network.zip -n blueprint.yaml -b gcp`

If you are an Openstack user:

  `cfy install https://github.com/cloudify-community/blueprint-examples/releases/download/4.5.5-4/openstack-example-network.zip -n blueprint.yaml -i external_network_id=0000-0000-0000-0000 -b openstack`


### Upload the infrastructure blueprint

For example, if you are an AWS user:

  `cfy blueprints upload https://github.com/cloudify-community/blueprint-examples/releases/download/4.5.5-4/db-lb-app-infrastructure.zip -n aws.yaml -b infrastructure`

If you are an Azure user:

  `cfy blueprints upload https://github.com/cloudify-community/blueprint-examples/releases/download/4.5.5-4/db-lb-app-infrastructure.zip -n azure.yaml -b infrastructure`

If you are an GCP user:

  `cfy blueprints upload https://github.com/cloudify-community/blueprint-examples/releases/download/4.5.5-4/db-lb-app-infrastructure.zip -n gcp.yaml -b infrastructure`

If you are an Openstack user:

  `cfy blueprints upload https://github.com/cloudify-community/blueprint-examples/releases/download/4.5.5-4/db-lb-app-infrastructure.zip -n openstack.yaml -b infrastructure`

### Install the database

  `cfy install https://github.com/cloudify-community/blueprint-examples/releases/download/4.5.5-4/db-lb-app-db.zip -n application.yaml -b db`

  **Openstack**\
  `cfy install https://github.com/cloudify-community/blueprint-examples/releases/download/4.5.5-4/db-lb-app-db.zip -n application.yaml -b db -i infrastructure--image_id=ca19086a-1147-4052-85bd-ba40e9e350d4 -i infrastructure--flavor_id=3 -i infrastructure--region_name=RegionOne -i infrastructure--resource_name_prefix=db`

  Where `infrastructure--image_id` is ID of centos-7-with-docker image.
### Install the load balancer

  `cfy install https://github.com/cloudify-community/blueprint-examples/releases/download/4.5.5-4/db-lb-app-lb.zip -n application.yaml -b lb`

  **Openstack**\
  `cfy install https://github.com/cloudify-community/blueprint-examples/releases/download/4.5.5-4/db-lb-app-lb.zip -n application.yaml -b lb -i infrastructure--resource_name_prefix='lb' -i infrastructure--image_id=ca19086a-1147-4052-85bd-ba40e9e350d4 -i infrastructure--flavor_id=3 -i infrastructure--region_name=RegionOne`


### Install the application (Drupal)

  `cfy install https://github.com/cloudify-community/blueprint-examples/releases/download/4.5.5-4/db-lb-app-app.zip -n application.yaml -b app`

  **Openstack**\
  `cfy install https://github.com/cloudify-community/blueprint-examples/releases/download/4.5.5-4/db-lb-app-app.zip -n application.yaml -b app -i infrastructure--resource_name_prefix='app' -i infrastructure--image_id=ca19086a-1147-4052-85bd-ba40e9e350d4 -i infrastructure--flavor_id=3 -i infrastructure--region_name=RegionOne`

  
## Complete Application Installation

  `cfy deployment outputs app`
