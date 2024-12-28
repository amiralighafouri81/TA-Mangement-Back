from rest_framework import serializers
from .models import Course
from request.models import Request
from faculty.serializers import TAStudentSerializer, SimpleInstructorSerializer
from faculty.models import Student


class CourseSerializer(serializers.ModelSerializer):
    # head_TA = serializers.PrimaryKeyRelatedField(
    #     queryset=Request.objects.none(),  # Initialize with an empty queryset
    #     required=False,
    #     allow_null=True
    # )
    accepted_students = serializers.SerializerMethodField()
    instructor = SimpleInstructorSerializer(read_only=True)
    head_TA = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'instructor', 'head_TA', 'accepted_students']
        read_only_fields = ['id', 'name', 'semester', 'instructor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.role == 'instructor':
            instructor_courses = Course.objects.filter(instructor__user=request.user)
            if self.instance and self.instance in instructor_courses:
                self.fields['head_TA'].queryset = Request.objects.filter(
                    course=self.instance,
                    status=Request.REQUSET_STATUS_ACCEPTED
                )

    def get_accepted_students(self, obj):
        # Fetch accepted requests for the course
        accepted_requests = Request.objects.filter(course=obj, status=Request.REQUSET_STATUS_ACCEPTED)

        # Get the actual Student objects using the student IDs
        student_ids = accepted_requests.values_list('student', flat=True)
        students = Student.objects.filter(id__in=student_ids)

        # Use the TAStudentSerializer to serialize the list of students
        return TAStudentSerializer(students, many=True).data

    def get_head_TA(self, obj):
        if obj.head_TA:
            return TAStudentSerializer(obj.head_TA.student).data  # Assuming `head_TA` has a `student` field
        return None  # Return `None` if there is no head TA



class SimpleCourseSerializer(CourseSerializer):
    instructor = SimpleInstructorSerializer(read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'instructor']
        read_only_fields = ['id', 'name', 'semester', 'instructor']