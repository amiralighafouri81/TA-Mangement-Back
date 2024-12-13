from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from .models import Course
from .serializers import CourseSerializer

@api_view()
def course_list(request):
    queryset = Course.objects.all()
    serializer = CourseSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view()
def course_detail(request, id):
    course = get_object_or_404(Course, pk=id)
    serializer = CourseSerializer(course)
    return Response(serializer.data)