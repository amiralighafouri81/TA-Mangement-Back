from rest_framework import serializers
from faculty.serializers import SimpleInstructorSerializer
from .models import Course
from request.models import Request


class CourseSerializer(serializers.ModelSerializer):
    head_TA = serializers.PrimaryKeyRelatedField(
        queryset=Request.objects.none(),  # Initialize with an empty queryset
        required=False,
        allow_null=True
    )

    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'instructor', 'head_TA']
        read_only_fields = ['id', 'name', 'semester', 'instructor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.role == 'instructor':
            # Fetch the instructor's course based on the course being updated
            instructor_courses = Course.objects.filter(instructor__user=request.user)
            if self.instance and self.instance in instructor_courses:
                # Filter requests for the course with 'accepted' status
                self.fields['head_TA'].queryset = Request.objects.filter(
                    course=self.instance,
                    status=Request.REQUSET_STATUS_ACCEPTED
                )


class SimpleCourseSerializer(serializers.ModelSerializer):
    instructor = SimpleInstructorSerializer()
    class Meta:
        model = Course
        fields = ['id','name','semester', 'instructor']