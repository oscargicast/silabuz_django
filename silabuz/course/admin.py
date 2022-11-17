from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'max_capacity',
        'is_active',
        'modified',
        'created',
    )
