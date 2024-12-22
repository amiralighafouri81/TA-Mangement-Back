from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from .models import Request
from .serializers import CourseSerializer

class RequestList(APIView):
    def get(self, request):
        queryset = Request.objects.all()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RequestDetail(APIView):
    def get(self, request, id):
        request = get_object_or_404(Request, pk=id)
        serializer = CourseSerializer(request)
        return Response(serializer.data)
    def put(self, request, id):
        request = get_object_or_404(Request, pk=id)
        serializer = CourseSerializer(request, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self, request, id):
        request = get_object_or_404(Request, pk=id)
        request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)