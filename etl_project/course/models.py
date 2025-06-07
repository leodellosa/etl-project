from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    points = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Level(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='levels')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    class Meta:
        unique_together = ('course', 'level')

    def __str__(self):
        return f"{self.course.title} - {self.get_level_display()}"


class Category(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.level.get_level_display()})"


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title
