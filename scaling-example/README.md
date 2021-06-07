This example demonstrates a scalable infrastructure setup in **AWS**  using Ansible playbooks to deploy it, the deployment consists of:

 * Instance
 * Security Group
 * Network
 * All of the essential peripherals in AWS (IP address, NIC, etc...).

In this example, we will deploy only the infrastructure and scale it.

## Prerequisites
This example expects the following prerequisites:

* A Cloudify manager ready(version 5.1 and above). 
* Access to AWS infrastructure is required to demonstrate this example.
* `selinux` installed on manager VM/docker(`yum install libselinux-python3`).


#### Cloudify CLI or Cloudify Management Console

Cloudify allows for multiple user interfaces. Some users find the Cloudify Management Console (web based UI) more intuitive while others prefer the Cloudify CLI (Command Line Interface). This tutorial and all the following ones will describe both methods.

* [Using the Cloudify Management Console](#cloudify-management-console)
* [Using the Cloudify CLI](#cloudify-cli)

{{% note %}}
Community version - Some of the options described in the guide are not available in the community version management console (web UI). An example would be setting up secrets. You can still perform all of the functionality using the Cloudify CLI.
{{% /note %}}

## Cloudify Management Console

This section explains how to run the above described steps using the Cloudify Management Console.
The Cloudify Management Console and Cloudify CLI can be used interchangeably for all Cloudify activities.



### Create Secrets

To connect to AWS, credentials are required.
Cloudify recommends storing such sensitive information in a Cloudify secret.
Secrets are kept encrypted in a secure way and used in run-time by the system.
Learn more about Cloudify secrets [here](https://docs.cloudify.co/latest/working_with/manager/using-secrets/).

AWS credentials can be created by following the guide [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey).

To store the access keys as secrets in the Cloudify Manager, login to the Cloudify Management Console and select the **System Resources** page. Scroll to the **Secret Store Management** widget and use the **Create** button to add the following new secrets:

* aws_access_key_id
* aws_secret_access_key

### Upload Plugins

Plugins are Cloudify's extendable interfaces to services, cloud providers, and automation tools.
I.e., running playbooks requires the Ansible plugin.

To upload the required plugins to your manager, select the **Cloudify Catalog** page, scroll to the **Plugins Catalog** widget and select the plugins you wish to upload.

For this example, upload the following plugins:

* Utilities
* Ansible.



### Upload Blueprint

A blueprint is a general purpose model for describing systems, services or any orchestrated object topology.
Blueprints are represented as descriptive code (yaml based files) and typically stored and managed as part of the source repository.
The example blueprint is available [here](https://github.com/cloudify-community/blueprint-examples/blob/master/scaling-example/ansible.yaml).

The flow required to setup a service consists of:

1. Upload the blueprint describing the service to the Cloudify Manager.
1. Create a deployment from the uploaded blueprint. This generates a model of the service topology in the Cloudify database and provides the "context" needed for running workflows.
1. Run the **install** workflow for the created deployment to apply the model to the infrastructure.

Let's run these one by one.

To upload a blueprint to the Cloudify Manager, select the **Blueprints** page, and use the **Upload blueprint** button, select ansible.yaml file.




### Deploy & Install

Once the blueprint is uploaded, it will be displayed in the Blueprints widget. to deploy the blueprint click the **Create deployment** button next to the blueprint you wish to deploy. Specify a deployment name, update any inputs (such as the AWS region), and click **Deploy & Install**. Changing inputs is completely optional and the defaults are safe to use.

You will be directed to the **Deployment** page and will be able to track the progress of the execution.

The deployment you have created should be displayed in the deployments list in the **Deployments** page.

### Validate

In this example we have setup a simple infrastructure. A virtual instance (VM) was created in the region specified in the Deployment inputs alongside a new network and various other resources.
This is done by executing two Ansible playbooks:
1. [playbook.yaml](https://github.com/cloudify-community/blueprint-examples/blob/master/scaling-example/resources/ansible/playbook.yaml) which creates All the networking infrastructure.
2. [create_eni_and_vm_playbook.yaml](https://github.com/cloudify-community/blueprint-examples/blob/master/scaling-example/resources/ansible/create_eni_and_vm_playbook.yaml) which creates eni and VM.

* Go to your AWS console and see the new instance and other resources that were created.
* Examine the Deployment page in the Cloudify Management Console for more information about your deployed nodes, topology, and view the installation logs.

To login to your new AWS instance, you can look at the on the `install_eni_vm-playbook` Node instance runtime properties to find your AWS instance public IP.
Also, look at the **Deployment Outputs/Capabilities** widget on the Deployment screen to find your AWS instance SSH username, and SSH private key.

### Scale

To scale the infrastructure, means to create more VM's the scale workflow is being used.
Go to **Deployments** page and select your deployment, then click on `Execute workflow` ->  `Default workflows` -> `Scale`.
Fill the inputs:
* `scalable_entity_name` : vm-group
* `delta` : 1

Press **Execute**.

Notice that another `install_eni_vm-playbook` node instance created, Check AWS console to see the new VM created.

### Teardown

To remove the deployment and destroy the orchestrated infrastructure resources, run the **Uninstall** workflow by clicking the **Execute workflow** menu next to the deployment, expanding **Default workflows**, and selecting **Uninstall**.


____


## Cloudify CLI

Create a CLI profile instructing your CLI how to connect with the Cloudify Manager by running the following CLI commands

```bash
cfy init
cfy profiles use <your manager hostname / URL / IP> -u admin -p <the admin  password> --ssl
cfy profiles set --manager-tenant default_tenant
```

### Create Secrets

To enable Cloudify to connect to AWS, credentials are required.
Cloudify recommends storing such sensitive information as a Cloudify secret.
Secrets are encrypted in a secure way and used during run-time by the system.
Learn more about Cloudify secrets [here]({{< relref "/working_with/manager/using-secrets.md" >}}).

AWS credentials can be created by following the guide [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey_CLIAPI).

To store the access keys as secrets via the Cloudify CLI, run the following (replacing <value> with the actual string retrieved from AWS):

```bash
cfy secrets create aws_access_key_id --secret-string <value>
cfy secrets create aws_secret_access_key --secret-string <value>
```

### Upload Plugins

Plugins are Cloudify's extendable interfaces to services, cloud providers, and automation tools.
Executing playbooks requires the Ansible plugin. You may upload specific plugins or, for simplicity, upload the plugin bundle containing all of the basic, pre-packaged, plugins.

To upload the default plugins bundle (this may take a few minutes depending on your internet speed):
```bash
cfy plugins bundle-upload
```

**Tip**: Read more about [plugins](https://docs.cloudify.co/latest/working_with/official_plugins/) and [writing your own plugins](https://docs.cloudify.co/latest/developer/writing_plugins/).

### Upload Blueprint and Deploy

A blueprint is a general purpose model for describing systems, services, or any orchestrated object topology. Blueprints are represented as descriptive code (YAML-based files) and are typically stored and managed as part of the source code repository.

The `ansible.yaml` blueprint is available [here](https://github.com/cloudify-community/blueprint-examples/blob/master/scaling-example/ansible.yaml).

Uploading a blueprint to Cloudify can be done by direct upload or by providing the link in the source code repository.
The flow to do that is:

 1. Upload the blueprint.
 1. Create a deployment from the uploaded blueprint. This generates a model of the service topology in the Cloudify database and provides the "context" needed for running workflows.
 1. Run the **install** workflow for the created deployment to apply the model to the infrastructure.

In order to perform this flow as a single unit, we will use the **install** command.

```bash
cfy install <path-to-blueprint-zip> -n ansible.yaml}
```

### Validate

In this example, we have set up an infrastructure. A virtual instance (VM) was created in the region specified in the Deployment inputs alongside a new network and various other resources.

* Go to your AWS console and see the new instance and other resources that were created.
* You can easily get a list of all deployed nodes by running:

```
$ cfy nodes list -d scaling-example

Listing nodes for deployment scaling-example...

Nodes:
+-------------------------+-----------------+-----------------+---------+--------------------------------------+------------+----------------+---------------------+-----------------------------+------------+
|            id           |  deployment_id  |   blueprint_id  | host_id |                 type                 | visibility |  tenant_name   | number_of_instances | planned_number_of_instances | created_by |
+-------------------------+-----------------+-----------------+---------+--------------------------------------+------------+----------------+---------------------+-----------------------------+------------+
|  install_infra_playbook | scaling-example | scaling-example |         |         cloudify.nodes.Root          |   tenant   | default_tenant |          1          |              1              |   admin    |
| install_eni_vm_playbook | scaling-example | scaling-example |         |         cloudify.nodes.Root          |   tenant   | default_tenant |          1          |              1              |   admin    |
|        cloud_init       | scaling-example | scaling-example |         | cloudify.nodes.CloudInit.CloudConfig |   tenant   | default_tenant |          1          |              1              |   admin    |
|        agent_key        | scaling-example | scaling-example |         |      cloudify.keys.nodes.RSAKey      |   tenant   | default_tenant |          1          |              1              |   admin    |
+-------------------------+-----------------+-----------------+---------+--------------------------------------+------------+----------------+---------------------+-----------------------------+------------+

Showing 4 of 4 nodes
```
**Tip**: To check out some more commands to use with the Cloudify Management Console, run `cfy --help`

An even easier way to review your deployment is through the [Cloudify Management Console](#validate).
Login to the console and browse to the **Deployments** page.
Select the deployment (`scaling-example`) and explore the topology, inputs, outputs, nodes, and logs.

This is also a good time to examine the blueprint used in the example.
The blueprint can be examined in the Cloudify Management Console, however in this case
we will go to the Cloudify examples repository in Github and examine it there: [ansible.yaml](https://github.com/cloudify-community/blueprint-examples/blob/master/scaling-example/ansible.yaml)

### Scale

In order to scale the infrastructure, means to create more VM's, the scale workflow is being used.
execute:
`cfy executions start scale -d scaling-example -p scalable_entity_name=vm-group -p delta=1`

Notice that another `install_eni_vm-playbook` node instance created, Check AWS console to see the new VM created.

```
$ cfy nodes list -d scaling-example

Listing nodes for deployment scaling-example...

Nodes:
+-------------------------+-----------------+-----------------+---------+--------------------------------------+------------+----------------+---------------------+-----------------------------+------------+
|            id           |  deployment_id  |   blueprint_id  | host_id |                 type                 | visibility |  tenant_name   | number_of_instances | planned_number_of_instances | created_by |
+-------------------------+-----------------+-----------------+---------+--------------------------------------+------------+----------------+---------------------+-----------------------------+------------+
|  install-infra-playbook | scaling-example | scaling-example |         |         cloudify.nodes.Root          |   tenant   | default_tenant |          1          |              1              |   admin    |
| install_eni_vm-playbook | scaling-example | scaling-example |         |         cloudify.nodes.Root          |   tenant   | default_tenant |          2          |              2              |   admin    |
|        cloud_init       | scaling-example | scaling-example |         | cloudify.nodes.CloudInit.CloudConfig |   tenant   | default_tenant |          1          |              1              |   admin    |
|        agent_key        | scaling-example | scaling-example |         |      cloudify.keys.nodes.RSAKey      |   tenant   | default_tenant |          1          |              1              |   admin    |
+-------------------------+-----------------+-----------------+---------+--------------------------------------+------------+----------------+---------------------+-----------------------------+------------+

Showing 4 of 4 nodes

```

Notice that number of instances for node `install_eni_vm-playbook` is two.

### Teardown

To remove the deployment and delete all resources from AWS simply run the uninstall command:
```bash
cfy uninstall scaling-example
```
