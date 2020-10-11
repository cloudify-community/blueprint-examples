# Terraform-Ansible example.

This example porpose is to demonstrate cloudify Orchestrator of Orchestrators approach.

This blueprint creates infrastructure on AWS using Terraform, then runs ansible playbook that installs NGINX on the created infrastructue.


## Requirements

If you have already ensured these requirements are met, skip to [installation steps](#installation-steps).

- [ ] You will need a Cloudify Manager v5.0.5 or higher. See [install Cloudify Manager](#install-cloudify-manager-with-docker).

- [ ] You must install the following plugins on your Cloudify Manager.

    - [ ] `cloudify-utilites-plugin`, version 1.22.1 or higher, see [releases](https://github.com/cloudify-incubator/cloudify-utilities-plugin/releases).
    - [ ] `cloudify-terraform-plugin`, version 0.14.0 or higher, see [releases](https://github.com/cloudify-cosmo/cloudify-terraform-plugin/releases).
    - [ ] `cloudify-ansible-plugin`, see [releases](https://github.com/cloudify-cosmo/cloudify-ansible-plugin/releases).

To learn how to upload plugins, see [uploading plugins](#how-to-upload-plugins).

- [ ] You must create the following secrets, please create [required AWS secrets](#aws-secrets-checklist).


To learn how to create secrets, see [creating secrets](#how-to-create-secrets).

## Installation steps

First you will need to make sure that you have the latest terraform-ansible blueprint. These are located at [Blueprint Examples Releases](https://github.com/cloudify-community/blueprint-examples/releases). Look for the zip archive with the example name. Copy the link URL. You will need it to complete these steps.


#### Install the example with the CLI

Upload the blueprint to your Cloudify Manager with the following command:

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


# Appendix

### Install Cloudify Manager with Docker

If you have Docker, you can install a Cloudify Manager with the following command:

```shell
sudo docker run --name cfy_manager_local -d --restart unless-stopped -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --security-opt seccomp:unconfined --cap-add SYS_ADMIN -p 80:80 -p 8000:8000 cloudifyplatform/premium-cloudify-manager-aio:latest

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
  
If you need help locating your credentials, read about [AWS Access Key](https://aws.amazon.com/blogs/security/wheres-my-secret-access-key/).

[Return to requirements](#requirements).




