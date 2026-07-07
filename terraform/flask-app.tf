resource "azurerm_public_ip" "flask_app" {
  name                = "flask-app-public-ip"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  allocation_method = "Static"
  sku               = "Standard"

  tags = local.common_tags
}

resource "azurerm_network_interface" "flask_app" {
  name                = "flask-app-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Static"
    private_ip_address            = "10.0.1.20"
    public_ip_address_id          = azurerm_public_ip.flask_app.id
  }

  tags = local.common_tags
}

resource "azurerm_linux_virtual_machine" "flask_app" {
  name                = "flask-app"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  size = "Standard_B2as_v2"

  admin_username = var.admin_username

  network_interface_ids = [
    azurerm_network_interface.flask_app.id
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = file(var.public_key_path)
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "ubuntu-24_04-lts"
    sku       = "server"
    version   = "latest"
  }

  disable_password_authentication = true

  tags = local.common_tags
}
