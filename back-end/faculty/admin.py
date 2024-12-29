from django.contrib import admin
from . import models
from core.models import User
from django.utils.html import format_html
from django.templatetags.static import static

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'student_number']
    list_per_page = 10
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            # Filter users to only show those with the Student role
            kwargs["queryset"] = User.objects.filter(role=User.STUDENT)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(models.Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'staff_id')
    list_per_page = 10
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']

    class Media:
        # Link the CSS file to be loaded in the admin panel
        css = {
            'all': (static('admin_area/css/admin_styles.css'),)
        }

    # def go_to_link(self, obj):
    #    return format_html(
    #        '<a class="button" href="{}" target="_blank" style="padding: 5px 10px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">Go to Link</a>',
    #        "https://example.com/some-link/"
    #    )
    # go_to_link.short_description = "External Link"  # Label for the column

    def changelist_view(self, request, extra_context=None):
        # Add a custom button for bulk uploading instructors
        extra_context = extra_context or {}
        extra_context["bulk_upload_button"] = format_html(
            '<a class="button" href="bulk_upload/">Add Instructors in Bulk</a>'
        )
        return super().changelist_view(request, extra_context=extra_context)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            # Filter users to only show those with the Instructor role
            kwargs["queryset"] = User.objects.filter(role=User.INSTRUCTOR)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
