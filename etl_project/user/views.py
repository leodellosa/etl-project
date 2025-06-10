from django.shortcuts import render, get_object_or_404,redirect
from .models import User
from django.db.models import Q
from django.contrib import messages
from etl_project.config import DJANGO_ENV, get_api_urls
import requests
from admin_panel.models import APISettings
import logging
from datetime import datetime
from .forms import RegistrationForm,LoginForm,ProfileEditForm
import jwt
from etl_project.utils.decorators import login_required_session_token

logger = logging.getLogger('django')

@login_required_session_token
def user_list(request):
    token = request.session.get('access_token')
    
    USER_API_URL, _ = get_api_urls()
    settings = APISettings.objects.first()
    users = []

    print(f"DJANGO_ENV: {DJANGO_ENV} and USER_API_URL: {USER_API_URL}")
    if DJANGO_ENV == 'production':
        base_url = f"{USER_API_URL}/users"
        try:
            response = requests.get(base_url,headers={'Authorization': f'Bearer {token}'}, timeout=5)
            # response.raise_for_status()
            usersData = response.json()
            users = usersData.get('data', [])
            if response.status_code == 200:
                for user in users:
                    if 'created_at' in user:
                        try:
                            user['created_at_formatted'] = datetime.fromisoformat(user['created_at']).strftime('%b %d, %Y')
                        except ValueError:
                            user['created_at_formatted'] = user['created_at'] 
                return render(request, 'user_list.html', {'users': users})
            else:
                error = usersData.get("error", usersData.get("detail", "Error fetching users."))
                messages.error(request, error)
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


@login_required_session_token
def user_detail(request, id):
    token = request.session.get('access_token')
    
    USER_API_URL, _ = get_api_urls()
    settings = APISettings.objects.first()
    if (DJANGO_ENV == 'production'):
        base_url = f"{USER_API_URL}/users/{id}"
        try:
            response = requests.get(base_url,headers={'Authorization': f'Bearer {token}'}, timeout=5)
            user = response.json()
            if response.status_code == 200:
                if 'created_at' in user:
                    try:
                        user['created_at_formatted'] = datetime.fromisoformat(user['created_at']).strftime('%b %d, %Y')
                    except ValueError:
                        user['created_at_formatted'] = user['created_at']
                return render(request, 'user_details.html', {'user': user})
            else:
                 messages.error(request,user.get("error", user.get("detail", "Error fetching users.")))
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

def register_user(request):
    USER_API_URL, _ = get_api_urls()
    settings = APISettings.objects.first()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            payload = form.cleaned_data
            try:
                baseUrl = f"{USER_API_URL}/users/register"
                response = requests.post(baseUrl, json=payload,timeout=5)
                if response.status_code == 201:
                    messages.success(request, "Registration successful. You can now log in.")
                    return redirect('register')
                else:
                    error = response.json()
                    error_msg = error.get("error",  error.get("detail","Error registering user."))
                    messages.error(request, error_msg)
                    logger.error(f"Error registering user: {error_msg}")
            except requests.exceptions.RequestException as e:
                error_msg = settings.get_user_api_message() if settings else "User API is currently unavailable."
                messages.error(request, error_msg)
                logger.error(f"RequestException while registering user: {e}")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
                logger.exception("Unexpected error in register_user view")
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"Error in {field.label}: {error}")
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})   


def login_view(request):
    USER_API_URL, _ = get_api_urls()
    settings = APISettings.objects.first()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            payload = {
                'username': username,
                'password': password,
            }
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            try:
                baseUrl = f"{USER_API_URL}/auth/token"
                response = requests.post(baseUrl, data=payload, headers=headers)
                if response.status_code == 200:
                    token_data = response.json()
                    access_token = token_data.get('access_token')
                    refresh_token = token_data.get('refresh_token')
                    
                    request.session['access_token'] = access_token
                    request.session['refresh_token'] = refresh_token

                    decoded = jwt.decode(access_token, options={"verify_signature": False})
                    user_id = decoded.get('sub')
                   
                    base_url = f"{USER_API_URL}/users/{user_id}"
                    user_response = requests.get(base_url, headers={'Authorization': f'Bearer {access_token}'})
                    if user_response.status_code == 200:
                        user_data = user_response.json()
                        request.session['user_details'] = user_data
                    else:
                        messages.error(request, "Failed to fetch user details.")
                        logger.error(f"Error fetching user details: {user_response.status_code} - {user_response.text}")
                    messages.success(request, "Login successful.")
                    return redirect('user_list')
                
                else:
                    try:
                        error = response.json()
                        error_msg = error.get("error", error.get("detail", "Error logging in."))
                    except Exception:
                        error_msg = response.text or "Error logging in."
                    messages.error(request, error_msg)
                    logger.error(f"Error logging in: {error_msg}")
            except requests.exceptions.RequestException as e:
                error_msg = settings.get_user_api_message() if settings else "User API is currently unavailable."
                messages.error(request, error_msg)
                logger.error(f"RequestException while logging in: {e}")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
                logger.exception("Unexpected error in login_user view")
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"Error in {field.label}: {error}")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if 'access_token' in request.session:
        del request.session['access_token']
    if 'refresh_token' in request.session:
        del request.session['refresh_token']
    if 'user_details' in request.session:
        del request.session['user_details']
    return redirect('home')

@login_required_session_token
def profile_view(request):
    user_details = request.session.get('user_details', {})
    if not user_details:
        messages.error(request, "User details not found in session.")
        return redirect('login')
   
    if 'created_at' in user_details:
        try:
            user_details['created_at_formatted'] = datetime.fromisoformat(user_details['created_at']).strftime('%b %d, %Y')
        except ValueError:
            user_details['created_at_formatted'] = user_details['created_at']

    return render(request, 'profile.html', {'user': user_details})

@login_required_session_token
def edit_profile_view(request):
    token = request.session.get('access_token')
    
    user_details = request.session.get('user_details', {})
    if not user_details:
        messages.error(request, "User details not found in session.")
        return redirect('login')

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, initial=user_details)
        if form.is_valid():
            payload = form.cleaned_data
            try:
                USER_API_URL, _ = get_api_urls()
                base_url = f"{USER_API_URL}/users/update/{user_details['id']}"
                headers = {'Authorization': f'Bearer {token}'}
                response = requests.put(base_url, json=payload, headers=headers, timeout=5)
                if response.status_code == 200:
                    updated_user = response.json()
                    request.session['user_details'] = updated_user
                    messages.success(request, "Profile updated successfully.")
                    return redirect('profile')
                else:
                    error = response.json()
                    error_msg = error.get("error", error.get("detail", "Error updating profile."))
                    messages.error(request, error_msg)
            except requests.exceptions.RequestException as e:
                messages.error(request, "User API is currently unavailable.")
                logger.error(f"RequestException while updating profile: {e}")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
                logger.exception("Unexpected error in edit_profile_view")
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"Error in {field.label}: {error}")
    else:
        form = ProfileEditForm(initial=user_details)

    return render(request, 'edit_profile.html', {'form': form})
    