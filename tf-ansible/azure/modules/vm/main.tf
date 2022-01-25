# Generate a random suffix to suffix resources with
resource "random_id" "suffix" {
  byte_length = 4
}

resource "azurerm_public_ip" "example_ip" {
  name                    = "${var.prefix}-public-ip-${random_id.suffix.hex}"
  location                = var.location
  resource_group_name     = var.resource_group_name
  allocation_method       = "Dynamic"
  idle_timeout_in_minutes = 30
}

resource "azurerm_network_interface" "example_interface" {
  name                = "${var.prefix}-nic-${random_id.suffix.hex}"
  location            = var.location
  resource_group_name = var.resource_group_name

  ip_configuration {
    name                          = "${var.prefix}-internal-ip-${random_id.suffix.hex}"
    subnet_id                     = var.subnet
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.example_ip.id

  }
}

resource "azurerm_linux_virtual_machine" "example" {
  name                = "${var.prefix}-vm-${random_id.suffix.hex}"
  resource_group_name = var.resource_group_name
  location            = var.location
  size                = var.instance_type
  admin_username      = var.admin_user
  network_interface_ids = [
    azurerm_network_interface.example_interface.id,
  ]

  admin_ssh_key {
    username   = var.admin_user
    public_key = var.admin_key_public
  }

  os_disk {
    caching              = "None"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "OpenLogic"
    offer     = "CentOS"
    sku       = "7_9-gen2"
    version   = "latest"
  }
}
