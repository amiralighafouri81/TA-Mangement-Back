from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
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

    def destroy(self, request, *args, **kwargs):
        # Check if the user is staff
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this object.")

        # Proceed with the default destroy method if user is staff
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Check if the user is staff
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to update this object.")

        # Proceed with the default destroy method if user is staff
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Check if the user is staff
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to create this object.")

        # Proceed with the default destroy method if user is staff
        return super().destroy(request, *args, **kwargs)
