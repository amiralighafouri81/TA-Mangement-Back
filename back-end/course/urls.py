from django.urls import path
from rest_framework_nested import routers
from . import views

urlpatterns = [
    path('courses/', views.CourseList.as_view()),
    path('courses/<int:id>/', views.CourseDetail.as_view()),
]