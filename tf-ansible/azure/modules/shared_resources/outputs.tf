output "location" {
  value = azurerm_resource_group.example_rg.location
}

output "resource_group_name" {
  value = azurerm_resource_group.example_rg.name
}

output "subnet" {
  value = azurerm_subnet.example_subnet.id
}
