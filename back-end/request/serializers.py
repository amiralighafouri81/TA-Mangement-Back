from rest_framework import serializers

from course.serializers import CourseSerializer
from faculty.serializers import SimpleStudentSerializer
from .models import Request


class RequestSerializer(serializers.ModelSerializer):
    student = SimpleStudentSerializer()
    course = CourseSerializer()
    class Meta:
        model = Request
        fields = ['id', 'course', 'student', 'status', 'date']