from django.shortcuts import render, get_object_or_404
from .models import Course
from .forms import CourseForm
from django.db.models import Q
from django.contrib import messages
from etl_project.config import DJANGO_ENV, get_api_urls
import requests
from admin_panel.models import APISettings
import logging

logger = logging.getLogger('myapp')
 
def course_list(request):
    _, COURSE_API_URL = get_api_urls()
    settings = APISettings.objects.first()
    courses = []

    print(f"DJANGO_ENV: {DJANGO_ENV} and COURSE_API_URL: {COURSE_API_URL}")

    if DJANGO_ENV == 'production':
        base_url = f"{COURSE_API_URL}/courses"
        try:
            response = requests.get(base_url, timeout=5)
            response.raise_for_status()
            courses = response.json()
        except requests.exceptions.RequestException as e:
            custom_msg = (
                settings.get_course_api_message()
                if settings and hasattr(settings, "get_course_api_message")
                else "Course API is currently unavailable."
            )
            messages.error(request, custom_msg)
            logger.error(f"RequestException while fetching courses: {e}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            logger.exception("Unexpected error in course_list view")

        return render(request, "course_list.html", {"courses": courses})

    else:
        # Development fallback
        courses = Course.objects.all()
        query = request.GET.get("q", "")
        if query:
            courses = courses.filter(Q(title__icontains=query))

        return render(request, "course_list.html", {
            "courses": courses,
            "query": query
        })
    

def course_detail_by_id(request, id):
    _, COURSE_API_URL = get_api_urls()
    settings = APISettings.objects.first()

    if DJANGO_ENV == 'production':
        base_url = f"{COURSE_API_URL}/course/details/{id}"
        try:
            response = requests.get(base_url, timeout=5)
            if response.status_code == 200:
                course = response.json()
                return render(request, 'course_details.html', {'course': course})
            else:
                # print(f"Error fetching courses: {response.status_code}")
                messages.error(request, f"Error fetching courses: {response.status_code}")
        except requests.exceptions.RequestException as e:
                error_msg = settings.get_course_api_message() if settings else "Course API is currently unavailable."
                messages.error(request, error_msg)   
                logger.error(f"RequestException while fetching course id: {id} - {e}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            logger.exception("Unexpected error in get course_detail_by_id view")
        
        return render(request, 'course_list.html', {'courses': []})
    else:
        course = get_object_or_404(Course, id=id)
        return render(request, 'course_details.html', {'course': course})


