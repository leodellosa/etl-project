from django.shortcuts import render, get_object_or_404, redirect
from .models import Course
from django.db.models import Q
from django.contrib import messages
from etl_project.config import DJANGO_ENV, get_api_urls
import requests
from admin_panel.models import APISettings
import logging
from etl_project.utils.decorators import login_required_session_token
from django.forms import formset_factory
from .forms import CourseForm, LevelForm, CategoryForm, ItemForm

logger = logging.getLogger('myapp')
 
@login_required_session_token
def course_list(request):
    token = request.session.get('access_token')
    
    _, COURSE_API_URL = get_api_urls()
    settings = APISettings.objects.first()
    courses = []

    print(f"DJANGO_ENV: {DJANGO_ENV} and COURSE_API_URL: {COURSE_API_URL}")

    if DJANGO_ENV == 'production':
        base_url = f"{COURSE_API_URL}/courses"
        try:
            response = requests.get(base_url, timeout=5)
            response.raise_for_status()
            courseData = response.json()
            courses = courseData.get("data", [])
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

        return render(request, "course_list_api.html", {"courses": courses})

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
    

@login_required_session_token
def course_detail_by_id(request, id):
    _, COURSE_API_URL = get_api_urls()
    settings = APISettings.objects.first()

    if DJANGO_ENV == 'production':
        base_url = f"{COURSE_API_URL}/course/details/{id}"
        try:
            response = requests.get(base_url, timeout=5)
            if response.status_code == 200:
                course = response.json()
                return render(request, 'course_details_api.html', {'course': course})
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
        
        return render(request, 'course_list_api.html', {'courses': []})
    else:
        course = get_object_or_404(Course, id=id)
        return render(request, 'course_details.html', {'course': course})


# Create formsets
LevelFormSet = formset_factory(LevelForm, extra=1)
CategoryFormSet = formset_factory(CategoryForm, extra=1, can_delete=True)
ItemFormSet = formset_factory(ItemForm, extra=1, can_delete=True)

def create_course(request):
    _, COURSE_API_URL = get_api_urls()
    settings = APISettings.objects.first()

    if request.method == 'POST':
        base_url = f"{COURSE_API_URL}/course/create"
        course_form = CourseForm(request.POST)
        level_formset = LevelFormSet(request.POST, prefix='levels')
        try:
            if course_form.is_valid() and level_formset.is_valid():
                payload = {
                    'title': course_form.cleaned_data['title'],
                    'description': course_form.cleaned_data['description'],
                    'levels': []
                }

                for i, level_form in enumerate(level_formset.forms):
                    if not level_form.cleaned_data or level_form.cleaned_data.get('DELETE'):
                        continue

                    level_name = level_form.cleaned_data['name']
                    categories_data = []

                    category_formset = CategoryFormSet(request.POST, prefix=f'categories-{i}')
                    if category_formset.is_valid():
                        for j, category_form in enumerate(category_formset.forms):
                            if not category_form.cleaned_data or category_form.cleaned_data.get('DELETE'):
                                continue

                            category_name = category_form.cleaned_data['name']
                            items_data = []

                            item_formset = ItemFormSet(request.POST, prefix=f'items-{i}-{j}')
                            if item_formset.is_valid():
                                for item_form in item_formset.forms:
                                    if not item_form.cleaned_data or item_form.cleaned_data.get('DELETE'):
                                        continue
                                    items_data.append({'name': item_form.cleaned_data['name']})

                            categories_data.append({
                                'name': category_name,
                                'items': items_data
                            })

                    payload['levels'].append({
                        'name': level_name,
                        'categories': categories_data
                    })
                print(f"Payload: {payload}")
                # Send data to your backend API
                response = requests.post(base_url, json=payload,timeout=5)
                
                if response.status_code == 200:
                    messages.success(request, "Course created successfully!")
                    return redirect('course_list')
                else:
                    error = response.json()
                    error_msg = error.get("error", error.get("detail", "Failed to create course."))
                    messages.error(request, error_msg)
                    logger.error(f"Error creating course: {response.status_code} - {error_msg}")
        except requests.exceptions.RequestException as e:
            error_msg = settings.get_course_api_message() if settings else "Course API is currently unavailable."
            messages.error(request, error_msg)
            logger.error(f"RequestException while creating course: {e}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            logger.exception("Unexpected error in create_course view")

    else:
        course_form = CourseForm()
        level_formset = LevelFormSet(prefix='levels')

    return render(request, 'create_course.html', {
        'course_form': course_form,
        'level_formset': level_formset
    })

