from django.contrib import admin
from .models import APISettings

@admin.register(APISettings)
class APISettingsAdmin(admin.ModelAdmin):
    list_display = ('user_api_url', 'course_api_url','user_api_message','course_api_message', 'updated_at')
