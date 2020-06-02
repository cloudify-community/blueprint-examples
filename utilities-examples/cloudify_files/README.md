# Cloudify Utilities: Files

The files utility allows you to package a file with a blueprint and move it onto a managed Cloudify Compute node.

##Examples

###example 1:

blueprint:[simple.yaml](./simple.yaml)

This example copies /resources/docker.repo file to a given path.

Specify the file_path(destination):

`cfy install simple.yaml -i file_path=<path>`
