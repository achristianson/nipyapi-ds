from django.db import models


class K8sCluster(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    node_count = models.IntegerField()
    endpoint = models.CharField(max_length=2000)
    object = models.BinaryField(null=True)


class NifiInstance(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=1000, default='apache/nifi:latest')
    hostname = models.CharField(max_length=100)
    namespace = models.CharField(max_length=100)
    deploy_mongo = models.BooleanField(default=False)
    deploy_kafka = models.BooleanField(default=False)
    deploy_prometheus = models.BooleanField(default=False)
    deploy_jupyter = models.BooleanField(default=False)
    jupyter_token = models.CharField(max_length=1000, null=True)
    state = models.CharField(max_length=100, default='PENDING_CREATE')
    cluster = models.ForeignKey(K8sCluster, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class NifiImage(models.Model):
    git_repo = models.CharField(max_length=1000)
    branch = models.CharField(max_length=1000)
    mvn_build_args = models.CharField(max_length=1000)
    tag = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)


class NifiImageBuild(models.Model):
    image = models.ForeignKey(NifiImage, on_delete=models.CASCADE)
    state = models.CharField(max_length=100, default='PENDING_BUILD')
    docker_id = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class DockerRegistryAuth(models.Model):
    name = models.CharField(max_length=1000, null=False)
    username = models.CharField(max_length=1000, null=False)
    password = models.CharField(max_length=1000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class ImageMirror(models.Model):
    from_image = models.CharField(max_length=1000, null=False)
    to_image = models.CharField(max_length=1000, null=False)
    auth = models.ForeignKey(DockerRegistryAuth, null=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class ImageMirrorJob(models.Model):
    mirror = models.ForeignKey(ImageMirror, on_delete=models.CASCADE)
    state = models.CharField(max_length=100, default='PENDING_MIRROR')
    docker_id = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class InstanceType(models.Model):
    name = models.CharField(max_length=100)
    container_name = models.CharField(max_length=100)
    image = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)


class Instance(models.Model):
    instance_type = models.ForeignKey(InstanceType, on_delete=models.PROTECT)
    parent = models.ForeignKey(NifiInstance, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class InstanceTypeEnvVar(models.Model):
    instance_type = models.ForeignKey(InstanceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, null=False)
    default_value = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class InstanceTypePort(models.Model):
    instance_type = models.ForeignKey(InstanceType, on_delete=models.CASCADE)
    internal = models.IntegerField()
    external = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class InstanceTypeIngressRoutedService(models.Model):
    instance_type = models.ForeignKey(InstanceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, null=False)
    service_name = models.CharField(max_length=100)
    svc_port = models.IntegerField()
    target_port = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class InstanceTypeIngressRoutedServiceURI(models.Model):
    instance_type_svc = models.ForeignKey(InstanceTypeIngressRoutedService, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, null=False)
    path = models.CharField(max_length=1000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
