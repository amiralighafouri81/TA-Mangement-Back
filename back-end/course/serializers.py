from rest_framework import serializers
from .models import Course
from request.models import Request
from faculty.serializers import TAStudentSerializer, SimpleInstructorSerializer
from faculty.models import Student


class StudentCourseSerializer(serializers.ModelSerializer):
    accepted_students = serializers.SerializerMethodField()
    instructor = SimpleInstructorSerializer(read_only=True)
    head_TA = serializers.PrimaryKeyRelatedField(
        queryset=Request.objects.filter(status=Request.REQUSET_STATUS_ACCEPTED),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'instructor', 'max_TA_number', 'head_TA', 'accepted_students']
        read_only_fields = ['id', 'name', 'semester', 'instructor', 'max_TA_number']

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

class InstructorCourseSerializer(serializers.ModelSerializer):
    accepted_students = serializers.SerializerMethodField()
    head_TA = serializers.PrimaryKeyRelatedField(
        queryset=Request.objects.filter(status=Request.REQUSET_STATUS_ACCEPTED),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'condition', 'max_TA_number', 'head_TA', 'accepted_students']
        read_only_fields = ['id', 'name', 'semester']

    def get_accepted_students(self, obj):
        # Get the accepted requests for students
        accepted_requests = Request.objects.filter(course=obj, status=Request.REQUSET_STATUS_ACCEPTED)
        student_ids = accepted_requests.values_list('student', flat=True)
        students = Student.objects.filter(id__in=student_ids)
        return TAStudentSerializer(students, many=True).data

    def to_representation(self, instance):
        # Dynamically set the queryset for head_TA based on the course
        self.fields['head_TA'].queryset = Request.objects.filter(
            status=Request.REQUSET_STATUS_ACCEPTED,
            course=instance
        )

        # Call the default to_representation method
        representation = super().to_representation(instance)

        # Include detailed head_TA info if present
        if instance.head_TA:
            # Assuming head_TA is a Request object, and we want the student related to it
            representation['head_TA'] = TAStudentSerializer(instance.head_TA.student).data

        return representation



class AdminCourseSerializer(serializers.ModelSerializer):
    accepted_students = serializers.SerializerMethodField()
    instructor = SimpleInstructorSerializer(read_only=True)
    head_TA = serializers.PrimaryKeyRelatedField(
        queryset=Request.objects.filter(status=Request.REQUSET_STATUS_ACCEPTED),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'instructor', 'condition', 'max_TA_number', 'head_TA', 'accepted_students']

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

class SimpleCourseSerializer(StudentCourseSerializer):
    instructor = SimpleInstructorSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'instructor', 'max_TA_number']
        read_only_fields = ['id', 'name', 'semester', 'instructor', 'max_TA_number']