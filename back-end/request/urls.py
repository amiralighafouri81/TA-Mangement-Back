from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views


router = DefaultRouter()
router.register('requests', views.RequestViewSet, basename='requests')
urlpatterns = router.urls