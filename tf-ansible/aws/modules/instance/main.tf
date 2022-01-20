resource "aws_instance" "example_instance" {
  # The connection block tells our provisioner how to
  # communicate with the resource (instance)
  connection {
    # The default username for our AMI
    user = "centos"
  }

  key_name               = var.key_name
  instance_type          = var.instance_type
  ami                    = data.aws_ami.centos.image_id
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [var.security_group_id]

}

