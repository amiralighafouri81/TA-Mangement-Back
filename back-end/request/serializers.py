from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import Request
from faculty.models import Student
from faculty.serializers import StudentSerializer
from course.models import Course  # Ensure to import your Course model
from course.serializers import SimpleCourseSerializer

class StudentRequestSerializer(serializers.ModelSerializer):
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )
    course = SimpleCourseSerializer(read_only=True)
    message = serializers.SerializerMethodField()

    class Meta:
        model = Request
        fields = ['id', 'course_id', 'course', 'score', 'status', 'date', 'message']
        read_only_fields = ['status', 'message']

    def validate(self, data):
        user = self.context['request'].user
        student, created = Student.objects.get_or_create(user=user)

        # Check if a request with the same course and student already exists
        if Request.objects.filter(course=data['course'], student=student).exists():
            raise PermissionDenied("You have already made a request for this course.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        student, created = Student.objects.get_or_create(user=user)
        validated_data['student'] = student

        # Check the course condition
        course = validated_data['course']
        if course.condition is not None and validated_data['score'] < course.condition:
            validated_data['status'] = 'declined'
            # Add a custom message to the context
            self.context['message'] = (
                f"Your request was declined because your score ({validated_data['score']}) "
                f"is lower than the required score for this course."
            )
        else:
            validated_data['status'] = 'pending'

        return super().create(validated_data)

    def get_message(self, obj):
        # Return the custom message if available in the context
        return self.context.get('message', '')

    def get_course(self, obj):
        return str(obj.course)

class InstructorRequestSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = SimpleCourseSerializer(read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'student', 'course', 'score', 'status', 'date']
        read_only_fields = ['id', 'student', 'course', 'date', 'score']

    def get_course(self, obj):
        return str(obj.course)

class AdminRequestSerializer(serializers.ModelSerializer):
    course = SimpleCourseSerializer(read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'student', 'course', 'status', 'date']

    def get_course(self, obj):
        return str(obj.course)
