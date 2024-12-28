from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from faculty.models import Student, Instructor
from .models import Request
from .serializers import StudentRequestSerializer, InstructorRequestSerializer, AdminRequestSerializer
from .pagination import DefaultPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RequestFilter

class RequestViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RequestFilter
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        # Get the user role and return the corresponding serializer
        user = self.request.user
        if user.role == 'instructor':
            return InstructorRequestSerializer
        elif user.role == 'student':
            return StudentRequestSerializer
        elif user.role =='admin':
            return AdminRequestSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Request.objects.all()

        if user.role == 'student':
            # Only filter requests for the logged-in student
            student_id, created = Student.objects.only("id").get_or_create(user_id=user.id)
            return Request.objects.filter(student=student_id)

        elif user.role == 'instructor':
            # Get all courses taught by the current instructor
            instructor = Instructor.objects.get(user=user)
            courses = instructor.course_set.all()  # All courses where the instructor is teaching
            # Get all requests associated with these courses, excluding declined requests
            return Request.objects.filter(course__in=courses).exclude(status=Request.REQUSET_STATUS_DECLINED)
            # For other roles (admin, student), show all requests or adjust as necessary

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        # Get the Request instance
        request_instance = get_object_or_404(Request, pk=kwargs['pk'])
        user = request.user

        # Prevent instructors from deleting requests
        if user.role == 'instructor':
            raise PermissionDenied("Instructors are not allowed to delete requests.")

        # Prevent students from deleting accepted or declined requests
        if user.role == 'student' and request_instance.status in ['accepted', 'declined']:
            raise PermissionDenied("Students are not allowed to delete a request with accepted or declined status.")

        # Call the parent class's destroy method for other roles
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'instructor':
            raise PermissionDenied("Instructors are not allowed to create requests.")
        return super().create(request, *args, **kwargs)