data "azurerm_subscription" "current" {}

data "azurerm_client_config" "current" {}

data "azuread_service_principal" "app_proxy_ga_service_connection" {
  display_name = "DTS Operations Bootstrap GA"
}
module "tags" {
  source       = "github.com/hmcts/terraform-module-common-tags?ref=master"
  builtFrom    = var.builtFrom
  environment  = var.environment
  product      = var.product
  expiresAfter = "3000-01-01"
}