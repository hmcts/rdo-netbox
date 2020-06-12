"""This module populates Netbox with regions, subscriptions and prefixes from Azure"""
import pynetbox
from colorama import Fore, Style
from azure_data import prefixes, subscriptions, regions
from keyvault import GetSecret
from variables import Parser

class Netbox():
    """This class is used to interact with Netbox"""

    def __init__(self):
        """Initializes the Netbox class"""

        Parser.parse_var(self)
        self.url = GetSecret(f"{self.args.ENVIRONMENT}-netbox-url").secret_value
        self.token = GetSecret(f"{self.args.ENVIRONMENT}-netbox-token").secret_value
        self.nb = pynetbox.api(f"https://{self.url}", {self.token}, ssl_verify=False)

        Netbox.create_site(self)
        Netbox.create_subscriptions(self)
        Netbox.create_prefixes(self)

    def create_site(self):
        """Creates sites in Netbox, e.g uksouth.
        Data is pulled in from Azure"""

        for site in regions:
            if not self.nb.dcim.sites.get(name=site):
                self.nb.dcim.sites.create(
                    name=site,
                    slug=site)

    def create_subscriptions(self):
        """Creates Subscriptions in Netbox
        Data is pulled in from Azure"""

        for sub in subscriptions:
            if not self.nb.tenancy.tenants.get(name=sub):
                self.nb.tenancy.tenants.create(
                    name=sub,
                    slug=sub)

    def create_prefixes(self):
        """Creates and updates prefixes in Netbox
        Data is pulled in from Azure"""


        for item in self.nb.ipam.prefixes.all():
            item.delete()

        for prefix in prefixes:
            if not prefix["prefix"] in str(self.nb.ipam.prefixes.all()):
                self.nb.ipam.prefixes.create(
                    prefix=prefix["prefix"],
                    site=prefix["location"],
                    tenant=prefix["subscription"],
                    custom_fields=prefix["custom_fields"])
                print(f"{Fore.GREEN}Added to Netbox:")
                print(f"{Style.RESET_ALL}Subscription: {prefix['subscription']['name']}")
                print(f"Resource Group: {prefix['custom_fields']['resource_group']}")
                print(f"Vnet: {prefix['custom_fields']['vnet']}")
                print(f"Prefix: {prefix['prefix']}\n")
            else:
                if len(self.nb.ipam.prefixes.filter(prefix=prefix["prefix"])) > 1:
                    for item in self.nb.ipam.prefixes.filter(prefix=prefix["prefix"]):
                        if prefix["custom_fields"] == item.custom_fields:
                            item.update(prefix)
                else:
                    if not prefix["custom_fields"] == self.nb.ipam.prefixes.get(
                                                        prefix=prefix["prefix"]).custom_fields:
                        self.nb.ipam.prefixes.create(
                            prefix=prefix["prefix"],
                            site=prefix["location"],
                            tenant=prefix["subscription"],
                            custom_fields=prefix["custom_fields"])
                        print(f"{Fore.YELLOW}Added to Netbox (Overlap):")
                        print(f"{Style.RESET_ALL}Subscription: {prefix['subscription']['name']}")
                        print(f"Resource Group: {prefix['custom_fields']['resource_group']}")
                        print(f"Vnet: {prefix['custom_fields']['vnet']}")
                        print(f"Prefix: {prefix['prefix']}\n")
                    else:
                        self.nb.ipam.prefixes.get(prefix=prefix["prefix"]).update(prefix)

if __name__ == "__main__":
    Netbox()
