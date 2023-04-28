import os
from os import TMP_MAX
from PyPDF2.utils import PdfReadError
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer._helpers import get_content_type
from azure.core.credentials import AzureKeyCredential
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref, with_expression
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from caseconverter import snakecase
from PyPDF2 import PdfFileWriter, PdfFileReader


def processPage(page, content_type, form_recognizer_client):
    poller = form_recognizer_client.begin_recognize_invoices(
                page, content_type=content_type)
    result = poller.result()

    for invoice in result:
        invoice_details = dict()
        item_list = list()
        for name, field in invoice.fields.items():
            if name == "Items":
                print("Invoice Items:")
                for idx, items in enumerate(field.value):
                    print("...Item #{}".format(idx+1))
                    item_details = dict()
                    for item_name, item in items.value.items():
                        print("......{}: {} has confidence {}".format(
                            item_name, item.value, item.confidence))
                        item_details[str(
                            snakecase(item_name))] = item.value
                    item_list.append(item_details)
                    print(item_details)
            else:
                print("{}: {} has confidence {}".format(
                    name, field.value, field.confidence))
                invoice_details[str(snakecase(name))] = field.value
        invoice_obj = Invoice(**invoice_details)
        s = session()
        s.add(invoice_obj)
        for it in item_list:
            i = Item(**it)
            i.invoice = invoice_obj
            s.add(i)
        s.commit()


def analyze():
    endpoint = "https://<your_endpoint_name>.cognitiveservices.azure.com/"
    credential = AzureKeyCredential("<your_key>")

    form_recognizer_client = FormRecognizerClient(endpoint, credential)

    # Loop to print each filename separately
    with open(f'sample-invoice.jpg', "rb") as fd:
        content_type = get_content_type(fd)

        if content_type == 'application/pdf':
            pages = int(PdfFileReader(fd).getNumPages())
            print("This is a PDF file!!")
            for page in range(pages):
                output = PdfFileWriter()
                output.addPage(PdfFileReader(fd).getPage(page))
                with open(f"temp_page{page}.pdf", 'wb') as new_file:
                    output.write(new_file)
                with open(f"temp_page{page}.pdf", 'rb') as read_file:
                    processed = processPage(
                                read_file,
                                content_type,
                                form_recognizer_client
                            )
        else:
            print("Not a PDF File")
            print(f"file: {fd.name}")
            invoice = fd.read()
            processPage(invoice, content_type, form_recognizer_client)


Base = declarative_base()


class Invoice(Base):
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    amount_due = Column(String)
    billing_address = Column(String)
    billing_address_recipient = Column(String)
    customer_address = Column(String)
    customer_address_recipient = Column(String)
    customer_id = Column(String)
    due_date = Column(String)
    invoice_date = Column(String)
    invoice_id = Column(String)
    invoice_total = Column(String)
    previous_unpaid_balance = Column(String)
    purchase_order = Column(String)
    remittance_address = Column(String)
    remittance_address_recipient = Column(String)
    service_address = Column(String)
    service_address_recipient = Column(String)
    service_end_date = Column(String)
    service_start_date = Column(String)
    shipping_address = Column(String)
    shipping_address_recipient = Column(String)
    sub_total = Column(String)
    total_tax = Column(String)
    vendor_address = Column(String)
    vendor_address_recipient = Column(String)
    vendor_name = Column(String)


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    product_code = Column(String)
    quantity = Column(String)
    amount = Column(String)
    unit = Column(String)
    unit_price = Column(String)
    tax = Column(String)
    date = Column(String)
    invoice_id = Column(Integer, ForeignKey('invoice.id'))
    invoice = relationship(
        Invoice, backref=backref('item', uselist=True))


engine = create_engine('sqlite:///example.sqlite3')
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

analyze()
