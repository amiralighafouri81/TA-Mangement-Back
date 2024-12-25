from rest_framework import serializers
from faculty.serializers import SimpleInstructorSerializer
from .models import Course
from request.models import Request


class CourseSerializer(serializers.ModelSerializer):
    head_TA = serializers.PrimaryKeyRelatedField(
        queryset=Request.objects.none(),  # Default queryset
        required=False,
        allow_null=True
    )

    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'instructor', 'head_TA']
        read_only_fields = ['id', 'name', 'semester', 'instructor']

    def get_head_TA_queryset(self, course):
        if course:
            # Filter requests for the course and ensure the status is 'accepted'
            return Request.objects.filter(course=course, status=Request.REQUSET_STATUS_ACCEPTED)
        return Request.objects.none()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        course = self.instance
        self.fields['head_TA'].queryset = self.get_head_TA_queryset(course)


class SimpleCourseSerializer(serializers.ModelSerializer):
    instructor = SimpleInstructorSerializer()
    class Meta:
        model = Course
        fields = ['id','name','semester', 'instructor']