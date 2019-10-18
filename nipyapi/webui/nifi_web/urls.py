from django.urls import path
from . import views

urlpatterns = [
    path('api/nifi', views.NifiInstanceList.as_view()),
    path('api/nifi/new', views.NifiInstanceCreate.as_view()),
    path('api/nifi/<int:nifi_instance_id>', views.NifiInstanceDetail.as_view()),
    path('api/k8s-cluster', views.K8sClusterList.as_view()),
    path('api/k8s-cluster/<int:cluster_id>', views.K8sClusterDetail.as_view()),
]
