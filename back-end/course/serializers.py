from rest_framework import serializers
from faculty.serializers import SimpleInstructorSerializer
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    instructor = SimpleInstructorSerializer()
    class Meta:
        model = Course
        fields = ['id','name', 'instructor', 'semester']