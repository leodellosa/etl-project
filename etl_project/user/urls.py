from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('register/',views.register_user, name='register'),
    path('<int:id>/', views.user_detail, name='user_by_id'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    
]