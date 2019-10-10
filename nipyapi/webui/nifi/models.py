from django.db import models


class K8sCluster(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    node_count = models.IntegerField()
    endpoint = models.CharField(max_length=2000)


class NifiInstance(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='PENDING_CREATE')
    cluster = models.ForeignKey(K8sCluster, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
