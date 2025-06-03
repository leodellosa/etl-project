from django.db import models
from django.utils import timezone

class User(models.Model):
    first_name = models.CharField("First Name", max_length=100,blank=True, null=True)
    last_name = models.CharField("Last Name", max_length=100,blank=True, null=True)
    middle_name = models.CharField("Middle Name", max_length=100, blank=True, null=True)

    email = models.EmailField("Email", unique=True)
    mobile_number = models.CharField("Mobile Number (Viber)", max_length=15,blank=True, null=True)

    age = models.PositiveIntegerField("Age")
    date_of_birth = models.DateField("Date of Birth")

    ROLE_CHOICES = [
        ('learner', 'Learner'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]
    role = models.CharField("Role/Title", max_length=20, choices=ROLE_CHOICES, default='learner')

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(
        "Status",
        max_length=10,
        choices=STATUS_CHOICES,
        default='Active',
    )

    registration_date = models.DateTimeField("Registration Date", default=timezone.now)

    @property
    def complete_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.complete_name} - {self.email}"
