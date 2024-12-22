from django_filters import FilterSet
from .models import Course

class CourseFilter(FilterSet):
    class Meta:
        model = Course
        fields = {
            'name': ['icontains'],
        }