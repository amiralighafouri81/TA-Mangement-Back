from django.contrib import admin
from . import models

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'semester', 'instructor', 'head_TA')
    list_per_page = 10
    search_fields = ['name__istartswith']
