import logging
import os
import pickle
from base64 import b64encode

import google.auth
import urllib3
from background_task import background
from google.cloud import container_v1
from kubernetes import client
from kubernetes.client import V1Container, V1EnvVar, V1ContainerPort, V1VolumeMount, V1StorageClass, V1ObjectMeta, \
    V1SecurityContext, V1Secret, V1Volume, V1ProjectedVolumeSource, V1VolumeProjection, V1SecretProjection, V1KeyToPath
from nifi_web.docker.img_builder import perform_build_ops_bg
from nifi_web.k8s.general import auth_gcloud_k8s, ensure_single_container_deployment, \
    ensure_ingress_routed_svc, destroy_ingress_routed_svc, destroy_deployment, ensure_single_container_statefulset, \
    destroy_statefulset, ensure_storage_class, ensure_secret
from nifi_web.k8s.traefik import ensure_traefik
from nifi_web.models import K8sCluster, NifiInstance

logger = logging.getLogger(__name__)


def create_nifi_ss_object():
    container = client.V1Container(
        name="apache",
        image="apache/nifi:1.9.2",
        env=[client.V1EnvVar(name='NIFI_WEB_HTTP_HOST', value='0.0.0.0')],
        ports=[client.V1ContainerPort(container_port=8080)])
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "nifi"}),
        spec=client.V1PodSpec(containers=[container]))
    spec = client.V1StatefulSetSpec(
        replicas=1,
        service_name='nifi',
        template=template,
        selector={'matchLabels': {'app': 'nifi'}})
    ss = client.V1StatefulSet(
        api_version="apps/v1",
        kind="StatefulSet",
        metadata=client.V1ObjectMeta(name='nifi'),
        spec=spec
    )

    return ss


def scan_clusters(client, project_id):
    zone = '-'
    response = client.list_clusters(project_id, zone)
    clusters = response.clusters
    for c in clusters:
        obj, created = K8sCluster.objects.update_or_create(
            name=c.name,
            defaults={
                'status': c.status,
                'location': c.location,
                'node_count': c.current_node_count,
                'endpoint': c.endpoint,
                'object': pickle.dumps(c)
            })
        if created:
            logger.info('Created cluster %s', obj.name)
        else:
            logger.info('Updated cluster %s', obj.name)


