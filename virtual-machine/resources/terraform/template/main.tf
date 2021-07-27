# Specify the provider and access details
provider "aws" {
  region = var.aws_region
  access_key = var.access_key
  secret_key = var.secret_key
}

module "network" {
  source = "./modules/network"
}

variable "filename" {
  default = "cloud-config.cfg"
}

data "template_file" "template" {
  template = <<EOF
#cloud-config
users:
  - name: $${admin_user}
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    ssh-authorized-keys:
      - $${admin_key_public}
EOF
  vars = {
    admin_user = var.admin_user
    admin_key_public = var.admin_key_public
  }
}

resource "aws_instance" "example_vm" {
  # The connection block tells our provisioner how to
  # communicate with the resource (instance)
  connection {
    # The default username for our AMI
    user = var.admin_user
  }

  instance_type = "t2.micro"

  tags = {
    Name = "example-vm"
  }

  # Lookup the correct AMI based on the region
  # we specified
  ami = lookup(var.aws_amis, var.aws_region)

  # Our Security group to allow HTTP and SSH access
  vpc_security_group_ids = [network.example_security_group.id]

  # Connect to subnet
  subnet_id = network.example_subnet.id

  user_data =   data.template_file.template.rendered
}

resource "aws_eip" "eip" {
  instance = aws_instance.example_vm.id
  vpc      = true
}

output "instance_ip_addr" {
  value = aws_instance.server.private_ip
}