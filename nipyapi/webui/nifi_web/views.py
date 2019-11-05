import os

from django.db.models import Q
from django.http import JsonResponse
from nifi_web.bg_tasks import perform_cloud_ops
from nifi_web.models import NifiInstance, K8sCluster, NifiImage, NifiImageBuild
from nifi_web.serializers import NifiInstanceSerializer, K8sClusterSerializer, NifiInstanceDeepSerializer, \
    NifiImageSerializer, NifiImageBuildSerializer
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


class NifiImageBuildList(generics.ListAPIView):
    queryset = NifiImageBuild.objects.all()
    serializer_class = NifiImageBuildSerializer


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
