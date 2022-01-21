terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~>3.87"
    }
  }
}

provider "google" {
  credentials = var.credentials_json
  project     = var.project
}
