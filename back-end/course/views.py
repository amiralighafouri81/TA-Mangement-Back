from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Course
from .pagination import DefaultPagination
from .serializers import CourseSerializer
from .filters import CourseFilter
from faculty.models import Instructor


class CourseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = self.request.user
        if user.role == 'instructor':
            # Get all courses taught by the current instructor
            instructor = Instructor.objects.get(user=user)
            return Course.objects.filter(instructor=instructor)

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        # Check if the user is staff
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this object.")

        # Proceed with the default destroy method if user is staff
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        # Check if the user is staff
        if not user.is_staff and user.role != 'instructor':
            raise PermissionDenied("You do not have permission to update this object.")

        # Proceed with the default destroy method if user is staff
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Check if the user is staff
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to create this object.")

        # Proceed with the default destroy method if user is staff
        return super().create(request, *args, **kwargs)