# from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'appmain'
urlpatterns = [
    path('', views.AppMainView.as_view(), name='main'),
    path('type/<int:type_id>/', views.TypeView.as_view(), name='types'),
    path('computer/<int:computer_id>/', views.ComputerView.as_view(), name='computer_info'),
]
