module "redis" {
  source              = "git::https://github.com/hmcts/cnp-module-redis?ref=master"
  product             = var.product
  location            = var.location
  resource_group_name = azurerm_resource_group.netbox_rg.name
  env                 = var.environment
  common_tags         = module.tags.common_tags
  redis_version       = "6"
  business_area       = "sds"
  family              = "C"
  sku_name            = "Standard"
  maxmemory_reserved  = "125"
  maxmemory_delta     = "125"

  private_endpoint_enabled      = true
  public_network_access_enabled = false
}

resource "azurerm_key_vault_secret" "redis_hostname" {
  name         = "netbox-redis-hostname"
  value        = module.redis.host_name
  key_vault_id = azurerm_key_vault.netbox_key_vault.id
}

resource "azurerm_key_vault_secret" "redis_accesskey" {
  name         = "netbox-redis-accesskey"
  value        = module.redis.access_key
  key_vault_id = azurerm_key_vault.netbox_key_vault.id
}
resource "azurerm_key_vault_secret" "redis_port" {
  name         = "netbox-redis-port"
  value        = module.redis.redis_port
  key_vault_id = azurerm_key_vault.netbox_key_vault.id
}
