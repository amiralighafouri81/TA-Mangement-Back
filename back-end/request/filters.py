from django_filters import FilterSet, NumberFilter
from .models import Request

class RequestFilter(FilterSet):
    course = NumberFilter(field_name='course')

    class Meta:
        model = Request
        fields = {
            'id': ['exact'],
            'course': ['exact'],
        }
