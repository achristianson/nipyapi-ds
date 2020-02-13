from nifi_web.models import K8sCluster, NifiImage, NifiImageBuild, DockerRegistryAuth, InstanceTypePort, \
    InstanceTypeEnvVar, InstanceType, ImageMirror, ImageMirrorJob, Instance, InstanceTypeIngressRoutedService
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


class ImageMirrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageMirror
        fields = '__all__'


class ImageMirrorJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageMirrorJob
        fields = '__all__'


class DockerRegistryAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = DockerRegistryAuth
        fields = '__all__'


class InstanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstanceType
        fields = '__all__'


class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = '__all__'


class InstanceTypeEnvVarSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstanceTypeEnvVar
        fields = '__all__'


class InstanceTypePortSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstanceTypePort
        fields = '__all__'


class InstanceTypeIngressRoutedServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstanceTypeIngressRoutedService
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
