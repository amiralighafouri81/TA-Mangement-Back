from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from course.models import Course
from faculty.models import Student, Instructor
from policy.models import Policy
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
        user = self.request.user
        if user.role == 'instructor':
            return InstructorRequestSerializer
        elif user.role == 'student':
            return StudentRequestSerializer
        elif user.role == 'admin':
            return AdminRequestSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.role == 'admin':
            return Request.objects.all()

        if user.role == 'student':
            # Fetch only the student's requests
            student, _ = Student.objects.get_or_create(user=user)
            return Request.objects.filter(student=student)

        elif user.role == 'instructor':
            # Fetch courses taught by the instructor
            instructor = Instructor.objects.get(user=user)
            courses = instructor.course_set.all()

            # Filter requests for these courses, excluding declined ones
            return Request.objects.filter(course__in=courses).exclude(status=Request.REQUSET_STATUS_DECLINED)

    def get_serializer_context(self):
        return {'request': self.request}

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        user = self.request.user

        if user.role == 'student':
            student, _ = Student.objects.get_or_create(user=user)
            requested_courses = Request.objects.filter(student=student).values_list('course_id', flat=True)
            return queryset.filter(course_id__in=requested_courses)

        elif user.role == 'instructor':
            instructor = Instructor.objects.get(user=user)
            taught_courses = instructor.course_set.values_list('id', flat=True)
            return queryset.filter(course_id__in=taught_courses).exclude(status=Request.REQUSET_STATUS_DECLINED)

        return queryset

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

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'student':
            raise PermissionDenied("Students are not allowed to update requests.")
        new_status = request.POST.get('status')
        old_request = get_object_or_404(Request, pk=kwargs['pk'])
        course = old_request.course
        student_id = old_request.student_id
        if new_status == Request.REQUSET_STATUS_ACCEPTED:
            if course.max_TA_number is not None and \
                    Request.objects.filter(course_id=course.id, status=Request.REQUSET_STATUS_ACCEPTED).count() >= course.max_TA_number:
                raise PermissionDenied("The capacity of teaching assistants is the completion period")
            maximum_number_of_course_for_ta = Policy.objects.filter(key="MaximumNumberOfCourseForTA").first()
            if maximum_number_of_course_for_ta is not None and maximum_number_of_course_for_ta.value <= \
                    Request.objects.filter(student_id=student_id, status=Request.REQUSET_STATUS_ACCEPTED, course__semester__exact=course.semester).count():
                raise PermissionDenied("student already reach to the maximum number of course for TA")
        return super().update(request, *args, **kwargs)
