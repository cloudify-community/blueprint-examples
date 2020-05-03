# Docker Examples

**NOTE** These examples assume that you have docker plugin already installed

This folder contains several Docker examples:


  * _ansible_: Two examples that shows how to use docker container to run ansible playbook in 2 ways one using the generic way and the other using the node_type that is similar to what our ansible plugin has.
  * _terraform_: Two examples that shows how to use docker container to run terraform in 2 ways one using the generic way and the other using the node_type that is similar to what our terraform plugin has.
  * _general_: Some generic examples on how to use the docker plugin.
  * _docker-machine_: an example that will create a host on one of the public clouds and install docker on that host.
  * _installation_: an example on how to install the docker on a host.


## Pre-installation steps

Upload the required plugins:

  * [Docker Plugin](https://github.com/cloudify-cosmo/cloudify-docker-plugin/releases) .
  * for terraform example you need git package installed on the manager VM,
  execute depending on your host operating system:
  ```
yum install -y git || apt-get install -y git
```
## Creating secrets

Create secrets according to the example.

Replace <value> with actual values, without the <>

For **all examples**:

```shell
ssh-keygen -t rsa -C "your_email@example.com"
# [ENTER] [ENTER] [ENTER] [ENTER] [ENTER]
cfy secrets create agent_key_private -f ~/.ssh/id_rsa -u
cfy secrets create agent_key_public -f ~/.ssh/id_rsa.pub -u
```

For **Terraform examples**:
```shell
cfy secrets create aws_access_key_id --secret-string <value>
cfy secrets create aws_secret_access_key --secret-string <value>
```

### Running the examples


### ansible examples

For **ansible-container.yaml** example:
```shell
cfy install ansible-container.yaml -i docker_host=<ip> -i docker_user=<username> -i ansible_host=<ip> -i ansible_user=ubuntu
```
For **ansible-container-using-docker-ansible-playbook.yaml** example:
```shell script
cfy install ansible-container-using-docker-ansible-playbook.yaml -i docker_host=<ip> -i docker_user=<uername> -i ansible_host=<ip> -i ansible_user=ubuntu
```

 **Inputs:**(for two ansible examples)

 * docker_host: ip of vm with docker installed
 * docker_user: username for ssh to the vm (centos/ubuntu)
 * ansible_host: ip of vm with Ubuntu image installed on it.
 * ansible_user: ubuntu

In order to see that the example works:
 1. Go to  https://<ansible_host> and see the "hello world" site.
 2. you can check the container outputs : view docker_ansible_container node instance "run_result" runtime property.

## general examples

For **any-container.yaml** example:

```shell
cfy install any-container.yaml -i docker_host=<ip> -i docker_user=<username>
```
 **Inputs:**

 * docker_host: ip of vm with docker installed
 * docker_user: username for ssh to the vm (centos/ubuntu)

In order to check the container outputs : view docker_centos_container node instance "run_result" runtime property.

## installation examples

For **install-docker** example:
```shell script
cfy install install-docker.yaml -i docker_host=<ip> -i docker_user=<username>
```

**Inputs:**

 * docker_host: ip of vm that the docker will be installed on.
 * docker_user: username for ssh to the vm (centos/ubuntu)

 In order to check that the example worked you can ssh to the docker_host and check that docker has been installed
 and working correctly or you can check the docker API by access it on port 2375, for example you can use
 http://{public_ip_for_host}:2375/info

**NOTE** (you can check docker has been installed/working by executing: `docker --version` )

## terraform examples

For **terraform-container.yaml** example:

 ```shell script
cfy install terraform-container.yaml  -i docker_host=<ip> -i docker_user=<username>
```
 For **terraform-container-using-docker-terraform-module.yaml** example:
 ```shell script
cfy install terraform-container-using-docker-terraform-module.yaml   -i docker_host=<ip> -i docker_user=<username>

```

**Inputs:**(for two terraform examples)

 * docker_host: ip of vm with docker installed.
 * docker_user: username for ssh to the vm (centos/ubuntu)

 In order to see that the example works:
  1. You can enter your aws console and see that a VM was created.
  2. Look in docker_terraform_container node instance and view "run_result" runtime property (check terraform execution result).
