import logging
import os
import pickle
import uuid
from base64 import b64encode

import google.auth
import urllib3
from background_task import background
from google.cloud import container_v1
from kubernetes import client
from kubernetes.client import V1Container, V1EnvVar, V1ContainerPort, V1VolumeMount, V1StorageClass, V1ObjectMeta, \
    V1SecurityContext, V1Secret, V1Volume, V1ProjectedVolumeSource, V1VolumeProjection, V1SecretProjection, V1KeyToPath, \
    V1Service, V1ServiceSpec, V1ServicePort
from nifi_web.docker.img_builder import perform_build_ops_bg
from nifi_web.k8s.general import auth_gcloud_k8s, ensure_single_container_deployment, \
    ensure_ingress_routed_svc, destroy_ingress_routed_svc, destroy_deployment, ensure_statefulset_with_containers, \
    destroy_statefulset, ensure_storage_class, ensure_secret, ensure_namespace, destroy_namespace, ensure_service, \
    destroy_service
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
    webui_volume_paths = [
        ('data', '/opt/nipyapi/data', '20Gi', 'standard'),
    ]
    webui_volume_mounts = [V1VolumeMount(name=path[0], mount_path=path[1]) for path in webui_volume_paths]
    webui_volume_mounts.append(
        V1VolumeMount(
            name='webui-credentials',
            mount_path='/root/webui',
            read_only=True
        )
    )

    dind_volume_paths = [
        ('docker', '/var/lib/docker', '200Gi', 'standard'),
    ]
    dind_volume_mounts = [V1VolumeMount(name=path[0], mount_path=path[1]) for path in dind_volume_paths]
    shared_volume_mounts = [
        V1VolumeMount(
            name='dind-socket',
            mount_path='/var/run-shared'
        )
    ]
    ensure_statefulset_with_containers(
        api_apps_v1=api_apps_v1,
        name='admin',
        namespace='default',
        replicas=1,
        containers=[
            V1Container(
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
                    V1EnvVar(name='CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE',
                             value='/root/webui/gcloud_credentials.json'),
                    V1EnvVar(name='GOOGLE_CLOUD_PROJECT', value=os.getenv('GOOGLE_CLOUD_PROJECT')),
                    V1EnvVar(name='DOCKER_HOST', value='unix:///var/run-shared/docker.sock'),
                ],
                ports=[V1ContainerPort(container_port=8000)],
                volume_mounts=webui_volume_mounts + shared_volume_mounts
            ),
            V1Container(
                name='dind',
                image='docker:19-dind',
                security_context=V1SecurityContext(
                    privileged=True
                ),
                command=['dockerd', '-H', 'unix:///var/run-shared/docker.sock'],
                volume_mounts=dind_volume_mounts + shared_volume_mounts
            )
        ],
        volumes=[
            V1Volume(
                name='dind-socket',
                empty_dir={}
            ),
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
        volume_paths=webui_volume_paths + dind_volume_paths
    )
    ensure_ingress_routed_svc(
        api_core_v1=api_core_v1,
        api_custom=api_custom,
        domain=domain,
        hostname='admin',
        name='admin',
        target_name='admin',
        namespace='default',
        port_name='web',
        svc_port=80,
        target_port=8000
    )
    reg_volume_paths = [
        ('database', '/opt/nifi-registry/nifi-registry-current/database', '10Gi', 'standard'),
        ('flow-storage', '/opt/nifi-registry/nifi-registry-current/flow_storage', '20Gi', 'standard'),
    ]
    reg_volume_mounts = [V1VolumeMount(name=path[0], mount_path=path[1]) for path in reg_volume_paths]
    ensure_statefulset_with_containers(
        api_apps_v1=api_apps_v1,
        name='registry',
        namespace='default',
        replicas=1,
        containers=[
            V1Container(
                name='registry',
                image='apache/nifi-registry:latest',
                env=[
                    V1EnvVar(name='NIFI_REGISTRY_WEB_HTTP_PORT', value='19090'),
                ],
                ports=[V1ContainerPort(container_port=19090)],
                volume_mounts=reg_volume_mounts
            ),
        ],
        init_containers=[
            V1Container(
                name='init-permissions',
                image='busybox',
                command=['sh', '-c', 'chown -R 1000:1000 /opt/nifi-registry/nifi-registry-current'],
                volume_mounts=[V1VolumeMount(
                    name=path[0],
                    mount_path=path[1]
                ) for path in reg_volume_paths]
            )
        ],
        volumes=[],
        volume_paths=reg_volume_paths
    )
    ensure_ingress_routed_svc(
        api_core_v1=api_core_v1,
        api_custom=api_custom,
        domain=domain,
        hostname='registry',
        name='registry',
        target_name='registry',
        namespace='default',
        port_name='web',
        svc_port=80,
        target_port=19090
    )

    perform_nifi_ops(
        api_apps_v1,
        api_core_v1,
        api_custom,
        domain
    )

    perform_build_ops_bg()


