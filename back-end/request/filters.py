from django_filters import FilterSet
from .models import Request


class RequestFilter(FilterSet):
    class Meta:
        model = Request
        fields = {
            'id': ['exact']
        }