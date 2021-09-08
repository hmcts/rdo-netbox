"""This module populates Netbox with regions, subscriptions and prefixes from Azure"""
import pynetbox
import requests
from colorama import Fore, Style
import azure_data
from keyvault import GetSecret
from variables import Parser
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Netbox:
    """This class is used to interact with Netbox"""

    def __init__(self):
        """Initializes the Netbox class"""

        Parser.parse_var(self)
        self.url = GetSecret("netbox-url").secret_value
        self.token = GetSecret("netbox-token").secret_value
        self.nb = pynetbox.api(f"https://{self.url}", self.token)
        # Disable SSL Verification
        session = requests.Session()
        session.verify = False
        self.nb.http_session = session
        self.az_data = azure_data.AzureVnets()

    # def create_tags(self):
    #     """Creates tags in Netbox, e.g owner.
    #     Data is pulled in from Azure"""

    #     if not self.nb.extras.tags.get(name='azure'):
    #         self.nb.extras.tags.create(name='azure',
    #                                    slug= 'azure')

    def create_site(self):
        """Creates sites in Netbox, e.g uksouth.
        Data is pulled in from Azure"""

        for site in self.az_data.regions:
            if not self.nb.dcim.sites.get(name=site):
                self.nb.dcim.sites.create(
                    name=site,
                    slug=site)

    def create_subscriptions(self):
        """Creates Subscriptions in Netbox
        Data is pulled in from Azure"""

        for sub in self.az_data.subscriptions:
            if not self.nb.tenancy.tenants.get(name=sub['name']):
                self.nb.tenancy.tenants.create(
                    name=sub['name'],
                    slug=sub['name'],
                    description=sub['description'])

    def get_prefixes(self):
        """Checks if prefixes need to be added or
        removed from Netbox
        Data is pulled in from Azure"""
        nb_prefixes = [p.prefix for p in self.nb.ipam.prefixes.all() if p is not None]
        for self.prefix in self.az_data.prefixes:
            if not self.prefix["prefix"] in nb_prefixes:
                Netbox.add_prefixes(self, "GREEN")
            else:
                prefix_space = self.nb.ipam.prefixes.filter(prefix=self.prefix["prefix"])
                found_pref = False
                for pref in prefix_space:
                    print(self.prefix["custom_fields"])
                    if self.prefix["custom_fields"] == pref.custom_fields:
                        found_pref = True
                        break
                if not found_pref:
                    Netbox.add_prefixes(self, "YELLOW")

    def add_prefixes(self, code):
        """Creates and updates prefixes in Netbox
        Data is pulled in from Azure"""

        map_values = {
            "GREEN": "Added to Netbox:",
            "YELLOW": "Added to Netbox (IP overlap):",
        }

        colour = getattr(Fore, code)
        self.nb.ipam.prefixes.create(
            prefix=self.prefix["prefix"],
            site=self.prefix["location"],
            tenant=self.prefix["subscription"],
            # tags=self.prefix["tags"],
            custom_fields=self.prefix["custom_fields"])

        print(f"{colour}{map_values[code]}")
        print(f"{Style.RESET_ALL}Prefix: {self.prefix['prefix']}")
        print(f"Subscription: {self.prefix['subscription']['name']}")
        print(
            f"Resource Group: {self.prefix['custom_fields']['resource_group']}")
        print(f"Virtual Network: {self.prefix['custom_fields']['vnet']}\n")

    def remove_prefixes(self):
        """Removes prefixes in Netbox"""

        delete = []
        for item in self.nb.ipam.prefixes.all():
            delete.append(item)
            for self.prefix in self.az_data.prefixes:
                if item.custom_fields == self.prefix["custom_fields"]:
                    if delete.__contains__(item):
                        delete.remove(item)
        for item in delete:
            item.delete()

            print(f"{Fore.RED}Removed from Netbox:")
            print(f"{Style.RESET_ALL}Prefix: {item}")
            print(f"Subscription: {item.tenant}")
            print(f"Resource Group: {item.custom_fields['resource_group']}")
            print(f"Virtual Network: {item.custom_fields['vnet']}\n")


if __name__ == "__main__":
    netbox = Netbox()
    netbox.az_data.load_data()
    netbox.create_site()
    netbox.create_subscriptions()
    netbox.get_prefixes()
    netbox.remove_prefixes()
