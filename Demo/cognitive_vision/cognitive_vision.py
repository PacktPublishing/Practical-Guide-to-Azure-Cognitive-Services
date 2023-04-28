import base64
import json
import os

from azure.core.exceptions import HttpResponseError
from azure.storage.queue import QueueServiceClient
from azure.data.tables import TableServiceClient, TableClient


def poll() -> list:
    msg_list = list()

    queue = QueueServiceClient(
        account_url=str(os.getenv('AZURE_COG_VISION_QUEUE_ENDPOINT')),
        credential=str(os.getenv('AZURE_COG_VISION_CREDENTIAL'))
    )

    client = queue.get_queue_client("resultq")
    messages = client.receive_messages()

    for msg in messages:
        msg_list.append(json.loads(json.loads(str(base64.b64decode(msg['content']), "utf-8"))))
        client.delete_message(msg)

    with TableClient.from_connection_string(str(os.getenv('AZURE_COG_VISION_TABLE_CONN_STR')),
                                            str(os.getenv('AZURE_COG_VISION_TABLE_NAME'))) as table_client:
        try:
            queried_entities = table_client.list_entities()

            for entity_chosen in queried_entities:
                entity = table_client.get_entity(partition_key=entity_chosen["PartitionKey"],
                                                 row_key=entity_chosen["RowKey"])
                msg_list.append(json.loads(str(entity['result'])))
                table_client.delete_entity(row_key=entity_chosen["RowKey"], partition_key=entity_chosen["PartitionKey"])

        except HttpResponseError as e:
            print(e.message)

    return msg_list
