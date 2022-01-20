# Keypair used by EC2 instances
resource "aws_key_pair" "example_keypair" {
  public_key = var.public_key
}
