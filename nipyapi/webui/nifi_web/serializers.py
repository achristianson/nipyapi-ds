from nifi_web.models import K8sCluster, NifiImage, NifiImageBuild, DockerRegistryAuth
from nifi_web.models import NifiInstance
from rest_framework import serializers


class NifiInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NifiInstance
        fields = '__all__'


class NifiImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NifiImage
        fields = '__all__'


class DockerRegistryAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = DockerRegistryAuth
        fields = '__all__'


class NifiImageBuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = NifiImageBuild
        fields = '__all__'


class NifiInstanceDeepSerializer(serializers.ModelSerializer):
    class Meta:
        model = NifiInstance
        depth = 2
        fields = '__all__'


class K8sClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = K8sCluster
        fields = '__all__'
