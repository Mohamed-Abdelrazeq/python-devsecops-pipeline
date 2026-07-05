variable "location" {
  description = "Azure region"
  type        = string
}

variable "resource_group_name" {
  description = "Resource Group name"
  type        = string
}

variable "network_name" {
  description = "Virtual Network name"
  type        = string
}

variable "subnet_name" {
  description = "Subnet name"
  type        = string
}

variable "network_security_group_name" {
  description = "Network Security Group name"
  type        = string
}

variable "public_ip_name" {
  description = "Public IP name"
  type        = string
}

variable "network_interface_name" {
  description = "Network Interface name"
  type        = string
}

variable "vm_name" {
  description = "Virtual Machine name"
  type        = string
}

variable "admin_username" {
  description = "VM administrator username"
  type        = string
}

variable "public_key_path" {
  description = "Path to the SSH public key"
  type        = string
}

variable "allowed_ssh_ip" {
  description = "Public IP allowed to SSH into the VM"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}
