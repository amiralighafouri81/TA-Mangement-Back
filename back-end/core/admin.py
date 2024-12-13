from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django import forms
from faculty.models import Student, Instructor


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "username", "role", "password1", "password2" ),
            },
        ),
    )
    list_display = ("username", "first_name", "last_name", "role", "is_staff")

