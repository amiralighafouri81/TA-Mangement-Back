from rest_framework import serializers
from .models import Request
from faculty.models import Student
from rest_framework.exceptions import PermissionDenied




class StudentRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ['id', 'course', 'score', 'status', 'date']
        read_only_fields = ['status']

    def validate(self, data):
        # Get the currently logged-in user
        user = self.context['request'].user

        # Get or create the student object related to the logged-in user
        student, created = Student.objects.get_or_create(user=user)

        # Check if a request with the same course and student already exists
        if Request.objects.filter(course=data['course'], student=student).exists():
            raise PermissionDenied("You have already made a request for this course.")

        course = data['course']
        if course.condition is not None and data['score'] < course.condition:
            raise PermissionDenied(
                f"Your score ({data['score']}) is below the required condition ({course.condition}) for this course."
            )

        return data

    def create(self, validated_data):
        # Get the currently logged-in user
        user = self.context['request'].user

        # Get or create the student object related to the logged-in user
        student, created = Student.objects.get_or_create(user=user)

        # Add the student to the validated data
        validated_data['student'] = student

        # Call the parent class's create method to save the request
        return super().create(validated_data)

class InstructorRequestSerializer(serializers.ModelSerializer):
    # student = SimpleStudentSerializer(read_only=True)
    # course = SimpleCourseSerializer(read_only=True)
    class Meta:
        model = Request
        fields = ['id','student', 'course', 'score', 'status', 'date']
        read_only_fields = ['id', 'student', 'course', 'date', 'score']

    def get_course(self, obj):
        return str(obj.course)

class AdminRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id','student', 'course', 'status', 'date']

    def get_course(self, obj):
        return str(obj.course)
