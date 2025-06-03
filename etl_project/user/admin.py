from django.contrib import admin
from .models import User

# Register the custom admin class with the model
admin.site.register(User)