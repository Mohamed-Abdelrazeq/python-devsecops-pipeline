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

output "ssh_command" {
  description = "SSH command to connect to the Jenkins VM"
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.jenkins.ip_address}"
}
