from django import forms
from .models import Invoice, InvoiceItems, ScanInvoice


class InvoiceUploadForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['uploaded_file']


class ScanInvoiceUploadForm(forms.ModelForm):
    class Meta:
        model = ScanInvoice
        fields = ['uploaded_file']
