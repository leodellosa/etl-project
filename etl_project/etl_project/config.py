import os
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path, override=True)  # <--- force override
# print(f"Loaded environment variables from {dotenv_path}")

DJANGO_ENV = os.getenv("DJANGO_ENV", "development")
# print(f"DJANGO_ENV: {DJANGO_ENV}")
# etl_project/etl_project/config.py
DEFAULT_USER_API_URL = os.getenv("USER_API_URL", "http://127.0.0.1:8000")
DEFAULT_COURSE_API_URL = os.getenv("COURSE_API_URL", "http://127.0.0.1:8000")

def get_api_urls():
    try:
        from admin_panel.models import APISettings
        settings = APISettings.objects.first()
        if settings:
            user_api_url = settings.user_api_url or DEFAULT_USER_API_URL
            course_api_url = settings.course_api_url or DEFAULT_COURSE_API_URL
        else:
            user_api_url = DEFAULT_USER_API_URL
            course_api_url = DEFAULT_COURSE_API_URL
    except (ImportError, ImproperlyConfigured):
        user_api_url = DEFAULT_USER_API_URL
        course_api_url = DEFAULT_COURSE_API_URL

    return user_api_url, course_api_url


# USER_API_URL, COURSE_API_URL = get_api_urls()

# Task to allow settings of environment variable in ECS not from .env file
# import os

# if os.getenv("DJANGO_ENV") != "production":
#     from dotenv import load_dotenv
#     load_dotenv()