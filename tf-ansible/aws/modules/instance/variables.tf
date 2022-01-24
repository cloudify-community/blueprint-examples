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

variable "key_name" {
  type        = string
  description = "Name of the SSH key for admin user"
}

variable "instance_type" {
  type        = string
  description = "Instance type/size"
}

variable "subnet_id" {
  type        = string
  description = "ID of the subnet"
}

variable "security_group_id" {
  type        = string
  description = "ID of the security group"
}
