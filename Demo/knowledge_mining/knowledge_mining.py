import json
import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient


def search_index(query: str) -> list:
    endpoint = str(os.getenv('AZURE_COG_SEARCH_ENDPOINT'))
    credential = AzureKeyCredential(str(os.getenv('AZURE_COG_SEARCH_CREDENTIAL')))
    index_name = os.getenv('AZURE_COG_SEARCH_INDEX')

    returned_list = list()
    client = SearchClient(endpoint=endpoint,
                          index_name=index_name,
                          credential=credential)
    results = client.search(search_text=query)

    for result in results:
        returned_list.append(result)

    return returned_list


def view_result(result_key: str) -> dict:
    endpoint = str(os.getenv('AZURE_COG_SEARCH_ENDPOINT'))
    credential = AzureKeyCredential(str(os.getenv('AZURE_COG_SEARCH_CREDENTIAL')))
    index_name = os.getenv('AZURE_COG_SEARCH_INDEX')
    client = SearchClient(endpoint=endpoint,
                          index_name=index_name,
                          credential=credential)
    result = dict()

    result = client.get_document(key=result_key)

    return result
