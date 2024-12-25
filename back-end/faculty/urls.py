from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter

router = DefaultRouter()
router.register('students', views.StudentViewSet, basename='students')
router.register('instructors', views.InstructorViewSet)
urlpatterns = router.urls
