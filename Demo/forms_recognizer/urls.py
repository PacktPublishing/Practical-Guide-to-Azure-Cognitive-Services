from django.urls import path, include
from . import views

app_name = 'forms_recognizer'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload_invoice/', views.upload_invoice, name='upload_invoice'),
    path('upload_general/', views.upload_general, name='upload_general'),
    path('update_invoice_list', views.update_invoice_list, name='update_invoice_list'),
    path('invoice/<pk>', views.invoice_details, name='invoice_details')
]
