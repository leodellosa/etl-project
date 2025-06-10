from django.contrib import admin
from .models import User
import pprint

# Register the custom admin class with the model
admin.site.register(User)

from django.contrib.sessions.models import Session

class SessionAdmin(admin.ModelAdmin):
    def access_token(self, obj):
        data = obj.get_decoded()
        return data.get('access_token', '—')

    def refresh_token(self, obj):
        data = obj.get_decoded()
        return data.get('refresh_token', '—')
    
    def user_details(self, obj):
        data = obj.get_decoded()
        user_info = data.get('user_details', {})
        return pprint.pformat(user_info) if user_info else '—'

    list_display = ['session_key', 'expire_date', 'access_token','refresh_token', 'user_details']

admin.site.register(Session, SessionAdmin)