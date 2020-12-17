# Simple Hello-World Example

This blueprint installs a web-server on the Cloudify Manager machine. It is supported on Linux and most *nix machines.

## Prerequisites

- The Cloudify Manager machine's firewall should allow HTTP connections on port 8000.


## Usage
 
### Install 

- Upload this blueprint using the `Upload` button.
- Press the `Local Blueprints` tab and find the `Cloudify-Hello-World` blueprint. 
- Press the rocket shape icon to create a new deployment and give it a name, e.g. simple-hello-world-example.
- Press the `Deploy & Install` button to install the deployment. 
- Wait for the deployment installation to finish.

This will run a `Hello World` web-server on your Cloudify Manager machine in port 8000 (it might take a minute or two for the web-server to run properly). 
To access it, simply open your browser to:

 * `http://127.0.0.1:8000` if you are using your local machine, or a docker container as the Cloudify Manager machine.
 * `http://<VM IP>:8000` if you are using a VM as the Cloudify Manager machine.
 * `http://<your Cloudify as a Service URL>:8000` if you are using Cloudify as a Service.

### Uninstall
To uninstall the web-server:

- Press the `Deployments` tab and find the simple-hello-world-example deployment.
- Press the hamburger button, and in the opened menu press `Uninstall`.
