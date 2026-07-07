output "resource_group_name" {
  description = "Azure Resource Group"
  value       = azurerm_resource_group.main.name
}

output "virtual_network_name" {
  description = "Virtual Network"
  value       = azurerm_virtual_network.main.name
}

output "subnet_name" {
  description = "Subnet"
  value       = azurerm_subnet.main.name
}

output "jenkins_public_ip" {
  description = "Public IP address of the Jenkins VM"
  value       = azurerm_public_ip.jenkins.ip_address
}

output "flask_public_ip" {
  description = "Public IP address of the Flask VM"
  value       = azurerm_public_ip.flask_app.ip_address
}

output "jenkins_private_ip" {
  description = "Private IP address of the Jenkins VM"
  value       = azurerm_network_interface.jenkins.private_ip_address
}

output "flask_private_ip" {
  description = "Private IP address of the Flask VM"
  value       = azurerm_network_interface.flask_app.private_ip_address
}

output "jenkins_ssh_command" {
  description = "SSH command to connect to the Jenkins VM"
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.jenkins.ip_address}"
}

output "flask_ssh_command" {
  description = "SSH command to connect to the Flask VM"
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.flask_app.ip_address}"
}
