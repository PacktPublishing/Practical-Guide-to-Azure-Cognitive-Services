from django.urls import path
from . import views

app_name = 'cognitive_search'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('view/<str:key_id>', views.view, name='view'),
]
