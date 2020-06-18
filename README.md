# rdo-netbox

NetBox is an IP address management (IPAM) and data center infrastructure
management (DCIM) tool. It is intended to function as a domain-specific source of truth for network operations.

HMCTS NetBox runs as a web application atop the Django Python framework
with a PostgreSQL database and a Redis Cache hosted in Azure
This Netbox module is used grab every network prefix in use in HMCTS Azure
and populates the Netbox instance and will serve as a single source of truth for
all things IPAM.

The complete documentation for NetBox can be found at [Confluence](https://tools.hmcts.net/confluence/display/RD/Netbox).
Questions? Comments? Please ask in the #devops Slack channel.



### Build Status

|             | status |
|-------------|------------|
| **master** | [![Build Status](https://dev.azure.com/hmcts/DevOps/_apis/build/status/hmcts.rdo-netbox?branchName=master)](https://dev.azure.com/hmcts/DevOps/_build?definitionId=345) |

The pipeline is set to run every day at 7AM so that data is always up to date, it is also good practice to manually run the pipeline after
you create a new vnet so Netbox can get updated.

### Quick start

Click [here](https://netbox.platform.hmcts.net) to access the instance. (You must be connected to the VPN and using the HMCTS proxy)

You can view currently assigned network prefixes and assign yourself an available prefix based on the data.

#### Curl commands

In order to make Restful calls to Netbox, you need to ensure you are connected to the VPN and be using the HMCTS proxy
to be able to reach the Netbox instance.

In order to GET a prefix to see if it exists, enter a command such as:
```bash
curl -X GET -k https://netbox.platform.hmcts.net:443/api/ipam/prefixes/?prefix=10.230.6.0%2F24 -H "accept: application/json" | jq .
```

To pull ALL prefixes, use:
```bash
curl -X GET -k https://netbox.platform.hmcts.net:443/api/ipam/prefixes/ -H "accept: application/json" | jq .
```

To find any prefixes within a prefix, use:
```bash
curl -X GET -k https://netbox.platform.hmcts.net:443/api/ipam/prefixes/?within=10.50.0.0%2F16 -H "accept: application/json" | jq .
```

To grab a prefix from a specific vnet name, use:
```bash
curl -X GET -k https://netbox.platform.hmcts.net:443/api/ipam/prefixes/?cf_vnet="datalake-rg-vnet" -H "accept: application/json" |
 jq .
```

To grab a list of Subscriptions, use:
```bash
curl -X GET -k https://netbox.platform.hmcts.net:443/api/tenancy/tenants/ -H "accept: application/json" | jq .
```

### Using the Pynetbox SDK

You can do more with the Netbox Python SDK such as make a call for the next available prefix.

#### Prereqs

1) In order to be able to use it, you will need to get in contact with the devops team in the #devops
channel to request a token to access the instance with `Pynetbox`.

2) Install Python3 and the [Pynetbox](https://pypi.org/project/pynetbox/) module.
   
#### Quick start

Ensure you have environmental variables for `NETBOX_TOKEN` and `NETBOX_URL`
```bash
export NETBOX_TOKEN=[token]
export NETBOX_URL=[url]
```

Create a python file with the below contents
```python
import pynetbox
import urllib3, os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


NETBOX_URL = os.environ.get("NETBOX_URL")
NETBOX_TOKEN = os.environ.get("NETBOX_TOKEN")

nb = pynetbox.api(f"http://{NETBOX_URL}", NETBOX_TOKEN, ssl_verify=False)
import ipdb; ipdb.set_trace()
```

To see what prefixes live under a specific range, you can use the `filter` verb like:
```python
ipdb> nb.ipam.prefixes.filter(q="10.99.50.0/24")                                                                                                                     
[10.99.0.0/18, 10.99.0.0/18, 10.99.0.0/18]
```

To get a specific prefix and to see what available child prefixes exist, run something like this:
```python
ipdb> nb.ipam.prefixes.get(prefix="172.16.7.0/24").available_prefixes.list()                                                                                         
[{'family': 4, 'prefix': '172.16.7.0/24', 'vrf': None}]
```

To filter on the name of the vnet or resource group, use:
```python
ipdb> nb.ipam.prefixes.filter(cf_resource_group="datalake-rg")
[172.16.7.0/24]

ipdb> nb.ipam.prefixes.filter(cf_vnet="datalake-rg-vnet")
[172.16.7.0/24]
```

