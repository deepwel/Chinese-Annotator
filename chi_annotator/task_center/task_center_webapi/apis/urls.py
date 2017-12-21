from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    # First index page ####################################################
    path('test_connect/', views.test_connect, name='test_connect'),
]