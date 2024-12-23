from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from faculty.models import Student, Instructor
from core.models import User


class UserCreateSerializer(BaseUserCreateSerializer):
    student_number = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'username',
            'student_number', 'password', 'password_confirmation'
        ]

    def validate(self, attrs):
        self.student_number = attrs.pop('student_number', None)
        if attrs['password'] != attrs.pop('password_confirmation'):
            raise serializers.ValidationError({"password_confirmation": "Passwords do not match."})
        return super().validate(attrs)

    def create(self, validated_data):
        user = super().create(validated_data)

        user.role = User.STUDENT  # Set role to 'Student'
        user.save()

        if self.student_number:
            Student.objects.create(user=user, student_number=self.student_number)

        return user


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['username', 'first_name', 'last_name', 'role']  # Include role for clarity

    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)

        # Add student-specific fields if the user is a student
        if instance.role == User.STUDENT:
            try:
                student = Student.objects.get(user=instance)
                representation.update({
                    'student_number': student.student_number,
                    'biography': student.biography,
                })
            except Student.DoesNotExist:
                representation.update({
                    'student_number': None,
                    'biography': None,
                })

        # Add instructor-specific fields if the user is an instructor
        elif instance.role == User.INSTRUCTOR:
            try:
                instructor = Instructor.objects.get(user=instance)
                representation.update({
                    'staff_id': instructor.staff_id,
                    'way_of_communication': instructor.way_of_communication,
                    'research_fields': instructor.research_fields,
                })
            except Instructor.DoesNotExist:
                representation.update({
                    'staff_id': None,
                    'way_of_communication': None,
                    'research_fields': None,
                })

        return representation
