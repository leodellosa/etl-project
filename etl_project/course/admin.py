import nested_admin
from django.contrib import admin
from .models import Course, Level, Category, Item

class ItemInline(nested_admin.NestedTabularInline):
    model = Item
    extra = 1

class CategoryInline(nested_admin.NestedTabularInline):
    model = Category
    extra = 1
    inlines = [ItemInline]

class LevelInline(nested_admin.NestedTabularInline):
    model = Level
    extra = 1
    inlines = [CategoryInline]

@admin.register(Course)
class CourseAdmin(nested_admin.NestedModelAdmin):
    inlines = [LevelInline]
