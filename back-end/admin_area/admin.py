from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django import forms
import csv
import io
from faculty.models import Instructor
from core.models import User  # Assuming User model exists in core.models

# Form for bulk uploading instructors
class BulkInstructorUploadForm(forms.Form):
    csv_file = forms.FileField(label="CSV File", required=True)

# Extend the functionality of the existing InstructorAdmin
def add_bulk_upload_functionality(admin_class):
    def get_urls(self):
        urls = super(admin_class, self).get_urls()
        custom_urls = [
            path('bulk_upload/', self.admin_site.admin_view(self.bulk_upload), name="bulk_upload_instructors"),
        ]
        return custom_urls + urls

    def bulk_upload(self, request):
        if request.method == "POST":
            form = BulkInstructorUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data["csv_file"]
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                reader = csv.DictReader(io_string)
                
                created_instructors = []
                for row in reader:
                    try:
                        user, user_created = User.objects.get_or_create(
                            username=row["username"],
                            defaults={
                                "first_name": row["first_name"],
                                "last_name": row["last_name"],
                                "email": row["email"],
                                "role": User.INSTRUCTOR,  # Assuming role field exists
                            },
                        )
                        if not user_created and user.role != User.INSTRUCTOR:
                            raise ValidationError(f"User {user.username} exists but is not an instructor.")
                        
                        instructor, instructor_created = Instructor.objects.get_or_create(
                            user=user,
                            defaults={
                                "staff_id": row["staff_id"],
                                "way_of_communication": row["way_of_communication"],
                                "research_fields": row["research_fields"],
                            },
                        )
                        if instructor_created:
                            created_instructors.append(user.username)
                    except Exception as e:
                        self.message_user(request, f"Error processing row for {row.get('username', 'Unknown')}: {e}", level="error")
                
                self.message_user(request, f"{len(created_instructors)} instructors created successfully.", level="success")
                return redirect("..")
        else:
            form = BulkInstructorUploadForm()

        context = self.admin_site.each_context(request)
        context["form"] = form
        context["opts"] = self.model._meta
        return TemplateResponse(request, "admin/bulk_upload_instructors.html", context)

    # Add the custom methods to the admin class
    admin_class.get_urls = get_urls
    admin_class.bulk_upload = bulk_upload
    return admin_class

# Import the existing InstructorAdmin
from faculty.admin import InstructorAdmin

# Extend the functionality
InstructorAdmin = add_bulk_upload_functionality(InstructorAdmin)

