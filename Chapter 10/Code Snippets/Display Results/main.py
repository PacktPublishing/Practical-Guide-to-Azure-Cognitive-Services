import base64
import json
from time import sleep
from azure.storage.queue import QueueServiceClient
from results.result import Result
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel

console = Console()

service = QueueServiceClient(
    account_url="https://ch10oceansmartst.queue.core.windows.net/",
    credential="j9VWym0gnUfsNyTGs0INAPk8m6mmqqt6ojHmdWHEW8LM3zVxyIRojVoLwJ0Hw8r+Y3lg++0guyBB+AStxU08eQ=="
)
client = service.get_queue_client("resultq")

table = Table(show_header=True, header_style="bold magenta", expand=True)
table.add_column("File Name")
table.add_column("Good")
table.add_column("Bad")
table.add_column("Result", justify="right")


with Live(console=console, screen=True, auto_refresh=False) as live:
    while True:
        messages = client.receive_messages()

        for message in messages:
            decodedBytes = json.loads(json.loads(str(base64.b64decode(message.content), "utf-8")))
            if Result.unique(decodedBytes['file_name']):
                new_row = Result(*list(str(val) for val in decodedBytes.values()))
                table.add_row(new_row.file_name, new_row.good, new_row.bad, str(new_row.passed()))

        # console.print(f"Total results: {len(Result)}")
        live.update(Panel(table), refresh=True)
        sleep(1)
