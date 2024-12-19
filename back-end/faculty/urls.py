from django.urls import path
from rest_framework_nested import routers
from . import views

urlpatterns = [
    path('students/', views.student_list),
    path('students/<int:id>/', views.student_detail),
    path('instructors/', views.instructor_list),
    path('instructors/<int:id>/', views.instructor_detail),
    path('courses/', views.course_list),
    path('courses/<int:id>/', views.course_detail),

]
