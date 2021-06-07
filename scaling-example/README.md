+++
cloud_full = "Amazon Web Services"
cloud = "AWS"
blueprint_name = "ansible.yaml"
deployment_name = "scaling-example"
cloud_auth_ui_link = "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey"
cloud_auth_cli_link = "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey_CLIAPI"
cfy_manager_name = "Cloudify Manager"
cfy_console_name = "Cloudify Management Console"
product_name = "Cloudify"
deployment_name = scaling-example
+++

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

AWS credentials can be created by following the guide [here]({{< param cloud_auth_ui_link>}}).

To store the access keys as secrets in the {{< param cfy_manager_name >}}, login to the {{< param cfy_console_name >}} and select the **System Resources** page. Scroll to the **Secret Store Management** widget and use the **Create** button to add the following new secrets:

* aws_access_key_id
* aws_secret_access_key

### Upload Plugins

Plugins are {{< param product_name >}}'s extendable interfaces to services, cloud providers, and automation tools.
I.e., connecting to {{< param cloud >}} requires the {{< param cloud >}} plugin.

To upload the required plugins to your manager, select the **Cloudify Catalog** page, scroll to the **Plugins Catalog** widget and select the plugins you wish to upload.

For this example, upload the following plugins:

* Utilities
* Ansible.



### Upload Blueprint

