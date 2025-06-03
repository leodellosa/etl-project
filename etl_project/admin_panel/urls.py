from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_settings, name="admin-settings"),
]
