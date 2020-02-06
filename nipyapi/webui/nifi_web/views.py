import os

from django.db.models import Q
from django.http import JsonResponse
from nifi_web.bg_tasks import perform_cloud_ops
from nifi_web.models import NifiInstance, K8sCluster, NifiImage, NifiImageBuild, DockerRegistryAuth, InstanceType, \
    InstanceTypeEnvVar, InstanceTypePort
from nifi_web.serializers import NifiInstanceSerializer, K8sClusterSerializer, NifiInstanceDeepSerializer, \
    NifiImageSerializer, NifiImageBuildSerializer, DockerRegistryAuthSerializer, InstanceTypeSerializer, \
    InstanceTypeEnvVarSerializer, InstanceTypePortSerializer
from rest_framework import generics


class NifiInstanceList(generics.ListAPIView):
    queryset = NifiInstance.objects.filter(~Q(state='DESTROYED'))
    serializer_class = NifiInstanceSerializer


class NifiInstanceCreate(generics.CreateAPIView):
    queryset = NifiInstance.objects.all()
    serializer_class = NifiInstanceSerializer


class NifiInstanceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NifiInstanceDeepSerializer
    lookup_url_kwarg = 'nifi_instance_id'
    queryset = NifiInstance.objects.all()


class K8sClusterList(generics.ListAPIView):
    queryset = K8sCluster.objects.all()
    serializer_class = K8sClusterSerializer


class K8sClusterDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = K8sClusterSerializer
    lookup_url_kwarg = 'cluster_id'
    queryset = K8sCluster.objects.all()


class NifiImageList(generics.ListAPIView):
    queryset = NifiImage.objects.all()
    serializer_class = NifiImageSerializer


class NifiImageCreate(generics.CreateAPIView):
    queryset = NifiImage.objects.all()
    serializer_class = NifiImageSerializer


class NifiImageDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NifiImageSerializer
    lookup_url_kwarg = 'nifi_image_id'
    queryset = NifiImage.objects.all()


class DockerRegistryAuthList(generics.ListAPIView):
    queryset = DockerRegistryAuth.objects.all()
    serializer_class = DockerRegistryAuthSerializer


class DockerRegistryAuthCreate(generics.CreateAPIView):
    queryset = DockerRegistryAuth.objects.all()
    serializer_class = DockerRegistryAuthSerializer


class DockerRegistryAuthDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DockerRegistryAuthSerializer
    lookup_url_kwarg = 'registry_auth_id'
    queryset = DockerRegistryAuth.objects.all()


class InstanceTypeList(generics.ListAPIView):
    queryset = InstanceType.objects.all()
    serializer_class = InstanceTypeSerializer


class InstanceTypeCreate(generics.CreateAPIView):
    queryset = InstanceType.objects.all()
    serializer_class = InstanceTypeSerializer


class InstanceTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstanceTypeSerializer
    lookup_url_kwarg = 'obj_id'
    queryset = InstanceType.objects.all()


class InstanceTypeEnvVarList(generics.ListAPIView):
    queryset = InstanceTypeEnvVar.objects.all()
    serializer_class = InstanceTypeEnvVarSerializer


class InstanceTypeEnvVarCreate(generics.CreateAPIView):
    queryset = InstanceTypeEnvVar.objects.all()
    serializer_class = InstanceTypeEnvVarSerializer


class InstanceTypeEnvVarDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstanceTypeEnvVarSerializer
    lookup_url_kwarg = 'obj_id'
    queryset = InstanceTypeEnvVar.objects.all()


class InstanceTypePortList(generics.ListAPIView):
    queryset = InstanceTypePort.objects.all()
    serializer_class = InstanceTypePortSerializer


class InstanceTypePortCreate(generics.CreateAPIView):
    queryset = InstanceTypePort.objects.all()
    serializer_class = InstanceTypePortSerializer


class InstanceTypePortDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstanceTypePortSerializer
    lookup_url_kwarg = 'obj_id'
    queryset = InstanceTypePort.objects.all()


class NifiImageBuildList(generics.ListAPIView):
    serializer_class = NifiImageBuildSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = NifiImageBuild.objects.all()
        image_id = self.request.query_params.get('image', None)
        if image_id is not None:
            queryset = queryset.filter(image=image_id)
        return queryset


class NifiImageBuildCreate(generics.CreateAPIView):
    queryset = NifiImageBuild.objects.all()
    serializer_class = NifiImageBuildSerializer


class NifiImageBuildDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NifiImageBuildSerializer
    lookup_url_kwarg = 'nifi_image_build_id'
    queryset = NifiImageBuild.objects.all()


def get_config(request):
    data = {
        'domain': os.getenv('DOMAIN'),
    }
    return JsonResponse(data)


def start_perform_cloud_ops(request):
    perform_cloud_ops()
    data = {
        'status': 'OK',
    }
    return JsonResponse(data)
