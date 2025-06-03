from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:id>/', views.course_detail_by_id, name='course_by_id'),
    
]