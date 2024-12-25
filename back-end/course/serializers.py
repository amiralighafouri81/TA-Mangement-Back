from rest_framework import serializers
from faculty.serializers import SimpleInstructorSerializer
from .models import Course
from request.models import Request


class CourseSerializer(serializers.ModelSerializer):
    head_TA = serializers.PrimaryKeyRelatedField(
        queryset=Request.objects.filter(status=Request.REQUSET_STATUS_ACCEPTED),  # Filter requests with 'accepted' status
        required=False,
        allow_null=True
    )

    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'instructor', 'head_TA']
        read_only_fields = ['id', 'name', 'semester', 'instructor']


class SimpleCourseSerializer(serializers.ModelSerializer):
    instructor = SimpleInstructorSerializer()
    class Meta:
        model = Course
        fields = ['id','name','semester', 'instructor']