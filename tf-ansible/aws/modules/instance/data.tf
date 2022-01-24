data "aws_ami" "centos" {
  most_recent = true
  owners      = ["125523088429"]

  filter {
    name   = "name"
    values = ["CentOS 7.9.2009 x86_64"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
