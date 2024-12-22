from django.contrib import admin
from . import models

@admin.register(models.Request)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course', 'student')
    list_per_page = 10
    # search_fields = ['name__istartswith']
