import os
from storages.backends.azure_storage import AzureStorage

EXPIRATION_SECS = 1880


class StaticAzureStorage(AzureStorage):
    account_name = os.getenv('AZURE_ACCOUNT_NAME')
    account_key = os.getenv('AZURE_ACCOUNT_KEY')
    azure_container = os.getenv('AZURE_STATIC_CONTAINER')
    expiration_secs = EXPIRATION_SECS


class MediaAzureStorage(AzureStorage):
    account_name = os.getenv('AZURE_ACCOUNT_NAME')
    account_key = os.getenv('AZURE_ACCOUNT_KEY')
    azure_container = os.getenv('AZURE_MEDIA_CONTAINER')
    expiration_secs = EXPIRATION_SECS
