from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .models import Course
from .pagination import DefaultPagination
from .serializers import CourseSerializer
from .filters import CourseFilter


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter
    pagination_class = DefaultPagination

    def get_serializer_context(self):
        return {'request': self.request}
