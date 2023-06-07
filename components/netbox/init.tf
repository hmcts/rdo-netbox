terraform {
  required_version = ">=1.4.6"
  backend "azurerm" {
    /* subscription_id = "04d27a32-7a07-48b3-95b8-3c8691e1a263" */
  }
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.59.0"
    }
  }
}

provider "azurerm" {
  features {}

  subscription_id            = var.subscription_id
  skip_provider_registration = "true"

}

provider "azurerm" {
  features {}
  skip_provider_registration = true
  alias                      = "postgres_network"
  subscription_id            = var.aks_subscription_id
}