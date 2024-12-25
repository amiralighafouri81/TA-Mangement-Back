from rest_framework import serializers
from .models import Request
from faculty.models import Student



class StudentRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ['id', 'course', 'status', 'date']
        read_only_fields = ['status']

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
        fields = ['id','student', 'course', 'status', 'date']
        read_only_fields = ['id', 'student', 'course', 'date']

    def get_course(self, obj):
        return str(obj.course)

class AdminRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id','student', 'course', 'status', 'date']

    def get_course(self, obj):
        return str(obj.course)
