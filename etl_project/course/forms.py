from django import forms
from .models import Course, Level, Category, Item

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'points']


class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = ['course', 'level']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['level', 'name']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'title', 'content']
