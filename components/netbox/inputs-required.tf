variable "environment" {
  type        = string
  description = "Environment to deploy to"
}
variable "project" {
  type        = string
  description = "Name of the project"
}
variable "product" {
  type        = string
  description = "Name of the product"
}

variable "subscription_id" {
  type        = string
  description = "subscription ID"
}
variable "aks_subscription_id" {
  type        = string
  description = "subscription ID"
}



variable "location" {
  type        = string
  default     = "UK South"
  description = "Azure Region"
}
variable "component" {
  type        = string
  default     = "netbox"
  description = "Name of the component"
}

variable "builtFrom" {
  type        = string
  description = "Name of the github repo source"
}

variable "env" {

}