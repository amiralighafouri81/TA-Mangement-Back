from django_filters import FilterSet, NumberFilter
from .models import Course

class CourseFilter(FilterSet):
    instructor_id = NumberFilter(field_name='instructor', lookup_expr='exact')
    class Meta:
        model = Course
        fields = {
            'name': ['icontains'],
            'id' : ['exact'],
            'instructor': ['exact'],
        }