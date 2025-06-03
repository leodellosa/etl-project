from django.contrib import admin
from .models import Course

# Register the custom admin class with the model
admin.site.register(Course)