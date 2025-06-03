from django.db import models

class APISettings(models.Model):
    user_api_url = models.URLField("User API URL", max_length=300)
    user_api_message = models.CharField(
        "User API Error Message",
        max_length=255,
        blank=True,
        help_text="Message shown when User API is unreachable. Leave blank to use the default message."
    )

    course_api_url = models.URLField("Course API URL", max_length=300)
    course_api_message = models.CharField(
        "Course API Error Message",
        max_length=255,
        blank=True,
        help_text="Message shown when Course API is unreachable. Leave blank to use the default message."
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"API Settings (Last updated: {self.updated_at})"

    def get_user_api_message(self):
        return self.user_api_message or "User API is currently unavailable. Please try again later."

    def get_course_api_message(self):
        return self.course_api_message or "Course API is currently unavailable. Please try again later."

    class Meta:
        verbose_name = "API Setting"
        verbose_name_plural = "API Settings"
