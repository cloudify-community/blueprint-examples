output "security_group_id" {
  value = aws_security_group.example_security_group.id
}

output "subnet_id" {
  value = aws_subnet.example_subnet.id
}

output "key_name" {
  value = aws_key_pair.example_keypair.key_name
}
