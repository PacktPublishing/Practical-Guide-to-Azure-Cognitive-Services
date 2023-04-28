from django.contrib import admin
from .models import Invoice, InvoiceItems, ScanInvoice


class InvoiceAdmin(admin.ModelAdmin):
    pass


class InvoiceItemsAdmin(admin.ModelAdmin):
    pass


class ScanInvoiceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItems, InvoiceItemsAdmin)
admin.site.register(ScanInvoice, ScanInvoiceAdmin)
