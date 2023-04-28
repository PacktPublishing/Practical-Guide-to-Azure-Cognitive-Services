import os
import pathlib
import requests
from PyPDF2.errors import PdfReadError
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from caseconverter import snakecase
from PyPDF2 import PdfFileReader

from .models import Invoice, InvoiceItems, ScanInvoice

form_recognizer_client = DocumentAnalysisClient(
    endpoint=str(os.getenv('AZURE_ACCOUNT_NAME')),
    credential=AzureKeyCredential(str(os.getenv('AZURE_ACCOUNT_NAME')))
    )


def process_page(document: object, pages: int = None) -> object:
    if pages:
        pages = f"1-{pages}"
    poller = form_recognizer_client.begin_analyze_document(
        "prebuilt-invoice",
        document=document,
        pages=pages
        )
    result = poller.result()
    invoice_details = dict()
    item_list = list()
    for idx, invoice in enumerate(result.documents):
        for name, field in invoice.fields.items():
            if name == "Items":
                for items in field.value:
                    item_details = dict()
                    for item_name, item in items.value.items():
                        item_details[str(
                            snakecase(item_name))] = item.value
                    item_list.append(item_details)
            else:
                invoice_details[str(snakecase(name))] = field.value
    return invoice_details, item_list


def analyze(instance: ScanInvoice):
    try:
        invoice = Invoice()
        r = requests.get(instance.uploaded_file.url)
        file_extension = pathlib.Path(instance.filename()).suffix
        if 'pdf' in file_extension.lower():
            with open(instance.filename(), 'wb') as f:
                f.write(r.content)
                f.close()
            with open(instance.filename(), 'rb') as f:
                pages = int(PdfFileReader(f).getNumPages())
            with open(instance.filename(), 'rb') as f:
                completed_invoice, completed_items = process_page(
                    f.read(),
                    pages
                    )
        else:
            with open(instance.filename(), 'wb') as f:
                f.write(r.content)
                f.close()
            with open(instance.filename(), 'rb') as f:
                completed_invoice, completed_items = process_page(f.read())

        for attr, value in completed_invoice.items():
            setattr(invoice, attr, value)
        invoice.save()
        instance.invoices.add(invoice)
        instance.save()
        for item in completed_items:
            new_item = InvoiceItems()
            new_item.invoice = invoice
            for attr, value in item.items():
                setattr(new_item, attr, value)
            new_item.save()
        os.remove(instance.filename())
    except (PdfReadError, HttpResponseError) as e:
        instance.error_message = e
        instance.status = 'Error'
        instance.save()
        os.remove(instance.filename())
    except Exception as e:
        instance.error_message = e
        instance.status = 'Error'
        instance.save()
        os.remove(instance.filename())
