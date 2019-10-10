from nifi.models import NifiInstance, K8sCluster
from nifi.serializers import NifiInstanceSerializer, K8sClusterSerializer
from rest_framework import generics


class NifiInstanceListCreate(generics.ListCreateAPIView):
    queryset = NifiInstance.objects.all()
    serializer_class = NifiInstanceSerializer


class NifiInstanceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NifiInstanceSerializer
    lookup_url_kwarg = 'nifi_instance_id'
    queryset = NifiInstance.objects.all()


class K8sClusterList(generics.ListAPIView):
    queryset = K8sCluster.objects.all()
    serializer_class = K8sClusterSerializer


class K8sClusterDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = K8sClusterSerializer
    lookup_url_kwarg = 'cluster_id'
    queryset = K8sCluster.objects.all()
