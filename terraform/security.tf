# Jenkins NSG
resource "azurerm_network_security_group" "jenkins" {
  name                = "jenkins-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name      = "Allow-SSH"
    priority  = 100
    direction = "Inbound"
    access    = "Allow"
    protocol  = "Tcp"

    source_port_range      = "*"
    destination_port_range = "22"

    source_address_prefix      = var.allowed_ssh_ip
    destination_address_prefix = "*"
  }

  security_rule {
    name      = "Allow-Jenkins"
    priority  = 110
    direction = "Inbound"
    access    = "Allow"
    protocol  = "Tcp"

    source_port_range      = "*"
    destination_port_range = "8080"

    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = local.common_tags
}

# Flask NSG
resource "azurerm_network_security_group" "flask" {
  name                = "flask-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name      = "Allow-SSH"
    priority  = 100
    direction = "Inbound"
    access    = "Allow"
    protocol  = "Tcp"

    source_port_range      = "*"
    destination_port_range = "22"

    source_address_prefix      = var.allowed_ssh_ip
    destination_address_prefix = "*"
  }

  security_rule {
    name      = "Allow-SSH-From-Jenkins"
    priority  = 110
    direction = "Inbound"
    access    = "Allow"
    protocol  = "Tcp"

    source_port_range      = "*"
    destination_port_range = "22"

    source_address_prefix      = azurerm_network_interface.jenkins.private_ip_address
    destination_address_prefix = "*"
  }

  security_rule {
    name      = "Allow-Flask"
    priority  = 120
    direction = "Inbound"
    access    = "Allow"
    protocol  = "Tcp"

    source_port_range      = "*"
    destination_port_range = "5000"

    source_address_prefix      = var.allowed_ssh_ip
    destination_address_prefix = "*"
  }

  security_rule {
    name      = "Allow-Flask"
    priority  = 130
    direction = "Inbound"
    access    = "Allow"
    protocol  = "Tcp"

    source_port_range      = "*"
    destination_port_range = "5000"

    source_address_prefix      = azurerm_network_interface.jenkins.private_ip_address
    destination_address_prefix = "*"
  }

  tags = local.common_tags
}

#################################################
# NSG Associations
#################################################

resource "azurerm_network_interface_security_group_association" "jenkins" {
  network_interface_id      = azurerm_network_interface.jenkins.id
  network_security_group_id = azurerm_network_security_group.jenkins.id
}

resource "azurerm_network_interface_security_group_association" "flask" {
  network_interface_id      = azurerm_network_interface.flask_app.id
  network_security_group_id = azurerm_network_security_group.flask.id
}
