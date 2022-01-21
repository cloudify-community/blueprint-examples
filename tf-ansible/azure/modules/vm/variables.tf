variable "resource_group_name" {
  type        = string
  description = "Name of resource group to deploy instance into"
}

variable "location" {
  type        = string
  description = "Azure location to deploy instance into"
}

variable "subnet" {
  type        = string
  description = "Subnet to deploy instance into"
}

variable "prefix" {
  type        = string
  description = "Prefix to place before deployed resources"
  default     = "cfy"
}

variable "admin_user" {
  type        = string
  description = "Admin user for the image we're launching"
}

variable "admin_key_public" {
  type        = string
  description = "Public SSH key of admin user"
}

variable "instance_type" {
  type        = string
  description = "Instance type/size to deploy"
  default     = "Standard_B1s"
}
