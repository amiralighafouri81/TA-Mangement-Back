from rest_framework import serializers
from .models import Student, Instructor


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name','last_name', 'student_number', 'biography']

class SimpleStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id','first_name','last_name', 'student_number']

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['first_name','last_name', 'staff_id', 'way_of_communication', 'research_fields']

class SimpleInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id','first_name','last_name', 'staff_id']