def perform_nifi_ops(api_apps_v1, api_core_v1, api_custom, domain):
    create_nifi_instances(api_apps_v1, api_core_v1, api_custom, domain)
    destroy_nifi_instances(api_apps_v1, api_core_v1, api_custom)


def destroy_nifi_instances(api_apps_v1, api_core_v1, api_custom):
    for instance in NifiInstance.objects.filter(state='PENDING_DESTROY'):
        instance.state = 'DESTROYING'
        instance.save()
        instance.state = 'DESTROY_FAILED'
        try:
            destroy_statefulset(
                api_apps_v1,
                api_core_v1,
                namespace=instance.namespace,
                name=instance.hostname
            )
            destroy_ingress_routed_svc(
                api_core_v1=api_core_v1,
                api_custom=api_custom,
                name=instance.hostname,
                namespace=instance.namespace
            )
            destroy_statefulset(
                api_apps_v1,
                api_core_v1,
                namespace=instance.namespace,
                name='mongo'
            )
            destroy_service(
                api_core_v1,
                namespace=instance.namespace,
                name='mongo'
            )
            destroy_deployment(
                api_apps_v1,
                namespace=instance.namespace,
                name='mongo-express'
            )
            destroy_ingress_routed_svc(
                api_core_v1=api_core_v1,
                api_custom=api_custom,
                name='mongo-' + instance.hostname,
                namespace=instance.namespace
            )
            destroy_deployment(
                api_apps_v1,
                namespace=instance.namespace,
                name='zookeeper'
            )
            destroy_service(
                api_core_v1,
                namespace=instance.namespace,
                name='zookeeper'
            )
            destroy_deployment(
                api_apps_v1,
                namespace=instance.namespace,
                name='kafka'
            )
            destroy_service(
                api_core_v1,
                namespace=instance.namespace,
                name='kafka'
            )
            destroy_deployment(
                api_apps_v1,
                namespace=instance.namespace,
                name='prometheus'
            )
            destroy_ingress_routed_svc(
                api_core_v1=api_core_v1,
                api_custom=api_custom,
                name='prometheus-' + instance.hostname,
                namespace=instance.namespace
            )
            destroy_deployment(
                api_apps_v1,
                namespace=instance.namespace,
                name='jupyter'
            )
            destroy_ingress_routed_svc(
                api_core_v1=api_core_v1,
                api_custom=api_custom,
                name='jupyter-' + instance.hostname,
                namespace=instance.namespace
            )
            if instance.namespace != "default":
                destroy_namespace(api_core_v1, instance.namespace)
            instance.state = 'DESTROYED'
        finally:
            instance.save()


