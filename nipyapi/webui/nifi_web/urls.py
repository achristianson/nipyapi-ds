from django.urls import path
from . import views

urlpatterns = [
    path('api/nifi', views.NifiInstanceList.as_view()),
    path('api/nifi/new', views.NifiInstanceCreate.as_view()),
    path('api/nifi/<int:nifi_instance_id>', views.NifiInstanceDetail.as_view()),
    path('api/k8s-cluster', views.K8sClusterList.as_view()),
    path('api/k8s-cluster/<int:cluster_id>', views.K8sClusterDetail.as_view()),
    path('api/perform-cloud-ops', views.start_perform_cloud_ops),
    path('api/get-config', views.get_config),
]
