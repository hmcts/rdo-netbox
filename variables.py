"""This module accepts pipeline variables and sets them as env variables"""
import argparse
import os

class Parser():
    def __init__(self):
        pass

    def parse_var(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--KEY_VAULT_NAME")
        parser.add_argument("--AZURE_CLIENT_ID")
        parser.add_argument("--AZURE_CLIENT_SECRET")
        parser.add_argument("--AZURE_TENANT_ID")
        parser.add_argument("--ENVIRONMENT")
        self.args = parser.parse_args()
        self.args.AZURE_CLIENT_ID = os.environ["AZURE_CLIENT_ID"]
        self.args.AZURE_CLIENT_SECRET = os.environ["AZURE_CLIENT_SECRET"]
        self.args.AZURE_TENANT_ID = os.environ["AZURE_TENANT_ID"]
        self.args.KEY_VAULT_NAME = os.environ["KEY_VAULT_NAME"]
        self.args.ENVIRONMENT = os.environ["ENVIRONMENT"]
