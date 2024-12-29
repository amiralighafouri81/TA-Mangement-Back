from django.contrib import admin
from . import models

@admin.register(models.Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('course', 'student','score', 'status')
    list_per_page = 10
    search_fields = ['course__id', 'student__id']  # Add fields for search
