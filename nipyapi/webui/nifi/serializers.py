from rest_framework import serializers
from nifi.models import NifiInstance


class NifiInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NifiInstance
        fields = '__all__'
