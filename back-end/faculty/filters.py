from django_filters import FilterSet
from .models import Instructor

class InstructorFilter(FilterSet):
    class Meta:
        model = Instructor
        fields = {
            'user__first_name': ['icontains'],
            'user__last_name': ['icontains'],
        }