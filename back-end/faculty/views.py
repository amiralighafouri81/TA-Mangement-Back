from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Student, Instructor
from rest_framework.exceptions import PermissionDenied
from .serializers import StudentSerializer, InstructorSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import DefaultPagination
from .filters import InstructorFilter, StudentFilter


class StudentViewSet(ModelViewSet):
    # queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Student.objects.all()
        else:
            raise PermissionDenied("You do not have permission to see this endpoint.")

    def get_serializer_context(self):
        return {'request': self.request}



class InstructorViewSet(ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = InstructorFilter
    pagination_class = DefaultPagination

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        user = self.request.user

        # Exclude the logged-in instructor's information if the user is an instructor
        if user.role == 'instructor':
            return self.queryset.exclude(user=user)

        return self.queryset

    def destroy(self, request, *args, **kwargs):
        # Check if the user is staff
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this object.")

        # Proceed with the default destroy method if user is staff
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Only allow users with is_staff = True to update the student object
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this object.")
        # Proceed with the update if user has is_staff = True
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Only allow users with is_staff = True to update the student object
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to update this object.")
        # Proceed with the update if user has is_staff = True
        return super().create(request, *args, **kwargs)
