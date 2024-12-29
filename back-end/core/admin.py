from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

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
    list_display = ("id", "username", "first_name", "last_name", "role", "is_staff")
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    ordering = ('id',)  # Sort by id