from django.contrib import admin
from . import models

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user__first_name', 'user__last_name', 'user__email']
    list_per_page = 10
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']

@admin.register(models.Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user__first_name', 'user__last_name', 'user__email')
    list_per_page = 10
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('semester', 'instructor', 'name')
    list_per_page = 10
    search_fields = ['name__istartswith']