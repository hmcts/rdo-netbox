# rdo-netbox

NetBox is an IP address management (IPAM) and data center infrastructure
management (DCIM) tool. It is intended to function as a domain-specific source of truth for network operations.

HMCTS NetBox runs as a web application atop the Django Python framework
with a PostgreSQL database and a Redis Cache hosted in Azure
This Netbox module is used grab every network prefix in use in HMCTS Azure
and populates the Netbox instance and will serve as a single source of truth for
all things IPAM.

The complete documentation for NetBox can be found at [Confluence](https://tools.hmcts.net/confluence/display/RD/Netbox).
Questions? Comments? Please ask in the #devops Slack channel



### Build Status

|             | status |
|-------------|------------|
| **master** | [![Build Status](https://dev.azure.com/hmcts/DevOps/_apis/build/status/hmcts.rdo-netbox?branchName=master)](https://dev.azure.com/hmcts/DevOps/_build?definitionId=345) |
