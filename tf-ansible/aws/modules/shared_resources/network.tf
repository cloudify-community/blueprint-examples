# Create a VPC
resource "aws_vpc" "example_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
}

# Create a subnet to launch our instances into
resource "aws_subnet" "example_subnet" {
  vpc_id                  = aws_vpc.example_vpc.id
  cidr_block              = var.subnet_cidr
  map_public_ip_on_launch = true
}

# Create an Internet gateway and associate with the default route table
resource "aws_internet_gateway" "example_gateway" {
  vpc_id = aws_vpc.example_vpc.id
}

resource "aws_route" "example_default_route" {
  route_table_id         = aws_vpc.example_vpc.default_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.example_gateway.id
}

# Security group for our application.
resource "aws_security_group" "example_security_group" {
  description = "Security group for example application"
  vpc_id      = aws_vpc.example_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound internet access
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
