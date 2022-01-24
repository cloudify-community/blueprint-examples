variable "aws_access_key" {
  type        = string
  description = "Access key for AWS"
}

variable "aws_secret_key" {
  type        = string
  description = "Secret key for AWS"
}

variable "aws_region" {
  type        = string
  description = "AWS region to launch servers in"
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for AWS VPC"
}

variable "subnet_cidr" {
  type        = string
  description = "CIDR block for AWS Subnet"
}

variable "public_key" {
  type        = string
  description = "Public SSH key for admin user"
}
