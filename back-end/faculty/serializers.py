from rest_framework import serializers
from .models import Student, Instructor


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user_id','first_name','last_name', 'student_number']

class SimpleStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id','first_name','last_name', 'student_number']

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id','first_name','last_name', 'user_id', 'staff_id']

class SimpleInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id','first_name','last_name', 'staff_id']