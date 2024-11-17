from django.contrib import admin
from . import models

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user__first_name', 'user__last_name', 'user__email', 'entrance_year']
    list_editable = ['entrance_year']
    list_per_page = 10
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']

@admin.register(models.Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user__first_name', 'user__last_name', 'user__email')
    list_per_page = 10
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']