A blueprint is a general purpose model for describing systems, services or any orchestrated object topology.
Blueprints are represented as descriptive code (yaml based files) and typically stored and managed as part of the source repository.
The example blueprint is available [here](https://github.com/cloudify-community/blueprint-examples/blob/master/scaling-example/ansible.yaml).

The flow required to setup a service consists of:

1. Upload the blueprint describing the service to the {{< param cfy_manager_name >}}.
1. Create a deployment from the uploaded blueprint. This generates a model of the service topology in the {{< param product_name >}} database and provides the "context" needed for running workflows.
1. Run the **install** workflow for the created deployment to apply the model to the infrastructure.

Let's run these one by one.

To upload a blueprint to the {{< param cfy_manager_name >}}, select the **Blueprints** page, and use the **Upload blueprint** button, select ansible.yaml file.




### Deploy & Install

Once the blueprint is uploaded, it will be displayed in the Blueprints widget. to deploy the blueprint click the **Create deployment** button next to the blueprint you wish to deploy. Specify a deployment name, update any inputs (such as the {{< param cloud >}} region), and click **Deploy & Install**. Changing inputs is completely optional and the defaults are safe to use.

You will be directed to the **Deployment** page and will be able to track the progress of the execution.

The deployment you have created should be displayed in the deployments list in the **Deployments** page.

### Validate

In this example we have setup a simple infrastructure. A virtual instance (VM) was created in the region specified in the Deployment inputs alongside a new network and various other resources.
This is done by executing two Ansible playbooks:
1. [playbook.yaml](https://github.com/cloudify-community/blueprint-examples/blob/master/scaling-example/resources/ansible/playbook.yaml) which creates All the networking infrastructure.
2. [create_eni_and_vm_playbook.yaml](https://github.com/cloudify-community/blueprint-examples/blob/master/scaling-example/resources/ansible/create_eni_and_vm_playbook.yaml) which creates eni and VM.

* Go to your {{< param cloud >}} console and see the new instance and other resources that were created.
* Examine the Deployment page in the {{< param cfy_console_name >}} for more information about your deployed nodes, topology, and view the installation logs.

To login to your new {{< param cloud >}} instance, you can look at the on the `install_eni_vm-playbook` Node instance runtime properties to find your {{< param cloud >}} instance public IP.
Also, look at the **Deployment Outputs/Capabilities** widget on the Deployment screen to find your {{< param cloud >}} instance SSH username, and SSH private key.

### Scale

To scale the infrastructure, means to create more VM's the scale workflow is being used.
Go to **Deployments** page and select your deployment, then click on `Execute workflow` ->  `Default workflows` -> `Scale`.
Fill the inputs:
* `scalable_entity_name` : vm-group
* `delta` : 1

Press **Execute**.

Notice that another `install_eni_vm-playbook` node instance created, Check {{< param cloud >}} console to see the new VM created.

### Teardown

To remove the deployment and destroy the orchestrated infrastructure resources, run the **Uninstall** workflow by clicking the **Execute workflow** menu next to the deployment, expanding **Default workflows**, and selecting **Uninstall**.


____


## {{< param cfy_cli_name >}}

Create a CLI profile instructing your CLI how to connect with the {{< param cfy_manager_name >}} by running the following CLI commands

```bash
cfy init
cfy profiles use <your manager hostname / URL / IP> -u admin -p <the admin  password> --ssl
cfy profiles set --manager-tenant default_tenant
```

### Create Secrets

To enable {{< param product_name >}} to connect to {{< param cloud >}}, credentials are required.
{{< param product_name >}} recommends storing such sensitive information as a {{< param product_name >}} secret.
Secrets are encrypted in a secure way and used during run-time by the system.
Learn more about {{< param product_name >}} secrets [here]({{< relref "/working_with/manager/using-secrets.md" >}}).

{{< param cloud >}} credentials can be created by following the guide [here]({{< param cloud_auth_cli_link>}}).

To store the access keys as secrets via the {{< param cfy_cli_name >}}, run the following (replacing <value> with the actual string retrieved from {{< param cloud >}}):

```bash
cfy secrets create aws_access_key_id --secret-string <value>
cfy secrets create aws_secret_access_key --secret-string <value>
```

### Upload Plugins

Plugins are {{< param product_name >}}'s extendable interfaces to services, cloud providers, and automation tools.
Connecting to {{< param cloud >}} requires the {{< param cloud >}} plugin. You may upload specific plugins or, for simplicity, upload the plugin bundle containing all of the basic, pre-packaged, plugins.

To upload the default plugins bundle (this may take a few minutes depending on your internet speed):
```bash
cfy plugins bundle-upload
```

**Tip**: Read more about [plugins](https://docs.cloudify.co/latest/working_with/official_plugins/) and [writing your own plugins](https://docs.cloudify.co/latest/developer/writing_plugins/).

### Upload Blueprint and Deploy

A blueprint is a general purpose model for describing systems, services, or any orchestrated object topology. Blueprints are represented as descriptive code (YAML-based files) and are typically stored and managed as part of the source code repository.

The {{< param cloud >}} infrastructure blueprint is available [here](https://github.com/cloudify-community/blueprint-examples/blob/master/scaling-example/ansible.yaml).

Uploading a blueprint to {{< param product_name >}} can be done by direct upload or by providing the link in the source code repository.
The flow to do that is:

 1. Upload the blueprint.
 1. Create a deployment from the uploaded blueprint. This generates a model of the service topology in the {{< param product_name >}} database and provides the "context" needed for running workflows.
 1. Run the **install** workflow for the created deployment to apply the model to the infrastructure.

In order to perform this flow as a single unit, we will use the **install** command.

```bash
cfy install <path-to-blueprint-zip> -n ansible.yaml}
```

### Validate

In this example, we have set up an infrastructure. A virtual instance (VM) was created in the region specified in the Deployment inputs alongside a new network and various other resources.

* Go to your {{< param cloud >}} console and see the new instance and other resources that were created.
* You can easily get a list of all deployed nodes by running:

```
$ cfy nodes list -d {{< param deployment_name >}}

Listing nodes for deployment {{< param deployment_name >}}...

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
**Tip**: To check out some more commands to use with the {{< param cfy_console_name >}}, run `cfy --help`

An even easier way to review your deployment is through the [{{< param cfy_console_name >}}](#validate).
Login to the console and browse to the **Deployments** page.
Select the deployment (`{{< param deployment_name >}}`) and explore the topology, inputs, outputs, nodes, and logs.

This is also a good time to examine the blueprint used in the example.
The blueprint can be examined in the {{< param cfy_console_name >}}, however in this case
we will go to the {{< param product_name >}} examples repository in Github and examine it there: [{{< param blueprint_name >}}](https://github.com/cloudify-community/blueprint-examples/blob/master/scaling-example/ansible.yaml)

### Scale

In order to scale the infrastructure, means to create more VM's, the scale workflow is being used.
execute:
`cfy executions start scale -d {{< param deployment_name >}} -p scalable_entity_name=vm-group -p delta=1`

Notice that another `install_eni_vm-playbook` node instance created, Check {{< param cloud >}} console to see the new VM created.

```
$ cfy nodes list -d {{< param deployment_name >}}

Listing nodes for deployment {{< param deployment_name >}}...

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

To remove the deployment and delete all resources from {{< param cloud >}} simply run the uninstall command:
```bash
cfy uninstall {{< param deployment_name >}}
```
