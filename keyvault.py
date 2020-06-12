"""This module obtains secrets from an Azure Keyvault"""
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError
from variables import Parser

class GetSecret():
    """This class is used to interact with Azure Key Vaults"""

    def __init__(self, secret_name, secret_value=''):
        """This function retrieves a secret from an Azure Key Vault"""
        self.secret_name = secret_name
        self.secret_value = secret_value
        Parser.parse_var(self)

        key_vault_name = self.args.KEY_VAULT_NAME
        kv_uri = f"https://{key_vault_name}.vault.azure.net"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=kv_uri, credential=credential)

        try:
            retrieved_secret = client.get_secret(self.secret_name)
        except ResourceNotFoundError:
            print("Key not found, please verify that the key names are correct")
            exit(0)
        else:
            self.secret_value = retrieved_secret.value
            