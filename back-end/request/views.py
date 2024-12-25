from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from faculty.models import Student, Instructor
from .models import Request
from .serializers import StudentRequestSerializer, InstructorRequestSerializer


class RequestViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # Get the user role and return the corresponding serializer
        user = self.request.user
        if user.role == 'instructor':
            return InstructorRequestSerializer
        return StudentRequestSerializer  # Default to StudentRequestSerializer if role is student

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

            # Get all requests associated with these courses
            return Request.objects.filter(course__in=courses)

    def get_serializer_context(self):
        return {'request': self.request}
