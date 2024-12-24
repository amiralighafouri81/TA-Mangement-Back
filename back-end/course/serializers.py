from rest_framework import serializers
from faculty.serializers import SimpleInstructorSerializer
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    instructor = SimpleInstructorSerializer()
    class Meta:
        model = Course
        fields = ['id','name','semester', 'instructor', 'condition']

class SimpleCourseSerializer(serializers.ModelSerializer):
    instructor = SimpleInstructorSerializer()
    class Meta:
        model = Course
        fields = ['id','name','semester', 'instructor']