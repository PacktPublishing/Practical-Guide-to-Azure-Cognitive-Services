import os
import pathlib
import uuid

from django.db import models


def invoice_upload_handler(instance, filename):
    file_path = pathlib.Path(filename)
    new_filename = str(uuid.uuid1())
    return f"invoices/{new_filename}{file_path.suffix}"


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=255, blank=True, null=True)
    uploaded_file = models.FileField(upload_to=invoice_upload_handler, blank=True, null=True)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    amount_due = models.CharField(max_length=255, blank=True, null=True)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    billing_address_recipient = models.CharField(max_length=255, blank=True, null=True)
    customer_address = models.CharField(max_length=255, blank=True, null=True)
    customer_address_recipient = models.CharField(max_length=255, blank=True, null=True)
    customer_id = models.CharField(max_length=255, blank=True, null=True)
    due_date = models.CharField(max_length=255, blank=True, null=True)
    invoice_date = models.CharField(max_length=255, blank=True, null=True)
    invoice_id = models.CharField(max_length=255, blank=True, null=True)
    invoice_total = models.CharField(max_length=255, blank=True, null=True)
    previous_unpaid_balance = models.CharField(max_length=255, blank=True, null=True)
    purchase_order = models.CharField(max_length=255, blank=True, null=True)
    remittance_address = models.CharField(max_length=255, blank=True, null=True)
    remittance_address_recipient = models.CharField(max_length=255, blank=True, null=True)
    service_address = models.CharField(max_length=255, blank=True, null=True)
    service_address_recipient = models.CharField(max_length=255, blank=True, null=True)
    service_end_date = models.CharField(max_length=255, blank=True, null=True)
    service_start_date = models.CharField(max_length=255, blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    shipping_address_recipient = models.CharField(max_length=255, blank=True, null=True)
    sub_total = models.CharField(max_length=255, blank=True, null=True)
    total_tax = models.CharField(max_length=255, blank=True, null=True)
    vendor_address = models.CharField(max_length=255, blank=True, null=True)
    vendor_address_recipient = models.CharField(max_length=255, blank=True, null=True)
    vendor_name = models.CharField(max_length=255, blank=True, null=True)
    json_body = models.JSONField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def filename(self):
        return os.path.basename(self.uploaded_file.name)

    class Meta:
        ordering = ['date_created']
        verbose_name_plural = 'invoices'

    def __str__(self):
        return f"{self.id}-{self.filename()}"


class InvoiceItems(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)
    product_code = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    unit_price = models.CharField(max_length=255, blank=True, null=True)
    tax = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_created']
        verbose_name_plural = 'invoice items'

    def __str__(self):
        return f"{self.id}"


class ScanInvoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=255, blank=True, null=True)
    uploaded_file = models.FileField(upload_to=invoice_upload_handler)
    invoice_type = models.CharField(max_length=255, blank=True, null=True)
    invoices = models.ManyToManyField(Invoice, 'invoices')
    error_message = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def filename(self):
        return os.path.basename(self.uploaded_file.name)

    class Meta:
        ordering = ['date_created']
        verbose_name_plural = 'scan invoices'

    def __str__(self):
        return f"{self.id}-{self.filename()}"
