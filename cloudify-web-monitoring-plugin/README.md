cloudify-web-monitoring-plugin
===================


# Description

A Cloudify Plugin that monitor a URL response time and based on metrics will trigger scale up or down

Basic contifuration includes what to monitor (URL), thresholds, limits and how to perform the scaling. Please see node type description below for details

## Node types

### cloudify.nodes.monitoring.Monitor - implements monitoring logic
#### Properties
- deployment_id - Deployment ID to execute scale workflow for
- scalable_entity_name - scaling group or node id that will be scaled by scale workflow. This should be defined in the blueprint used for target deployment defined in deployment_id
- delta - scaling step (number of instances to add or remove during a single scaling workflow execution)
- url - URL to monitor the response time for
- low_threshold - url response miliseconds threshold below which a scale down will be triggered (if there is more than 1 instance)
- high_threshold - url response miliseconds threshold above which a scale up will be triggered (if the scaleout_limit is not reached)
- scaleup_cooldown - minutes to wait in between scaleups
- scaledown_cooldown - minutes to wait in between scaledowns
- interval - minutes URL monitoring interval. The workflow that performs URL check will be scheduled with this rate
- scaleout_limit - maximum number of scale out workflows to execute in a sequence e.g. when scale out is called a counter is incremented and compared to this value. When scale down is called the counter is decremented
- client - optional Cloudfiy REST configuration

## Building the plugin

In order to build the plugin you need to have wagon installed on a virtual environment

```
wagon create -r dev-requirements.txt --build-tag "centos-Core" -v -f .
```

or you can use Cloudify wagon builder Docker images

```
docker run -v {path_to_plugin}/:/packaging cloudifyplatform/cloudify-centos-7-py3-wagon-builder
```


## Installing the plugin

In order to upload the plugin you can do that through Cloudify console or through cli

```
cfy plugin upload -y plugin.yaml cloudify_web_monitoring_plugin-1.0-centos-Core-py36-none-linux_x86_64.wgn
```

## Example

check blueprints sub-directory for the example
