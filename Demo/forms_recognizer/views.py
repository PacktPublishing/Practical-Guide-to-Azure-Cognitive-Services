import pathlib
from asgiref.sync import sync_to_async
from azure.core.exceptions import HttpResponseError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.

from .forms import ScanInvoiceUploadForm
from .forms_recognizer import analyze
from .models import ScanInvoice


@login_required
def index(request):
    invoices = ScanInvoice.objects.all().order_by('-date_created')

    context = {
        'invoices': invoices
    }
    return render(request, 'forms_recognizer/index.html', context)


@login_required
def invoice_details(request, pk):
    invoices: ScanInvoice = get_object_or_404(ScanInvoice, pk=pk)
    file_extension = pathlib.Path(invoices.filename()).suffix.lower()
    context = {
        'invoices': invoices,
        'extension': file_extension,
        'fields': ScanInvoice._meta.get_fields()
    }
    return render(request, 'forms_recognizer/invoice_details.html', context)


def upload_invoice(request):
    form = ScanInvoiceUploadForm(request.POST or None, request.FILES or None)
    context = {
        'form': form
    }
    template = "forms_recognizer/_upload_invoice.html"
    response = render(request, template, context)
    response['HX-Trigger'] = 'refreshTable'

    if request.htmx:
        if form.is_valid():
            try:
                obj = form.save()
                instance = ScanInvoice.objects.get(id__exact=obj.id)
                instance.status = 'Pending'
                instance.invoice_type = 'Invoice'
                instance.save()
                messages.success(request, "File uploaded successfully!")
                sync_to_async(process_invoice(instance))
            except HttpResponseError as msg:
                messages.error(request, msg)
    return response


def upload_general(request):
    form = ScanInvoiceUploadForm(request.POST or None, request.FILES or None)
    context = {
        'form': form
    }
    template = "forms_recognizer/_upload_general.html"
    response = render(request, template, context)
    response['HX-Trigger'] = 'refreshTable'

    if request.htmx:
        if form.is_valid():
            try:
                obj = form.save()
                instance = ScanInvoice.objects.get(id__exact=obj.id)
                instance.status = 'Pending'
                instance.invoice_type = 'General'
                instance.save()
                messages.success(request, "File uploaded successfully!")
                sync_to_async(process_invoice(instance))
            except HttpResponseError as msg:
                messages.error(request, msg)
    return response


@login_required
def update_invoice_list(request):
    if request.htmx:
        invoices = ScanInvoice.objects.all().order_by('-date_created')
        context = {
            'invoices': invoices
        }
        return render(request, 'forms_recognizer/_invoice_list.html', context)


def process_invoice(instance):
    instance.status = "Processing"
    instance.save()
    # sleep(5)
    analyze(instance)
    if not instance.status == "Error":
        instance.status = "Completed"
        instance.save()
