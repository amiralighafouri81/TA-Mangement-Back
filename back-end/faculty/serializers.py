from rest_framework import serializers

from course.models import Course
from request.models import Request
from .models import Student, Instructor


class StudentSerializer(serializers.ModelSerializer):
    accepted_requests = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'student_number', 'biography', 'resume_file', 'accepted_requests']
        read_only_fields = ['id', 'first_name', 'last_name']

    def get_accepted_requests(self, student):
        accepted_requests = Request.objects.filter(student=student, status=Request.REQUSET_STATUS_ACCEPTED)
        return SimpleRequestSerializer(accepted_requests, many=True).data


class TAStudentSerializer(StudentSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'student_number']


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'first_name', 'last_name', 'way_of_communication', 'research_fields', 'email']


class SimpleInstructorSerializer(InstructorSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'first_name', 'last_name', 'way_of_communication', 'research_fields']
        read_only_fields = ['way_of_communication', 'research_fields']


class SimpleCourseSerializer(serializers.ModelSerializer):
    instructor = SimpleInstructorSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'instructor', 'max_TA_number']
        read_only_fields = ['id', 'name', 'semester', 'instructor', 'max_TA_number']


class SimpleRequestSerializer(serializers.ModelSerializer):
    course = SimpleCourseSerializer(read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'student', 'course', 'status', 'date']
        read_only_fields = ['id', 'student', 'course', 'status', 'date']

    def get_course(self, obj):
        return str(obj.course)
