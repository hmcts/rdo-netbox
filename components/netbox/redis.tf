module "redis" {
  source        = "git@github.com:hmcts/cnp-module-redis?ref=add-redis-version-flag"
  product       = var.product
  location      = var.location
  env           = var.environment
  common_tags   = module.tags.common_tags
  redis_version = "6"
  business_area = "sds"
  family        = "C"
  sku_name      = "Basic"

  private_endpoint_enabled      = false
  public_network_access_enabled = false
}