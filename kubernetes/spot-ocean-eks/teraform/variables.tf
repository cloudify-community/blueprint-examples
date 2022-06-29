variable "spot_token" {
  type = string
  description = "Spot ocean accpunt token."
}

variable "spot_account" {
  type = string
  description = "Spot ocean account ID."
}

variable "eks_name" {
  type = string
  description = "AWS EKS cluster name"
}

variable "endpoint" {
  type = string
}

variable "token" {
  type = string
  description = "kube token"
}

variable "ca_cert" {
  type = string
}
