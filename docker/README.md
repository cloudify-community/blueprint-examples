# Docker Examples

**NOTE** These examples assume that you have docker plugin already installed

This folder contains several Docker examples:


  * _ansible_: Two examples that shows how to use docker container to run ansible playbook in 2 ways one using the generic way and the other using the node_type that is similar to what our ansible plugin has.
  * _terraform_: Two examples that shows how to use docker container to run terraform in 2 ways one using the generic way and the other using the node_type that is similar to what our terraform plugin has.
  * _general_: Some generic examples on how to use the docker plugin.
  * _installation_: an example on how to install the docker on a host.


## Pre-installation steps

Upload the required plugins:

  * [Docker Plugin](https://github.com/cloudify-cosmo/cloudify-docker-plugin/releases) .
  * for terraform example you need git package installed on the manager VM, 
  execute:
  ```
yum install -y git
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
 * docker_user: username for ssh to the vm(centos/ubuntu)
 * ansible_host: ip of vm with Ubuntu image installed on it.
 * ansible_user: ubuntu

In order to sse that the example works:
 1. Go to  https://<ansible_host> and see the "hello world" site.
 2. look in docker_ansible_container node instance and see the "run_result" runtime property.
   
## general examples

For **any-container.yaml** example:

```shell 
cfy install any-container.yaml -i docker_host=<ip> -i docker_user=<username>
```
 **Inputs:**
 
 * docker_host: ip of vm with docker installed
 * docker_user: username for ssh to the vm(centos)

In order to sse that the example works look in docker_centos_container node instance and see the "run_result" runtime property.
   
## installation examples

For **install-docker** example:
```shell script
cfy install install-docker.yaml -i docker_host=<ip> -i docker_user=<username> 
```

**Inputs:**
 
 * docker_host: ip of vm that the docker will be installed on.
 * docker_user: username for ssh to the vm(centos/ubuntu)
 
 In order to see that the example works ssh to the docker_host and check that docker has been installed
(you can check docker has been installed by execute: `docker --version` )
 
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
 * docker_user: username for ssh to the vm(centos/ubuntu)
 
 In order to sse that the example works:
  1. You can enter your aws console and see that a VM was created.
  2. Look in docker_terraform_container node instance and see the "run_result" runtime property(check that terraform was installed).
