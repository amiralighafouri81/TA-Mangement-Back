from django.contrib import admin
from . import models

@admin.register(models.Policy)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'value')
    list_per_page = 10
    search_fields = ['id']  # Add fields for search