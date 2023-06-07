data "azurerm_subscription" "current" {}

data "azurerm_client_config" "current" {}

module "tags" {
  source      = "github.com/hmcts/terraform-module-common-tags?ref=master"
  builtFrom   = "hmcts/terraform-module-postgresql-flexible"
  environment = var.environment
  product     = "sds-platform"
}