module "postgresql_flexible" {
  providers = {
    azurerm.postgres_network = azurerm.postgres_network
  }

  source        = "git::https://github.com/hmcts/terraform-module-postgresql-flexible?ref=master"
  env           = var.environment
  product       = var.product
  name          = "${var.product}-v14-flexible"
  component     = var.component
  business_area = "sds"
  location      = var.location

  common_tags          = module.tags.common_tags
  admin_user_object_id = azurerm_client_config.current.object_id
  pgsql_databases = [
    {
      name : "netbox"
    }
  ]

  pgsql_version = "14"
}
resource "azurerm_key_vault_secret" "POSTGRES-USER" {
  name         = "netbox-POSTGRES-USER"
  value        = module.postgresql_flexible.username
  key_vault_id = azurerm_key_vault.netbox_key_vault.id
}

resource "azurerm_key_vault_secret" "POSTGRES-PASS" {
  name         = "netbox-POSTGRES-PASS"
  value        = module.postgresql_flexible.password
  key_vault_id = azurerm_key_vault.netbox_key_vault.id
}

resource "azurerm_key_vault_secret" "POSTGRES_HOST" {
  name         = "netbox-POSTGRES-HOST"
  value        = module.postgresql_flexible.fqdn
  key_vault_id = azurerm_key_vault.netbox_key_vault.id
}


resource "azurerm_key_vault_secret" "POSTGRES_DATABASE" {
  name         = "netbox-POSTGRES-DATABASE"
  value        = "netbox"
  key_vault_id = azurerm_key_vault.netbox_key_vault.id
}

