"""This module extracts regions, subscriptins and prefixes from Azure"""
import json

FILENAME = "address_prefixes.json"

with open(FILENAME, "r") as r:
    data = json.load(r)

prefixes = []
subscriptions = []
regions = []

for element in data:
    for cidr in element["Network"]:
        prefixes.append({"prefix": cidr,
                         "location": {"name": element["Location"]},
                         "subscription": {"name": element["ID"]},
                         "custom_fields":{
                             "resource_group": element["ResourceGroup"],
                             "vnet": element["Name"]}
                        })
        if not element["ID"] in subscriptions:
            subscriptions.append(element["ID"])

        if not element["Location"] in regions:
            regions.append(element["Location"])
