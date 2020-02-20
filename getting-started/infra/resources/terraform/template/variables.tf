variable "aws_region" {
  description = "AWS region to launch servers."
}

variable "admin_user" {
  description = "Admin user for the AMI we're launching"
}

variable "admin_key_public" {
  description = "Public SSH key of admin user"
}

variable "aws_amis" {
  default = {
    ca-central-1 = "ami-033e6106180a626d0"
  }
}
