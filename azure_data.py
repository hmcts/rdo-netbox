"""This module extracts regions, subscriptions and prefixes from Azure"""
import itertools
import json
import os

from azure.identity import ClientSecretCredential
from azure.mgmt.resource import SubscriptionClient, ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient


class AzureVnets:
    """Azure vnets crawler."""

    def __init__(self, tenant_id=None, client_id=None, client_secret=None):
        tenant = tenant_id if tenant_id is not None else os.environ["AZURE_TENANT_ID"]
        client = client_id if client_id is not None else os.environ["AZURE_CLIENT_ID"]
        secret = client_secret if client_secret is not None else os.environ["AZURE_CLIENT_SECRET"]
        self.credentials = ClientSecretCredential(tenant_id=tenant, client_id=client, client_secret=secret)
        self.azure_subs = []
        self.regions = []
        self.subscriptions = []
        self.internal_prefixes = []
        self.propagated_prefixes = []

    def _pull_subscriptions(self):
        sub_client = SubscriptionClient(self.credentials)
        self.azure_subs = [sub.as_dict() for sub in sub_client.subscriptions.list()]
        self.subscriptions = [{"name": sub["display_name"]} for sub in self.azure_subs]

    def _pull_resource_groups(self):
        for sub in self.subscriptions:
            rg_client = ResourceManagementClient(self.credentials, sub["subscription_id"])
            azure_rgs = [rg.as_dict() for rg in rg_client.resource_groups.list()]
            rgs = [{"name": rg["name"]} for rg in azure_rgs]
            sub["resource_groups"] = rgs

    def _update_regions(self):
        unique_regions = set([pref["location"]["name"] for pref in self.internal_prefixes if pref["location"] is not None])
        self.regions = list(unique_regions)

    def _pull_prefixes(self):
        self._pull_subscriptions()
        # self._pull_resource_groups()
        for sub in self.azure_subs:
            net_client = NetworkManagementClient(self.credentials, sub["subscription_id"])
            az_vnets = [vnet.as_dict() for vnet in net_client.virtual_networks.list_all()]
            vnets = [
                {"id": v["id"], "name": v["name"], "location": v["location"],
                    "address_prefixes": v["address_space"]["address_prefixes"], "resource_group": v["id"].split("/")[4]}
                for v in az_vnets if v["address_space"] is not None
            ]
            for vnet in vnets:
                for cidr in vnet["address_prefixes"]:
                    self.internal_prefixes.append({
                        "prefix": cidr,
                        "location": {"name": vnet["location"]},
                        "subscription": {"name": sub["display_name"][:30]},
                        "custom_fields": {
                            "resource_group": vnet["resource_group"],
                            "vnet": vnet["name"]}
                    })
        self._update_regions()

    def _pull_propagated_prefixes(self):
        with open("static_data/effective_routes_resources.json", "r") as f:
            routes_resources = json.load(f)
        propagated_prefs = []
        for rr in routes_resources:
            net_client = NetworkManagementClient(
                self.credentials, subscription_id=rr["subscription"], api_version='2020-11-01')
            for res in rr["resources"]:
                routes = [
                    net_client.network_interfaces.begin_get_effective_route_table(
                        res["resource_group"], nic).result().as_dict() for nic in res["nics"]
                ]
                propagated_prefs.append([
                    {"prefix": j["address_prefix"][0],
                     "location": {"name": "external"},
                     "subscription": {"name": rr["subscription_name"][:30]},
                     "custom_fields": {
                         "resource_group": res["resource_group"],
                         "vnet": "external"}} for j in [
                        i for v in routes for i in v["value"] if v["value"] is not None
                    ]
                    if j["state"] == "Active"
                    and j["next_hop_type"] == "VirtualNetworkGateway"
                    and j["address_prefix"] is not None
                    and len(j["address_prefix"]) > 0]
                )
        self.propagated_prefixes = list(itertools.chain.from_iterable(propagated_prefs))

    @property
    def prefixes(self):
        return self.internal_prefixes + self.propagated_prefixes

    def load_data(self):
        self._pull_subscriptions()
        self._pull_prefixes()
        self._pull_propagated_prefixes()


if __name__ == "__main__":
    az_vnets = AzureVnets()
    az_vnets.load_data()
    print(len(az_vnets.prefixes))
    print(az_vnets.prefixes[0])
    print(az_vnets.prefixes[-1])
