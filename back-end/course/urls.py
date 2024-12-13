from django.urls import path
from rest_framework_nested import routers
from . import views

urlpatterns = [
    path('courses/', views.course_list),
    path('courses/<int:id>/', views.course_detail),
]