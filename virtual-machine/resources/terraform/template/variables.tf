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
    ca-central-1 = "ami-033e6106180a626d0"
    us-east-1 = "ami-03248a0341eadb1f1"
    us-west-1 = "ami-01dd5a8ef26e6341d"
    us-west-2 = "ami-024b56adf74074ca6"
    eu-west-1 = "ami-0eee6eb870dc1cefa"
  }
}
