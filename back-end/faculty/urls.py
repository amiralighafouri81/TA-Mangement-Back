from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.student_list, name='student-list'),
    path('students/<int:id>/', views.student_detail, name='student-detail'),
    path('instructors/', views.instructor_list, name='instructor-list'),
    path('instructors/<int:id>/', views.instructor_detail, name='instructor-detail'),
]
