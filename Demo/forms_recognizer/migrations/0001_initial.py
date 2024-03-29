# Generated by Django 4.0.2 on 2022-02-13 03:22

from django.db import migrations, models
import django.db.models.deletion
import forms_recognizer.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('uploaded_file', models.FileField(blank=True, null=True, upload_to=forms_recognizer.models.invoice_upload_handler)),
                ('customer_name', models.CharField(blank=True, max_length=255, null=True)),
                ('amount_due', models.CharField(blank=True, max_length=255, null=True)),
                ('billing_address', models.CharField(blank=True, max_length=255, null=True)),
                ('billing_address_recipient', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_address', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_address_recipient', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_id', models.CharField(blank=True, max_length=255, null=True)),
                ('due_date', models.CharField(blank=True, max_length=255, null=True)),
                ('invoice_date', models.CharField(blank=True, max_length=255, null=True)),
                ('invoice_id', models.CharField(blank=True, max_length=255, null=True)),
                ('invoice_total', models.CharField(blank=True, max_length=255, null=True)),
                ('previous_unpaid_balance', models.CharField(blank=True, max_length=255, null=True)),
                ('purchase_order', models.CharField(blank=True, max_length=255, null=True)),
                ('remittance_address', models.CharField(blank=True, max_length=255, null=True)),
                ('remittance_address_recipient', models.CharField(blank=True, max_length=255, null=True)),
                ('service_address', models.CharField(blank=True, max_length=255, null=True)),
                ('service_address_recipient', models.CharField(blank=True, max_length=255, null=True)),
                ('service_end_date', models.CharField(blank=True, max_length=255, null=True)),
                ('service_start_date', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_address', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_address_recipient', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_total', models.CharField(blank=True, max_length=255, null=True)),
                ('total_tax', models.CharField(blank=True, max_length=255, null=True)),
                ('vendor_address', models.CharField(blank=True, max_length=255, null=True)),
                ('vendor_address_recipient', models.CharField(blank=True, max_length=255, null=True)),
                ('vendor_name', models.CharField(blank=True, max_length=255, null=True)),
                ('json_body', models.JSONField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'invoices',
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='ScanInvoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('uploaded_file', models.FileField(upload_to=forms_recognizer.models.invoice_upload_handler)),
                ('invoice_type', models.CharField(blank=True, max_length=255, null=True)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('invoices', models.ManyToManyField(related_name='invoices', to='forms_recognizer.Invoice')),
            ],
            options={
                'verbose_name_plural': 'scan invoices',
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='InvoiceItems',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('product_code', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.CharField(blank=True, max_length=255, null=True)),
                ('unit', models.CharField(blank=True, max_length=255, null=True)),
                ('unit_price', models.CharField(blank=True, max_length=255, null=True)),
                ('tax', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.CharField(blank=True, max_length=255, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms_recognizer.invoice')),
            ],
            options={
                'verbose_name_plural': 'invoice items',
                'ordering': ['date_created'],
            },
        ),
    ]
