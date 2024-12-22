from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views


router = DefaultRouter()
router.register('courses', views.CourseViewSet, basename='courses')
urlpatterns = router.urls