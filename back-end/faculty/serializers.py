from rest_framework import serializers
from .models import Student, Instructor, Course


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user_id','first_name','last_name', 'student_number']

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id','first_name','last_name', 'user_id', 'staff_id']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'semester', 'instructor', 'name']