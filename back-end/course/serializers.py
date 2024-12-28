from rest_framework import serializers
from .models import Course
from request.models import Request
from faculty.serializers import TAStudentSerializer, SimpleInstructorSerializer
from faculty.models import Student


class CourseSerializer(serializers.ModelSerializer):
    accepted_students = serializers.SerializerMethodField()
    instructor = SimpleInstructorSerializer(read_only=True)
    head_TA = serializers.PrimaryKeyRelatedField(
        queryset=Request.objects.filter(status=Request.REQUSET_STATUS_ACCEPTED),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'instructor', 'head_TA', 'accepted_students']
        read_only_fields = ['id', 'name', 'semester', 'instructor']

    def get_accepted_students(self, obj):
        accepted_requests = Request.objects.filter(course=obj, status=Request.REQUSET_STATUS_ACCEPTED)
        student_ids = accepted_requests.values_list('student', flat=True)
        students = Student.objects.filter(id__in=student_ids)
        return TAStudentSerializer(students, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.head_TA:
            representation['head_TA'] = TAStudentSerializer(instance.head_TA.student).data
        return representation


class SimpleCourseSerializer(CourseSerializer):
    instructor = SimpleInstructorSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'instructor']
        read_only_fields = ['id', 'name', 'semester', 'instructor']