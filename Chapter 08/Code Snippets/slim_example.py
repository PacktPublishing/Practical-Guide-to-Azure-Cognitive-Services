from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential

endpoint = "https://<your_endpoint_name>.cognitiveservices.azure.com/"
credential = AzureKeyCredential("<your_key>")
form_recognizer_client = FormRecognizerClient(endpoint, credential)

with open(f'sample-invoice.jpg', "rb") as invoice:
    poller = form_recognizer_client.begin_recognize_invoices(invoice.read())

    for invoice in poller.result():
        for name, field in invoice.fields.items():
            if name == "Items":
                print("Invoice Items:")
                for idx, items in enumerate(field.value):
                    print("...Item #{}".format(idx+1))
                    for item_name, item in items.value.items():
                        print("......{}: {} has confidence {}".format(
                            item_name, item.value, item.confidence))
            else:
                print("{}: {} has confidence {}".format(
                    name, field.value, field.confidence))
