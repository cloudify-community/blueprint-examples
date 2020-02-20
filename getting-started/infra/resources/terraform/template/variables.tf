variable "aws_region" {
  type = string
  description = "AWS region to launch servers."
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
  }
}
