"""This module extracts regions, subscriptins and prefixes from Azure"""
import json

FILENAME = "address_prefixes.json"

with open(FILENAME, "r") as r:
    data = json.load(r)

SUBS = "subs.json"

with open(SUBS, "r") as r:
    subs_data = json.load(r)

prefixes = []
subscriptions = []
regions = []

[regions.append(element["Location"]) for element in data if not element["Location"] in regions]
[subscriptions.append({"name": element["Name"][:30],
                       "description": element["Name"]})
                       for element in subs_data if not element["Name"] in subscriptions]

for element in data:
    for cidr in element["Network"]:
        prefixes.append({"prefix": cidr,
                         "location": {"name": element["Location"]},
                         "subscription": {"name": element["ID"][:30]},
                         "custom_fields":{
                             "resource_group": element["ResourceGroup"],
                             "vnet": element["Name"]}
                        })