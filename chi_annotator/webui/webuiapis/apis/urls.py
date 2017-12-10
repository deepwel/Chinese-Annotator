from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from . import views

router = DefaultRouter()
# router.register(r'annotation_data', views.AnnotationDataViewSet)

urlpatterns = [
    # First index page ####################################################
    path('upload_remote_file/', views.upload_remote_file, name='upload_remote_file'),
    path('export_data/', views.export_data, name='export_data'),
]
