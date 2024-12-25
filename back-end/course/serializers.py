from rest_framework import serializers
from faculty.serializers import SimpleInstructorSerializer
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','name','semester', 'instructor']
        read_only_fields = ['id','name','semester', 'instructor']

class SimpleCourseSerializer(serializers.ModelSerializer):
    instructor = SimpleInstructorSerializer()
    class Meta:
        model = Course
        fields = ['id','name','semester', 'instructor']