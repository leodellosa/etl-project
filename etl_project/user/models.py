from django.db import models

class User(models.Model):

    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    date_of_birth = models.DateField()

    # STATUS_CHOICES = [
    #     ('Active', 'Active'),
    #     ('Inactive', 'Inactive'),
    # ]
    # status = models.CharField(
    #     max_length=10,
    #     choices=STATUS_CHOICES,
    #     default='Active',
    # )

    def __str__(self):
        return f"{self.email} - {self.age} - {self.date_of_birth}"