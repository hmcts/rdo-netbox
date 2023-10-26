#--------------------------------------------------------------
# Netbox - Resource Group
#--------------------------------------------------------------

resource "azurerm_resource_group" "netbox_rg" {
  name     = "netbox-${var.environment}-rg"
  location = var.location

  tags = module.tags.common_tags
}

#--------------------------------------------------------------
# Netbox - Key Vault
#--------------------------------------------------------------

resource "azurerm_key_vault" "netbox_key_vault" {
  name                = "netbox-vault-${var.environment}"
  location            = var.location
  resource_group_name = azurerm_resource_group.netbox_rg.name
  tenant_id           = data.azurerm_subscription.current.tenant_id

  sku_name = "standard"

  tags = module.tags.common_tags
}

resource "azurerm_role_assignment" "app-proxy-ga-service-connection-secret-management" {
  scope                = azurerm_key_vault.netbox_key_vault.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azuread_service_principal.app_proxy_ga_service_connection.object_id
}
