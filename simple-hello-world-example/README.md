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

This will run a `Hello World` web-server on your Cloudify Manager machine in port 8000 (it might take a minute or two for the web-server to run properly). 
To access it, simply open your browser to:

 * `http://127.0.0.1:8000` if you are using your local machine, or a docker container as the Cloudify Manager machine.
 * `http://<VM IP>:8000` if you are using a VM as the Cloudify Manager machine.
 * `http://<your Cloudify as a Service URL>:8000` if you are using Cloudify as a Service.

### Uninstall
To uninstall the web-server, simply run:

```bash
cfy uninstall simple-hello-world-example
```
