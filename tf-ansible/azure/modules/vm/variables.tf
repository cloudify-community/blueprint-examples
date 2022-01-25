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

variable "client_id" {
  type        = string
  description = "Azure Client ID used for authentication"
}

variable "client_secret" {
  type        = string
  description = "Azure Client Secret used for authentication"
}

variable "subscription_id" {
  type        = string
  description = "Azure Subscription ID used for authentication"
}

variable "tenant_id" {
  type        = string
  description = "Azure Tenant ID used for authentication"
}
