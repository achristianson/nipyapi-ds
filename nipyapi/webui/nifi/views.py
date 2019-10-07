from nifi.models import NifiInstance
from nifi.serializers import NifiInstanceSerializer
from rest_framework import generics


class NifiInstanceListCreate(generics.ListCreateAPIView):
    queryset = NifiInstance.objects.all()
    serializer_class = NifiInstanceSerializer


class NifiInstanceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NifiInstanceSerializer
    lookup_url_kwarg = 'nifi_instance_id'
    queryset = NifiInstance.objects.all()
