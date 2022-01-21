# This can be generated with: jq -c . /path/to/gce-creds.json
variable "credentials_json" {
  type        = string
  description = "Contents of a GCP JSON credentials file"
}

variable "project" {
  type        = string
  description = "GCP project ID"
}

variable "admin_user" {
  type        = string
  description = "Admin user for the image we're launching"
}

variable "admin_key_public" {
  type        = string
  description = "Public SSH key of admin user"
}

variable "image" {
  type = object({
    project = string
    family  = string
  })
  default = {
    project = "centos-cloud"
    family  = "centos-7"
  }
}

variable "prefix" {
  type        = string
  description = "Resource name prefix"
  default     = "cfy"
}

variable "instance_type" {
  type        = string
  description = "VM instance_type"
}

variable "network" {
  type        = string
  description = "Network to connect instance to"
}

variable "region" {
  type        = string
  description = "Default region for GCP provider"
  default     = "us-west2"
}
