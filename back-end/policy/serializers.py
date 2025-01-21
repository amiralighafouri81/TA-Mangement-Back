from rest_framework import serializers
from .models import Policy


class StudentPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'key', 'value']
        read_only_fields = ['id', 'key', 'value']


class InstructorPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'key', 'value']
        read_only_fields = ['id', 'key', 'value']


class AdminPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'key', 'value']
        read_only_fields = ['id', 'key']
