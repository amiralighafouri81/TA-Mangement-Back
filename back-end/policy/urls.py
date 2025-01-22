from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views


router = DefaultRouter()
router.register('policies', views.PolicyViewSet, basename='policies')
urlpatterns = router.urls