from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register(r'annotation_data', views.AnnotationDataViewSet)

urlpatterns = [
    # First index page ####################################################
    path('upload_remote_file/', views.upload_remote_file, name='upload_remote_file'),
    path('load_local_dataset/', views.load_local_dataset, name='load_local_dataset'),
    path('export_data/', views.export_data, name='export_data'),
    path('load_single_unlabeled/', views.load_single_unlabeled, name='load_single_unlabeled'),
]
