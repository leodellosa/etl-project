from django.db import models
from django.utils import timezone

class User(models.Model):
    firstName = models.CharField("First Name", max_length=100, blank=True, null=True)
    lastName = models.CharField("Last Name", max_length=100, blank=True, null=True)
    middleName = models.CharField("Middle Name", max_length=100, blank=True, null=True)

    email = models.EmailField("Email", unique=True)
    mobile = models.CharField("Mobile Number (Viber)", max_length=15, blank=True, null=True)

    username = models.CharField("Username", max_length=150, unique=True, blank=True, null=True)
    plain_password = models.CharField("Password (Unhashed)", max_length=128, blank=True, null=True)  # ⚠️ Store temporarily only!

    ROLE_CHOICES = [
        ('learner', 'Learner'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]
    role = models.CharField("Role/Title", max_length=20, choices=ROLE_CHOICES, blank=True, null=True)

    STATus_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]
    status = models.CharField("Status", max_length=10, choices=STATus_CHOICES, default='active')
    created_at = models.DateTimeField("Registration Date", default=timezone.now)

    @property
    def completeName(self):
        names = filter(None, [self.firstName, self.middleName, self.lastName])
        return " ".join(names)

    def __str__(self):
        return f"{self.completeName} - {self.email}"
