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
