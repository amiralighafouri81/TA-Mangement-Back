from rest_framework.viewsets import ModelViewSet
from .models import Student, Instructor
from rest_framework.exceptions import PermissionDenied
from .serializers import StudentSerializer, InstructorSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import DefaultPagination
from .filters import InstructorFilter


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

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

    def destroy(self, request, *args, **kwargs):
        # Check if the user is staff
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this object.")

        # Proceed with the default destroy method if user is staff
        return super().destroy(request, *args, **kwargs)