def create_nifi_instances(api_apps_v1, api_core_v1, api_custom, domain):
    for instance in NifiInstance.objects.filter(state='PENDING_CREATE'):
        instance.state = 'CREATING'
        instance.save()
        port_name = 'web'
        instance.state = 'CREATE_FAILED'
        try:
            namespace = 'default'

            if instance.namespace is not None and instance.namespace != 'default':
                namespace = instance.namespace
                ensure_namespace(api_core_v1, namespace)
            else:
                instance.namespace = 'default'

            # deploy nifi
            nifi_volume_paths = [
                ('db-repo', '/opt/nifi/nifi-current/database_repository', '20Gi', 'standard'),
                ('flowfile-repo', '/opt/nifi/nifi-current/flowfile_repository', '20Gi', 'standard'),
                ('provenance-repo', '/opt/nifi/nifi-current/provenance_repository', '20Gi', 'standard'),
                ('content-repo', '/opt/nifi/nifi-current/content_repository', '20Gi', 'standard'),
            ]
            ensure_statefulset_with_containers(
                api_apps_v1=api_apps_v1,
                name=instance.hostname,
                namespace=namespace,
                replicas=1,
                containers=[V1Container(
                    name='nifi',
                    image=instance.image,
                    env=[V1EnvVar(name='NIFI_WEB_HTTP_HOST', value='0.0.0.0')],
                    ports=[V1ContainerPort(container_port=8080)],
                    volume_mounts=[V1VolumeMount(
                        name=path[0],
                        mount_path=path[1]
                    ) for path in nifi_volume_paths]
                )],
                init_containers=[
                    V1Container(
                        name='init-permissions',
                        image='busybox',
                        command=['sh', '-c', 'chown -R 1000:1000 /opt/nifi/nifi-current'],
                        volume_mounts=[V1VolumeMount(
                            name=path[0],
                            mount_path=path[1]
                        ) for path in nifi_volume_paths]
                    )
                ],
                volume_paths=nifi_volume_paths
            )
            ensure_ingress_routed_svc(
                api_core_v1=api_core_v1,
                api_custom=api_custom,
                domain=domain,
                hostname=instance.hostname,
                name=instance.hostname,
                target_name=instance.hostname,
                namespace=namespace,
                port_name=port_name,
                svc_port=80,
                target_port=8080
            )

            # deploy mongo
            if instance.deploy_mongo:
                mongo_volume_paths = [
                    ('db', '/data/db', '20Gi', 'standard'),
                ]
                ensure_statefulset_with_containers(
                    api_apps_v1=api_apps_v1,
                    name='mongo',
                    namespace=namespace,
                    replicas=1,
                    containers=[V1Container(
                        name='mongo',
                        image='mongo',
                        env=[
                            V1EnvVar(name='MONGO_INITDB_ROOT_USERNAME', value='admin'),
                            V1EnvVar(name='MONGO_INITDB_ROOT_PASSWORD', value='admin')
                        ],
                        ports=[V1ContainerPort(name='mongo', container_port=27017)],
                        volume_mounts=[V1VolumeMount(
                            name=path[0],
                            mount_path=path[1]
                        ) for path in mongo_volume_paths]
                    )],
                    volume_paths=mongo_volume_paths
                )
                ensure_service(
                    api=api_core_v1,
                    service=V1Service(
                        api_version="v1",
                        metadata=V1ObjectMeta(
                            name='mongo'
                        ),
                        spec=V1ServiceSpec(
                            type='ClusterIP',
                            ports=[
                                V1ServicePort(
                                    protocol='TCP',
                                    port=27017,
                                    name='mongo',
                                    target_port=27017
                                ),
                            ],
                            selector={
                                'app': 'mongo'
                            }
                        )
                    ),
                    name='mongo',
                    namespace=namespace
                )
                ensure_single_container_deployment(
                    api_apps_v1,
                    V1Container(
                        name='mongo-express',
                        image='mongo-express',
                        env=[
                            V1EnvVar(name='ME_CONFIG_MONGODB_ADMINUSERNAME', value='admin'),
                            V1EnvVar(name='ME_CONFIG_MONGODB_ADMINPASSWORD', value='admin')
                        ],
                        ports=[V1ContainerPort(container_port=8000)]),
                    'mongo-express',
                    instance.namespace
                )
                ensure_ingress_routed_svc(
                    api_core_v1=api_core_v1,
                    api_custom=api_custom,
                    domain=domain,
                    hostname="mongo-" + instance.hostname,
                    name="mongo-" + instance.hostname,
                    target_name="mongo-express",
                    namespace=namespace,
                    port_name=port_name,
                    svc_port=80,
                    target_port=8081
                )

            if instance.deploy_kafka:
                # deploy zookeeper
                ensure_single_container_deployment(
                    api_apps_v1,
                    V1Container(
                        name='zookeeper',
                        image='wurstmeister/zookeeper',
                        env=[],
                        ports=[V1ContainerPort(container_port=2181)]),
                    'zookeeper',
                    instance.namespace
                )
                ensure_service(
                    api=api_core_v1,
                    service=V1Service(
                        api_version="v1",
                        metadata=V1ObjectMeta(
                            name='zookeeper'
                        ),
                        spec=V1ServiceSpec(
                            type='ClusterIP',
                            ports=[
                                V1ServicePort(
                                    protocol='TCP',
                                    port=2181,
                                    name='zookeeper',
                                    target_port=2181
                                ),
                            ],
                            selector={
                                'app': 'zookeeper'
                            }
                        )
                    ),
                    name='zookeeper',
                    namespace=namespace
                )

                # deploy kafka
                ensure_single_container_deployment(
                    api_apps_v1,
                    V1Container(
                        name='kafka',
                        image='wurstmeister/kafka',
                        env=[
                            V1EnvVar(name='KAFKA_ADVERTISED_HOST_NAME', value='kafka'),
                            V1EnvVar(name='KAFKA_ZOOKEEPER_CONNECT', value='zookeeper:2181'),
                            V1EnvVar(name='KAFKA_PORT', value='9092')
                        ],
                        ports=[V1ContainerPort(container_port=9092)]),
                    'kafka',
                    instance.namespace
                )
                ensure_service(
                    api=api_core_v1,
                    service=V1Service(
                        api_version="v1",
                        metadata=V1ObjectMeta(
                            name='kafka'
                        ),
                        spec=V1ServiceSpec(
                            type='ClusterIP',
                            ports=[
                                V1ServicePort(
                                    protocol='TCP',
                                    port=9092,
                                    name='kafka',
                                    target_port=9092
                                ),
                            ],
                            selector={
                                'app': 'kafka'
                            }
                        )
                    ),
                    name='kafka',
                    namespace=namespace
                )

            if instance.deploy_prometheus:
                # deploy prometheus
                ensure_single_container_deployment(
                    api_apps_v1,
                    V1Container(
                        name='prometheus',
                        image='prom/prometheus',
                        env=[],
                        ports=[V1ContainerPort(container_port=9090)]),
                    'prometheus',
                    instance.namespace
                )
                ensure_ingress_routed_svc(
                    api_core_v1=api_core_v1,
                    api_custom=api_custom,
                    domain=domain,
                    hostname="prometheus-" + instance.hostname,
                    name="prometheus",
                    target_name="prometheus",
                    namespace=namespace,
                    port_name=port_name,
                    svc_port=9090,
                    target_port=9090
                )

            if instance.deploy_jupyter:
                # deploy jupyter
                instance.jupyter_token = str(uuid.uuid1())
                ensure_single_container_deployment(
                    api_apps_v1,
                    V1Container(
                        name='jupyter',
                        image='jupyter/datascience-notebook',
                        command=['start-notebook.sh', '--NotebookApp.token=' + instance.jupyter_token],
                        env=[],
                        ports=[V1ContainerPort(container_port=8888)]),
                    'jupyter',
                    instance.namespace
                )
                ensure_ingress_routed_svc(
                    api_core_v1=api_core_v1,
                    api_custom=api_custom,
                    domain=domain,
                    hostname="jupyter-" + instance.hostname,
                    name="jupyter",
                    target_name="jupyter",
                    namespace=namespace,
                    port_name=port_name,
                    svc_port=8888,
                    target_port=8888
                )

            instance.state = 'RUNNING'
        finally:
            instance.save()
