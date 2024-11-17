from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from .models import Student, Instructor
from .serializers import StudentSerializer, InstructorSerializer

@api_view()
def student_list(request):
    queryset = Student.objects.all()
    serializer = StudentSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view()
def student_detail(request, id):
    student = get_object_or_404(Student, pk=id)
    serializer = StudentSerializer(student)
    return Response(serializer.data)

@api_view()
def instructor_list(request):
    queryset = Instructor.objects.all()
    serializer = InstructorSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view()
def instructor_detail(request, id):
    instructor = get_object_or_404(Instructor, pk=id)
    serializer = InstructorSerializer(instructor)
    return Response(serializer.data)
