from django import forms
from django.contrib import admin
from . import models

class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        course = self.instance  # The current Course instance
        if course.pk:
            # Filter head_TA to only show accepted requests for the current course
            self.fields['head_TA'].queryset = models.Request.objects.filter(
                course=course,
                status=models.Request.REQUSET_STATUS_ACCEPTED,
                student__isnull=False
            )
        else:
            # If creating a new course, set head_TA to an empty queryset
            self.fields['head_TA'].queryset = models.Request.objects.none()

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm  # Use the custom form with the filtered head_TA field
    list_display = ('id', 'name', 'semester', 'instructor', 'head_TA')
    list_per_page = 10
    search_fields = ['name__icontains']
    ordering = ('id',)
