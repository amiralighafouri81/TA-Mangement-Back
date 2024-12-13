from django.contrib import admin
from django.urls import re_path, path, include
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="TA Management API's",
        default_version="v1",
        description="API documentation for your project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

admin.AdminSite.site_header = "TA Management Admin"
admin.AdminSite.index_title = "Admin"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('faculty/', include('faculty.urls')),
    path('course/', include('course.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/v1/',  # Added trailing slash
         include([
             path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
         ])
         ),
]

