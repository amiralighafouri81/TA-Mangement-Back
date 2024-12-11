from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from faculty.models import Student
from core.models import User


class UserCreateSerializer(BaseUserCreateSerializer):
    student_number = serializers.CharField(write_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password','student_number', 'email')

    def validate(self, attrs):
        # Extract student_number to avoid it being passed to User model creation
        self.student_number = attrs.pop('student_number', None)
        return super().validate(attrs)

    def create(self, validated_data):
        # Create the User instance
        user = super().create(validated_data)

        # Create a Student instance and associate it with the user
        if self.student_number:
            Student.objects.create(user=user, student_number=self.student_number)

        return user


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
