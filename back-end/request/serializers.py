from rest_framework import serializers
from .models import Request
from faculty.serializers import SimpleStudentSerializer
from course.serializers import SimpleCourseSerializer


class StudentRequestSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Request
        fields = ['id', 'course', 'status', 'date']
        read_only_fields = fields

    def get_course(self, obj):
        return str(obj.course)

class InstructorRequestSerializer(serializers.ModelSerializer):
    student = SimpleStudentSerializer(read_only=True)
    course = SimpleCourseSerializer(read_only=True)
    class Meta:
        model = Request
        fields = ['id','student', 'course', 'status', 'date']
        read_only_fields = ['id', 'student', 'course', 'date']

    def get_course(self, obj):
        return str(obj.course)
