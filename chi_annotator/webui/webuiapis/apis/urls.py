from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register(r'annotation_data', views.AnnotationDataViewSet)

urlpatterns = [
    # First index page ####################################################
    path('project_info/', views.project_info, name='project_info'),
    path('upload_remote_file/', views.upload_remote_file, name='upload_remote_file'),
    path('load_local_dataset/', views.load_local_dataset, name='load_local_dataset'),
    path('export_data/', views.export_data, name='export_data'),
    path('load_single_unlabeled/', views.load_single_unlabeled, name='load_single_unlabeled'),
    path('load_all_unlabeled/', views.load_all_unlabeled, name='load_all_unlabeled'),
    path('annotate_single_unlabeled/', views.annotate_single_unlabeled, name='annotate_single_unlabeled'),
    path('query_annotation_history/', views.query_annotation_history, name='query_annotation_history'),

]
