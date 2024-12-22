from django.urls import path
from rest_framework_nested import routers
from . import views

urlpatterns = [
    path('requests/', views.RequestList.as_view()),
    path('requests/<int:id>/', views.RequestDetail.as_view()),
]