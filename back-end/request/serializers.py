from rest_framework import serializers
from .models import Request


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'course', 'student', 'status', 'date']