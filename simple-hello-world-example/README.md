# Simple Hello-World Example

This blueprint installs a web-server on the Cloudify Manager machine. It is supported on Linux and most *nix machines.


## Prerequisites

- [Cloudify CLI](https://docs.cloudify.co/latest/install_maintain/installation/installing-cli/) installed on your computer. It is used to run commands on the Cloudify Manager.
- The Cloudify Manager machine's firewall should allow HTTP connections on port 8000.


## Usage
 
### Install 

The `cfy install <blueprint-path>` command will upload the blueprint to your Cloudify Manager, create a deployment out of it, and install the created deployment. 

```bash
cfy install https://github.com/cloudify-community/blueprint-examples/releases/download/latest/simple-hello-world-example.zip
```

This will run a `Hello World` web-server on your Cloudify Manager machine in port 8000. To access it, simply open your browser to:

 * `http://localhost:8000` if you are using your local machine as the Cloudify Manager machine.
 * `http://<VM or container IP>:8000` if you are using a VM, or a docker container as the Cloudify Manager machine.

### Uninstall
To uninstall the web-server, simply run:

```bash
cfy uninstall simple-hello-world-example
```
