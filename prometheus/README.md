

# Prometheus Example


## Prerequisites:

  * You need the `jmespath` python package: `pip install jmespath`.
  * Openstack users require cloudify-openstack-plugin 3.0.0 or greater.

### Install the plugins

Install Cloudify plugins
```shell
cfy plugins bundle-upload
```

### Creating secrets

Create secrets according to your IaaS provider.

Replace <value> with actual values, without the <>

For **AWS**
```shell
cfy secrets create aws_access_key_id --secret-string <value>
cfy secrets create aws_secret_access_key --secret-string <value>
```
 
For **Azure**
```shell
cfy secrets create azure_subscription_id --secret-string <value>
cfy secrets create azure_tenant_id --secret-string <value>
cfy secrets create azure_client_id --secret-string <value>
cfy secrets create azure_client_secret --secret-string <value>
```

For **GCP**

gcp_credentials: A GCP service account key in JSON format. **Hint: Create this secret from a file:**
```shell   
`cfy secrets create gcp_credentials -f ./path/to/JSON key`.
```  
                                           
gcp_zone: A GCP Zone such as `us-east1-b`:                                                              

```shell
cfy secrets create gcp_zone --secret-string <zone>                                                                                                                                              
```

gcp_project_id:
```shell
cfy secrets create gcp_project_id --secret-string <project_id>                                                                                                                                              
```

For **Openstack**
```shell
cfy secrets create openstack_username --secret-string <value>
cfy secrets create openstack_password --secret-string <value>
cfy secrets create openstack_tenant_name --secret-string <value>
cfy secrets create openstack_auth_url --secret-string <value>
```
      
For **Key pair**
```shell
ssh-keygen -t rsa -C "your_email@example.com"
# [ENTER] [ENTER] [ENTER] [ENTER] [ENTER]
cfy secrets create agent_key_private -f ~/.ssh/id_rsa -u
cfy secrets create agent_key_public -f ~/.ssh/id_rsa.pub -u
```
         
### Running the example


For **AWS**:

```shell
cfy install aws.yaml -i region_name=eu-central-1 -i availability_zone=eu-central-1b -i image_id=ami-04f992cf4dcaed3c4 -i instance_type=t2.large -i agent_user=ec2-user
```

For **Azure**:

```shell
cfy install azure.yaml -i location=westeurope
```

For **GCP**:

```shell
cfy install gcp.yaml -i region=<region>
```

For **Openstack**:

```shell
cfy install \
  ~/dev/repos/blueprint-examples/prometheus/openstack.yaml
  \ -i ~/dev/repos/blueprint-examples/prometheus/inputs/everything.yaml \
  -i external_network_id=dda079ce-12cf-4309-879a-8e67aec94de4 \
  -i region_name=RegionOne \
  -i image_id=70de1e0f-2951-4eae-9a8f-05afd97cd036 \
  -i flavor_id=3 -b prometheus
```
