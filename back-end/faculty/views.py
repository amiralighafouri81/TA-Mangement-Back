from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Student, Instructor, _delete_file
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

    def get_queryset(self, pk=None):

        user = self.request.user

        if user.role == 'instructor':
            return Student.objects.all()

        if user.role == 'student':
            if pk is None:
                return Student.objects.filter(user=user)
            else:
                return Student.objects.filter(id=pk)

        return Student.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        obj = Student.objects.filter(id=kwargs['pk']).first()
        old_resume_file = None
        if obj is not None:
            old_resume_file = obj.resume_file
        if old_resume_file is not None and old_resume_file.name is not None and old_resume_file.name != "":
            raise PermissionDenied("{0}".format(old_resume_file.path))
            _delete_file(old_resume_file.path)

        raise PermissionDenied("{0}".format(obj))

        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'instructor':
            raise PermissionDenied("instructors are not allowed to update students.")

        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['GET'])
    def download_file(self, request, pk):
        resume_file = Student.objects.filter(id=pk).first().resume_file
        file_path = resume_file.path
        response = FileResponse(open(file_path, "rb"))
        return response

    @action(detail=True, methods=['post', 'get'])
    def remove_resume(self, request, pk):
        student = Student.objects.filter(id=pk).first()
        resume_file = student.resume_file
        if resume_file is not None and resume_file.name is not None and resume_file.name != "":
            _delete_file(resume_file.path)
        student.resume_file = None
        student.save()
        return HttpResponse("remove_resume", status=200)


class InstructorViewSet(ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsAuthenticated]
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
