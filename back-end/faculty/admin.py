from django.contrib import admin
from . import models

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'student_number']
    list_per_page = 10
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']

@admin.register(models.Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'staff_id')
    list_per_page = 10
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']