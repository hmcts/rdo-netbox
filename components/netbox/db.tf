module "postgresql_flexible" {
  providers = {
    azurerm.postgres_network = azurerm.postgres_network
  }

  source                        = "git::https://github.com/hmcts/terraform-module-postgresql-flexible?ref=master"
  env                           = var.environment
  resource_group_name           = azurerm_resource_group.netbox_rg.name
  product                       = var.product
  name                          = "${var.product}-v14-flexible"
  component                     = var.component
  business_area                 = "sds"
  location                      = var.location
  enable_read_only_group_access = false
  common_tags                   = module.tags.common_tags
  admin_user_object_id          = data.azurerm_client_config.current.object_id
  collation                     = var.collation
  pgsql_databases = [
    {
      name : "netbox"
    }
  ]

  pgsql_server_configuration = [
    {
      name  = "azure.extensions"
      value = "PG_BUFFERCACHE,PG_STAT_STATEMENTS,PLPGSQL"
    }
  ]

  pgsql_version = "14"
}
resource "azurerm_key_vault_secret" "POSTGRES-USER" {
  name         = "netbox-POSTGRES-USER-v14"
  value        = module.postgresql_flexible.username
  key_vault_id = azurerm_key_vault.netbox_key_vault.id
}

resource "azurerm_key_vault_secret" "POSTGRES-PASS" {
  name         = "netbox-POSTGRES-PASS-v14"
  value        = module.postgresql_flexible.password
  key_vault_id = azurerm_key_vault.netbox_key_vault.id
}

resource "azurerm_key_vault_secret" "POSTGRES-HOST" {
  name         = "netbox-POSTGRES-HOST-v14"
  value        = module.postgresql_flexible.fqdn
  key_vault_id = azurerm_key_vault.netbox_key_vault.id
}


resource "azurerm_key_vault_secret" "POSTGRES-DATABASE" {
  name         = "netbox-POSTGRES-DATABASE-v14"
  value        = "netbox"
  key_vault_id = azurerm_key_vault.netbox_key_vault.id
}

