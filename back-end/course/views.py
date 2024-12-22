from django_filters import rest_framework as filters
from rest_framework.viewsets import ModelViewSet
from .models import Course
from .serializers import CourseSerializer


class CourseFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Course
        fields = ['name']

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CourseFilter  # Use the custom FilterSet

    def get_serializer_context(self):
        return {'request': self.request}
