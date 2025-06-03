from django.shortcuts import render, get_object_or_404
from .forms import UserForm
from .models import User
from django.db.models import Q
from django.contrib import messages
from etl_project.config import DJANGO_ENV, get_api_urls
import requests
from admin_panel.models import APISettings
import logging

logger = logging.getLogger('django')

def user_list(request):
    USER_API_URL, _ = get_api_urls()
    settings = APISettings.objects.first()
    users = []

    print(f"DJANGO_ENV: {DJANGO_ENV} and USER_API_URL: {USER_API_URL}")
    if DJANGO_ENV == 'production':
        base_url = f"{USER_API_URL}/users"
        try:
            response = requests.get(base_url, timeout=5)
            response.raise_for_status()
            usersData = response.json()
            users = usersData.get('data', [])
            if response.status_code == 200:
                return render(request, 'user_list.html', {'users': users})
            else:
                messages.error(request, f"Error fetching users: {response.status_code}")
        except requests.exceptions.RequestException as e:
            error_msg = settings.get_user_api_message() if settings else "User API is currently unavailable."
            messages.error(request, error_msg)
            logger.error(f"RequestException while fetching users: {e}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            logger.exception("Unexpected error in user_list view")
        
        return render(request, 'user_list.html', {'users': users})
    
    else:
        users = User.objects.all()
        query = request.GET.get('q', '')
        if query:
            user = User.objects.filter(Q(email__icontains=query))
        else:
            user = User.objects.all()

        return render(request, 'user_list.html', {'users': user,'query': query})

def user_detail(request, id):
    USER_API_URL, _ = get_api_urls()
    settings = APISettings.objects.first()
    if (DJANGO_ENV == 'production'):
        base_url = f"{USER_API_URL}/users/{id}"
        try:
            response = requests.get(base_url, timeout=5)
            if response.status_code == 200:
                user = response.json()
                return render(request, 'user_details.html', {'user': user})
            else:
                messages.error(request, f"Error fetching users: {response.status_code}")
        except requests.exceptions.RequestException as e:
           error_msg = settings.get_user_api_message() if settings else "User API is currently unavailable."
           messages.error(request, error_msg)
           logger.error(f"RequestException while fetching user id: {id} - {e}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            logger.exception("Unexpected error in user_detail view")

        return render(request, 'user_list.html', {'user': []})
    else:
        user = get_object_or_404(User, id=id)
        return render(request, 'user_details.html', {'user': user})

