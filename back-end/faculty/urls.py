from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter

urlpatterns = [
    path('students/', views.student_list),
    path('students/<int:id>/', views.student_detail),
    path('instructors/', views.instructor_list),
    path('instructors/<int:id>/', views.instructor_detail),
    path('courses/', views.course_list),
    path('courses/<int:id>/', views.course_detail),

]

router = DefaultRouter()
router.register('students', views.StudentViewSet)
router.register('instructors', views.InstructorViewSet)
urlpatterns = router.urls
