# AWS Example Network

This blueprint deploys an example network on AWS which is based on Amazon's [VPC Scenario 2](https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Scenario2.html). It is the classic network architecture, allowing a user to deploy both public-facing and private components.

### Resources Created

The install workflow will create the following resources in AWS:

  * `vpc`
  * `internet_gateway`
  * `public_subnet`
  * `private_subnet`
  * `public_subnet_routetable`
  * `private_subnet_routetable`
  * `route_public_subnet_internet_gateway`
  * `nat_gateway_ip`
  * `nat_gateway`
  * `route_private_subnet_nat_gateway`

## Compatibility

Tested with:
  * Cloudify 4.5.5


## Pre-installation steps

Upload the required plugins:

  * [AWS Plugin](https://github.com/cloudify-cosmo/cloudify-aws-plugin/releases) version 2.0.0, or higher.

You must have these secrets on your Cloudify Manager `tenant`:

  * `aws_access_key_id`: Your AWS credentials access key ID.
  * `aws_secret_access_key`: Your AWS credentials access key secret.
  * `region_name`: The EC2 region, for example `us-east-1`.
  * `ec2_region_endpoint`: The EC2 region service endpoint, for example `ec2.us-east-1.amazonaws.com`.
  * `availability_zone`: Your preferred availability zone in your EC2 region, such as `us-east-1c`.

**You may override the secrets' values via deployment inputs when you create the deployment.**


## Installation

1. On your Cloudify Manager, navigate to `Local Blueprints` and select `Upload`. [Right-click and copy URL](https://github.com/cloudify-community/blueprint-examples/archive/master.zip). Paste where it says `Enter blueprint url`. Provide a blueprint name, such as `aws-example-blueprint` in the field labeled `blueprint name`. Select `aws-example-network/blueprint.yaml` from `Blueprint filename` menu.

1. After the new blueprint has been created, click the `Deploy` button.

1. Navigate to `Deployments`, find your new deployment, select `Install` from the `workflow`'s menu. _Reminder, at this stage, you may provide your own values for any of the default `deployment inputs`._

#### Installation steps using the CLI:

```shell
cfy secrets create aws_secret_access_key -s .................
cfy secrets create aws_access_key_id -s .................
cfy secrets create region_name -s us-east-1
cfy secrets create ec2_region_endpoint -s us-east-1.amazonaws.com
cfy secrets create availability_zone -s us-east-1c
cfy blueprints upload https://github.com/cloudify-community/blueprint-examples/archive/master.zip -n aws-example-network/blueprint.yaml -b aws-example-network
cfy deployments create -b aws-example-network 
cfy executions start install -d aws-example-network
```

## Uninstallation

Navigate to the deployment and select `Uninstall`. When the uninstall workflow is finished, select `Delete deployment`.
