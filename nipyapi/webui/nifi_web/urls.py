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
    path('api/nifi-image', views.NifiImageList.as_view()),
    path('api/nifi-image/new', views.NifiImageCreate.as_view()),
    path('api/nifi-image/<int:nifi_image_id>', views.NifiImageDetail.as_view()),
    path('api/nifi-image-build', views.NifiImageBuildList.as_view()),
    path('api/nifi-image-build/new', views.NifiImageBuildCreate.as_view()),
    path('api/nifi-image-build/<int:nifi_image_build_id>', views.NifiImageBuildDetail.as_view()),
    path('api/get-config', views.get_config),
    path('api/docker-registry-auth', views.DockerRegistryAuthList.as_view()),
    path('api/docker-registry-auth/new', views.DockerRegistryAuthCreate.as_view()),
    path('api/docker-registry-auth/<int:registry_auth_id>', views.DockerRegistryAuthDetail.as_view()),
]
