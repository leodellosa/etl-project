from datetime import datetime, timezone
from django.utils import timezone as dj_timezone
import jwt
from django.shortcuts import redirect
from django.utils.timezone import localtime
import requests
from etl_project.config import DJANGO_ENV, get_api_urls

def is_token_expired(token):
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        exp_timestamp = decoded.get("exp")
        if exp_timestamp:
            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            print(f"Token expiration time: {localtime(exp_datetime)}, Current time: {localtime(dj_timezone.now())}")
            return exp_datetime < dj_timezone.now()
        return True  # Treat missing exp as expired
    except Exception as e:
        print(f"Error decoding token: {e}")
        return True  # Any error = treat as expired

def refresh_token_if_needed(request):
    token = request.session.get('access_token')
    refresh_token = request.session.get('refresh_token')
    USER_API_URL, _ = get_api_urls()

    if not token or is_token_expired(token):
        if not refresh_token:
            return False  # Can't refresh, no token

        # Call backend API to refresh the token
        print("Access token expired, attempting to refresh...")
        try:
            response = requests.post(
                f"{USER_API_URL}/auth/token/refresh",
                json={"refresh_token": refresh_token},
                timeout=5
            )
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get('access_token')
                refresh_token = token_data.get('refresh_token')
                request.session['access_token'] = access_token
                request.session['refresh_token'] = refresh_token
                print("Token refreshed successfully.")
                return True
            else:
                print("Refresh failed:", response.json())
                return False
        except Exception as e:
            print("Refresh error:", e)
            return False

    return True