provider "kubernetes" {
  host                   =  var.endpoint
  token                  =  var.token
  cluster_ca_certificate = base64decode(var.ca_cert)
}

module "ocean-controller" {
  source = "spotinst/ocean-controller/spotinst"

  # Credentials.
  spotinst_token   = var.spot_token
  spotinst_account = var.spot_account

  # Configuration.
  cluster_identifier = var.eks_name
}

