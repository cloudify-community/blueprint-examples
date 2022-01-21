# This can be generated with: jq -c . /path/to/gce-creds.json
variable "credentials_json" {
  type        = string
  description = "Contents of a GCP JSON credentials file"
}

variable "project" {
  type        = string
  description = "GCP project ID"
}

variable "prefix" {
  type        = string
  description = "Resource name prefix"
  default     = "cfy"
}

variable "region" {
  type        = string
  description = "Default region for GCP provider"
  default     = "us-west2"
}
