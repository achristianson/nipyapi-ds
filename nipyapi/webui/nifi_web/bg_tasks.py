import logging
import os
import pickle

import google.auth
import urllib3
from background_task import background
from google.cloud import container_v1
from kubernetes import client
from kubernetes.client import V1ObjectMeta, V1ServiceSpec, \
    V1ServicePort, V1Service
from nifi_web.models import K8sCluster

from nifi_web.k8s.general import auth_gcloud_k8s, ensure_service
from nifi_web.k8s.traefik import ensure_traefik

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

    credentials, project = google.auth.default()
    gcloud_client = container_v1.ClusterManagerClient(credentials=credentials)

    scan_clusters(gcloud_client, project)

    # FIXME add the k8s cert to a trust store
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    auth_gcloud_k8s(credentials)

    api_core_v1 = client.CoreV1Api()
    api_apps_v1 = client.AppsV1Api()
    api_custom_api = client.CustomObjectsApi()
    api_extensions_v1_beta1 = client.ExtensionsV1beta1Api()
    api_ext_v1_beta1 = client.ApiextensionsV1beta1Api()
    api_rbac_auth_v1_b1 = client.RbacAuthorizationV1beta1Api()

    # print("Listing pods with their IPs:")
    # pods = v1.list_pod_for_all_namespaces(watch=False)
    # for i in pods.items:
    #     print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    # cluster = client.get_cluster(project, 'us-east4', 'dfa-1')

    ensure_traefik(
        api_core_v1,
        api_ext_v1_beta1,
        api_apps_v1,
        api_custom_api,
        api_rbac_auth_v1_b1,
        admin_email,
        domain,
        static_ip,
        oauth_client_id,
        oauth_client_secret,
        oauth_domain,
        oauth_secret
    )

    ensure_service(
        api=api_core_v1,
        service=V1Service(
            api_version="v1",
            metadata=V1ObjectMeta(
                name='nifi',
                labels={'app': 'nifi'}
            ),
            spec=V1ServiceSpec(
                type='ClusterIP',
                ports=[
                    V1ServicePort(
                        port=8080,
                        target_port=8080,
                        name='web'
                    )
                ],
                selector={'app': 'nifi'}
            )
        ),
        name='nifi',
        namespace='default'
    )
    # Creation of the Deployment in specified namespace
    # (Can replace "default" with a namespace you may have created)
    # extensions_v1_beta1.create_namespaced_ingress(
    #     namespace="default",
    #     body=(client.ExtensionsV1beta1Ingress(
    #         api_version="extensions/v1beta1",
    #         kind="Ingress",
    #         metadata=client.V1ObjectMeta(name="nifi", annotations={
    #             "nginx.ingress.kubernetes.io/rewrite-target": "/"
    #         }),
    #         spec=client.ExtensionsV1beta1IngressSpec(
    #             rules=[client.ExtensionsV1beta1IngressRule(
    #                 # host="somehost.com",
    #                 http=client.ExtensionsV1beta1HTTPIngressRuleValue(
    #                     paths=[client.ExtensionsV1beta1HTTPIngressPath(
    #                         path="/",
    #                         backend=client.ExtensionsV1beta1IngressBackend(
    #                             service_port=8080,
    #                             service_name="nifi")
    #
    #                     )]
    #                 )
    #             )
    #             ]
    #         )
    #     ))
    # )

    # api_response = apps_v1.create_namespaced_stateful_set(
    #     body=(create_nifi_ss_object()),
    #     namespace='default'
    # )
    # print("StatefulSet created. status='%s'" % str(api_response.status))
