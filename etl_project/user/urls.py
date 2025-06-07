from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('register/',views.register_user, name='register'),
    path('<int:id>/', views.user_detail, name='user_by_id'),
    
]