@background(schedule=0, remove_existing_tasks=True)
def perform_cloud_ops():
    # set GOOGLE_APPLICATION_CREDENTIALS env to credentials file
    # set GOOGLE_CLOUD_PROJECT env to project id

    domain = os.getenv('DOMAIN')
    assert domain
    logger.info(f'using domain: {domain}')

    static_ip = os.getenv('STATIC_IP')
    assert static_ip
    logger.info(f'using static IP: {static_ip}')

    admin_email = os.getenv('ADMIN_EMAIL')
    assert admin_email
    logger.info(f'using ACME admin email: {admin_email}')

    oauth_client_id = os.getenv('OAUTH_CLIENT_ID')
    assert oauth_client_id
    logger.info(f'using oauth client id: {oauth_client_id}')

    oauth_client_secret = os.getenv('OAUTH_CLIENT_SECRET')
    assert oauth_client_secret
    logger.info(f'using oauth client secret: {oauth_client_secret}')

    oauth_secret = os.getenv('OAUTH_SECRET')
    assert oauth_secret
    logger.info(f'using oauth secret: {oauth_secret}')

    oauth_domain = os.getenv('OAUTH_DOMAIN')
    assert oauth_domain
    logger.info(f'using domain: {oauth_domain}')

    django_secret_key = os.getenv('DJANGO_SECRET_KEY')
    assert django_secret_key
    logger.info(f'using DJANGO_SECRET_KEY: {django_secret_key}')

    credentials, project = google.auth.default()
    gcloud_client = container_v1.ClusterManagerClient(credentials=credentials)

    scan_clusters(gcloud_client, project)

    # FIXME add the k8s cert to a trust store
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    auth_gcloud_k8s(credentials)

    api_core_v1 = client.CoreV1Api()
    api_apps_v1 = client.AppsV1Api()
    api_storage_v1 = client.StorageV1Api()
    api_custom = client.CustomObjectsApi()
    api_extensions_v1_beta1 = client.ExtensionsV1beta1Api()
    api_ext_v1_beta1 = client.ApiextensionsV1beta1Api()
    api_rbac_auth_v1_b1 = client.RbacAuthorizationV1beta1Api()

    ensure_traefik(
        api_core_v1,
        api_ext_v1_beta1,
        api_apps_v1,
        api_custom,
        api_rbac_auth_v1_b1,
        admin_email,
        domain,
        static_ip,
        oauth_client_id,
        oauth_client_secret,
        oauth_domain,
        oauth_secret
    )
    volume_paths = [
        ('data', '/opt/nipyapi/data', '20Gi', 'standard'),
    ]

    with open(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'), 'rb') as f:
        gcloud_credentials_b64 = b64encode(f.read()).decode('UTF-8')

    ensure_secret(
        api=api_core_v1,
        name='webui-credentials',
        namespace='default',
        secret=V1Secret(
            metadata=client.V1ObjectMeta(
                name='webui-credentials'
            ),
            data={
                'gcloud-credentials': gcloud_credentials_b64
            }
        )
    )
    volume_mounts = [V1VolumeMount(name=path[0], mount_path=path[1]) for path in volume_paths]
    volume_mounts.append(
        V1VolumeMount(
            name='webui-credentials',
            mount_path='/root/webui',
            read_only=True
        )
    )
    ensure_single_container_statefulset(
        api_apps_v1=api_apps_v1,
        name='admin',
        replicas=1,
        container=V1Container(
            name='webui',
            image='aichrist/nipyapi-ds:latest',
            env=[
                # FIXME use k8s secrets for these values
                V1EnvVar(name='DOMAIN', value=domain),
                V1EnvVar(name='STATIC_IP', value=static_ip),
                V1EnvVar(name='ADMIN_EMAIL', value=admin_email),
                V1EnvVar(name='OAUTH_CLIENT_ID', value=oauth_client_id),
                V1EnvVar(name='OAUTH_CLIENT_SECRET', value=oauth_client_secret),
                V1EnvVar(name='OAUTH_SECRET', value=oauth_secret),
                V1EnvVar(name='OAUTH_DOMAIN', value=oauth_domain),
                V1EnvVar(name='DJANGO_SECRET_KEY', value=django_secret_key),
                V1EnvVar(name='GOOGLE_APPLICATION_CREDENTIALS', value='/root/webui/gcloud_credentials.json'),
                V1EnvVar(name='GOOGLE_CLOUD_PROJECT', value=os.getenv('GOOGLE_CLOUD_PROJECT')),
            ],
            ports=[V1ContainerPort(container_port=8000)],
            volume_mounts=volume_mounts
        ),
        volumes=[
            V1Volume(
                name='webui-credentials',
                projected=V1ProjectedVolumeSource(
                    sources=[
                        V1VolumeProjection(
                            secret=V1SecretProjection(
                                name='webui-credentials',
                                items=[
                                    V1KeyToPath(
                                        key='gcloud-credentials',
                                        path='gcloud_credentials.json'
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        ],
        volume_paths=volume_paths
    )
    ensure_ingress_routed_svc(
        api_core_v1=api_core_v1,
        api_custom=api_custom,
        domain=domain,
        name='admin',
        port_name='web',
        svc_port=80,
        target_port=8000
    )

    perform_nifi_ops(
        api_apps_v1,
        api_core_v1,
        api_custom,
        domain
    )

    perform_build_ops_bg()


def perform_nifi_ops(api_apps_v1, api_core_v1, api_custom, domain):
    for instance in NifiInstance.objects.filter(state='PENDING_CREATE'):
        instance.state = 'CREATING'
        instance.save()
        port_name = 'web'
        instance.state = 'CREATE_FAILED'
        try:
            volume_paths = [
                ('db-repo', '/opt/nifi/nifi-current/database_repository', '20Gi', 'standard'),
                ('flowfile-repo', '/opt/nifi/nifi-current/flowfile_repository', '20Gi', 'standard'),
                ('provenance-repo', '/opt/nifi/nifi-current/provenance_repository', '20Gi', 'standard'),
                ('content-repo', '/opt/nifi/nifi-current/content_repository', '20Gi', 'standard'),
            ]
            ensure_single_container_statefulset(
                api_apps_v1=api_apps_v1,
                name=instance.hostname,
                replicas=1,
                container=V1Container(
                    name='nifi',
                    image='apache/nifi:1.9.2',
                    env=[V1EnvVar(name='NIFI_WEB_HTTP_HOST', value='0.0.0.0')],
                    ports=[V1ContainerPort(container_port=8080)],
                    volume_mounts=[V1VolumeMount(
                        name=path[0],
                        mount_path=path[1]
                    ) for path in volume_paths]
                ),
                init_containers=[
                    V1Container(
                        name='init-permissions',
                        image='busybox',
                        command=['sh', '-c', 'chown -R 1000:1000 /opt/nifi/nifi-current'],
                        volume_mounts=[V1VolumeMount(
                            name=path[0],
                            mount_path=path[1]
                        ) for path in volume_paths]
                    )
                ],
                volume_paths=volume_paths
            )
            ensure_ingress_routed_svc(
                api_core_v1=api_core_v1,
                api_custom=api_custom,
                domain=domain,
                name=instance.hostname,
                port_name=port_name,
                svc_port=80,
                target_port=8080
            )
            instance.state = 'RUNNING'
        finally:
            instance.save()
    for instance in NifiInstance.objects.filter(state='PENDING_DESTROY'):
        instance.state = 'DESTROYING'
        instance.save()
        instance.state = 'DESTROY_FAILED'
        try:
            destroy_statefulset(
                api_apps_v1,
                api_core_v1,
                namespace='default',
                name=instance.hostname
            )
            destroy_ingress_routed_svc(
                api_core_v1=api_core_v1,
                api_custom=api_custom,
                name=instance.hostname
            )
            instance.state = 'DESTROYED'
        finally:
            instance.save()
