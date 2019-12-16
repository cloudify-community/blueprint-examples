# simple-python-webserver-blueprint

The blueprint installs a webserver on your local machine. It is supported on Linux and most *nix machines.


## Prerequisites

- [Cloudify CLI](http://docs.cloudify.co/4.3.0/installation/installing-cli/) installed on your computer.
- Your workstation's firewall should allow HTTP connections on port 8000.


## Usage

* Clone the repository

```bash
git clone https://github.com/cloudify-examples/local-simple-python-webserver-blueprint.git
cd local-simple-python-webserver-blueprint
```

* Install

```bash
cfy install blueprint.yaml
```

This will run a `Hello World` server on your local machine in port 8000.

```bash
Open your browser to http://localhost:8000
```

You will see the following in your browser:

![hwimage](/hello-world.png)


* Uninstall

```bash
cfy uninstall -b local-simple-python-webserver-blueprint
```
