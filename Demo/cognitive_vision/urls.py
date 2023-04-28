from django.urls import path
from . import views

app_name = 'cognitive_vision'
urlpatterns = [
    path('', views.index, name='index'),
    path('check/', views.check, name='check'),
    path('reclassify/<int:result_id>', views.reclassify, name='reclassify'),
]
