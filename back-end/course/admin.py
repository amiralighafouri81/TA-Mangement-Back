from django.contrib import admin
from . import models

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'semester', 'instructor')
    list_per_page = 10
    search_fields = ['name__istartswith']
