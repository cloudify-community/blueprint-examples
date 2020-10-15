variable "aws_region" {
  type = string
  description = "AWS region to launch servers."
}

variable "aws_zone" {
  type = string
  description = "AWS zone to create subnet."
}

variable "admin_user" {
  type = string
  description = "Admin user for the AMI we're launching"
}

variable "admin_key_public" {
  type = string
  description = "Public SSH key of admin user"
}

variable "access_key" {
  type = string
  description = "Access key for AWS"
}

variable "secret_key" {
  type = string
  description = "Secret key for AWS"
}

variable "aws_amis" {
  type = map(string)
  default = {
    ca-central-1 = "ami-2e00bf4a"
    us-east-1 = "ami-841f46ff"
    us-west-1 = "ami-b2527ad2"
    us-west-2 = "ami-718c6909"
    eu-west-1 = "ami-1e749f67"
  }
}
