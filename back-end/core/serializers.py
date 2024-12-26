from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from faculty.models import Student, Instructor
from core.models import User
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError as DRFValidationError


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
            raise DRFValidationError({"password_confirmation": "Passwords do not match."})
        return super().validate(attrs)

    def create(self, validated_data):
        user = super().create(validated_data)

        user.role = User.STUDENT  # Set role to 'Student'
        user.save()

        if self.student_number:
            try:
                # Try to create the student object
                Student.objects.create(user=user, student_number=self.student_number)
            except IntegrityError:
                # Catch the duplicate entry error and raise a ValidationError
                raise DRFValidationError({"student_number": "A student with that student number already exists."})

        return user

class UserSerializer(BaseUserSerializer):
    student_number = serializers.CharField(required=False, allow_null=True)
    biography = serializers.CharField(required=False, allow_null=True)
    staff_id = serializers.CharField(required=False, allow_null=True)
    way_of_communication = serializers.CharField(required=False, allow_null=True)
    research_fields = serializers.CharField(required=False, allow_null=True)

    class Meta(BaseUserSerializer.Meta):
        fields = [
            'username', 'first_name', 'last_name', 'role',  # Base fields
            'student_number', 'biography',  # Student fields
            'staff_id', 'way_of_communication', 'research_fields'  # Instructor fields
        ]
        read_only_fields = ['role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically remove irrelevant fields based on the user's role
        instance = self.instance

        if instance and hasattr(instance, 'role'):
            if instance.role == User.STUDENT:
                # Remove instructor-specific fields
                self.fields.pop('staff_id', None)
                self.fields.pop('way_of_communication', None)
                self.fields.pop('research_fields', None)
            elif instance.role == User.INSTRUCTOR:
                # Remove student-specific fields
                self.fields.pop('student_number', None)
                self.fields.pop('biography', None)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

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

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        if instance.role == User.STUDENT:
            student_data = {
                'student_number': validated_data.get('student_number'),
                'biography': validated_data.get('biography'),
            }
            student, created = Student.objects.get_or_create(user=instance)
            for field, value in student_data.items():
                if value is not None:
                    setattr(student, field, value)
            student.save()

        elif instance.role == User.INSTRUCTOR:
            instructor_data = {
                'staff_id': validated_data.get('staff_id'),
                'way_of_communication': validated_data.get('way_of_communication'),
                'research_fields': validated_data.get('research_fields'),
            }
            instructor, created = Instructor.objects.get_or_create(user=instance)
            for field, value in instructor_data.items():
                if value is not None:
                    setattr(instructor, field, value)
            instructor.save()

        return instance

    def validate(self, attrs):
        role = self.instance.role if self.instance else attrs.get('role', None)

        if role == User.STUDENT:
            student = Student.objects.filter(user=self.instance).first()

            # Only validate student_number if it's being updated and it exists
            if 'student_number' in attrs and attrs['student_number'] != (student.student_number if student else None):
                if Student.objects.filter(student_number=attrs['student_number']).exclude(user=self.instance).exists():
                    raise DRFValidationError({"student_number": "A student with that student number already exists."})

        elif role == User.INSTRUCTOR:
            instructor = Instructor.objects.filter(user=self.instance).first()

            # Only validate staff_id if it's being updated and it exists
            if 'staff_id' in attrs and attrs['staff_id'] != (instructor.staff_id if instructor else None):
                if Instructor.objects.filter(staff_id=attrs['staff_id']).exclude(user=self.instance).exists():
                    raise DRFValidationError({"staff_id": "An instructor with that staff ID already exists."})

        return super().validate(attrs)
