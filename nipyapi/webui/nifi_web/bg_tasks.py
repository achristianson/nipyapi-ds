import logging
import os
import pickle

import google.auth
import urllib3
from background_task import background
from google.cloud import container_v1
from kubernetes import client
from kubernetes.client import V1ObjectMeta, V1beta1CustomResourceDefinition, V1beta1CustomResourceDefinitionSpec, \
    V1ClusterRole, V1PolicyRule, V1ClusterRoleBinding, V1Subject, V1RoleRef, V1ServiceSpec, \
    V1ServicePort, V1Service, V1Deployment, V1ServiceAccount, V1DeploymentSpec, V1LabelSelector, V1PodTemplateSpec, \
    V1PodSpec, V1Container, V1ContainerPort, V1EnvVar
from nifi_web.models import K8sCluster

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

    c = K8sCluster.objects.get(id=1)
    configuration = client.Configuration()
    configuration.host = f"https://{c.endpoint}:443"
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + credentials.token}
    client.Configuration.set_default(configuration)

    v1 = client.CoreV1Api()
    # v1.connect_get_namespaced_pod_portforward()
    apps_v1 = client.AppsV1Api()
    custom_api = client.CustomObjectsApi()
    extensions_v1_beta1 = client.ExtensionsV1beta1Api()
    api_ext_v1_beta1 = client.ApiextensionsV1beta1Api()
    rbac_auth_v1_b1 = client.RbacAuthorizationV1beta1Api()

    print("Listing pods with their IPs:")
    pods = v1.list_pod_for_all_namespaces(watch=False)
    for i in pods.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    # cluster = client.get_cluster(project, 'us-east4', 'dfa-1')

    # deploy traefik
    ensure_crd(
        api=api_ext_v1_beta1,
        name='ingressroutes.traefik.containo.us',
        group='traefik.containo.us',
        kind='IngressRoute',
        plural='ingressroutes',
        singular='ingressroute',
        scope='Namespaced'
    )
    ensure_crd(
        api=api_ext_v1_beta1,
        name='ingressroutetcps.traefik.containo.us',
        group='traefik.containo.us',
        kind='IngressRouteTCP',
        plural='ingressroutetcps',
        singular='ingressroutetcp',
        scope='Namespaced'
    )
    ensure_crd(
        api=api_ext_v1_beta1,
        name='middlewares.traefik.containo.us',
        group='traefik.containo.us',
        kind='Middleware',
        plural='middlewares',
        singular='middleware',
        scope='Namespaced'
    )
    ensure_crd(
        api=api_ext_v1_beta1,
        name='tlsoptions.traefik.containo.us',
        group='traefik.containo.us',
        kind='TLSOption',
        plural='tlsoptions',
        singular='tlsoption',
        scope='Namespaced'
    )
    ensure_role(
        api=rbac_auth_v1_b1,
        role=V1ClusterRole(
            api_version='rbac.authorization.k8s.io/v1beta1',
            kind='ClusterRole',
            metadata=V1ObjectMeta(name='traefik-ingress-controller'),
            rules=[
                V1PolicyRule(
                    api_groups=[''],
                    resources=['services', 'endpoints', 'secrets'],
                    verbs=['get', 'list', 'watch']
                ),
                V1PolicyRule(
                    api_groups=['extensions'],
                    resources=['ingresses'],
                    verbs=['get', 'list', 'watch']
                ),
                V1PolicyRule(
                    api_groups=['extensions'],
                    resources=['ingresses/status'],
                    verbs=['update']
                ),
                V1PolicyRule(
                    api_groups=['traefik.containo.us'],
                    resources=['middlewares'],
                    verbs=['get', 'list', 'watch']
                ),
                V1PolicyRule(
                    api_groups=['traefik.containo.us'],
                    resources=['ingressroutes'],
                    verbs=['get', 'list', 'watch']
                ),
                V1PolicyRule(
                    api_groups=['traefik.containo.us'],
                    resources=['ingressroutetcps'],
                    verbs=['get', 'list', 'watch']
                ),
                V1PolicyRule(
                    api_groups=['traefik.containo.us'],
                    resources=['tlsoptions'],
                    verbs=['get', 'list', 'watch']
                )
            ]
        ),
        name='traefik-ingress-controller'
    )
    ensure_role_binding(
        api=rbac_auth_v1_b1,
        role_binding=V1ClusterRoleBinding(
            api_version='rbac.authorization.k8s.io/v1beta1',
            kind='ClusterRoleBinding',
            metadata=V1ObjectMeta(name='traefik-ingress-controller'),
            role_ref=V1RoleRef(
                api_group='rbac.authorization.k8s.io',
                kind='ClusterRole',
                name='traefik-ingress-controller'
            ),
            subjects=[
                V1Subject(
                    kind='ServiceAccount',
                    name='traefik-ingress-controller',
                    namespace='default'
                )
            ]
        ),
        name='traefik-ingress-controller'
    )
    ensure_service(
        api=v1,
        service=V1Service(
            api_version="v1",
            metadata=V1ObjectMeta(
                name='traefik'
            ),
            spec=V1ServiceSpec(
                type='LoadBalancer',
                load_balancer_ip=static_ip,
                ports=[
                    # V1ServicePort(
                    #     protocol='TCP',
                    #     port=80,
                    #     name='web'
                    # ),
                    V1ServicePort(
                        protocol='TCP',
                        port=443,
                        name='websecure'
                    ),
                ],
                selector={'app': 'traefik'}
            )
        ),
        name='traefik',
        namespace='default'
    )
    ensure_service(
        api=v1,
        service=V1Service(
            api_version="v1",
            metadata=V1ObjectMeta(
                name='whoami'
            ),
            spec=V1ServiceSpec(
                type='ClusterIP',
                ports=[
                    V1ServicePort(
                        protocol='TCP',
                        port=80,
                        name='web'
                    ),
                ],
                selector={'app': 'whoami'}
            )
        ),
        name='whoami',
        namespace='default'
    )
    ensure_service_account(
        api=v1,
        account=V1ServiceAccount(
            api_version="v1",
            metadata=V1ObjectMeta(
                name='traefik-ingress-controller'
            ),
        ),
        name='traefik-ingress-controller',
        namespace='default'
    )
    ensure_deployment(
        api=apps_v1,
        deployment=V1Deployment(
            api_version="apps/v1",
            metadata=V1ObjectMeta(
                name='traefik',
                labels={'app': 'traefik'}
            ),
            spec=V1DeploymentSpec(
                replicas=1,
                selector=V1LabelSelector(
                    match_labels={'app': 'traefik'}
                ),
                template=V1PodTemplateSpec(
                    metadata=V1ObjectMeta(
                        name='traefik',
                        labels={'app': 'traefik'}
                    ),
                    spec=V1PodSpec(
                        service_account_name='traefik-ingress-controller',
                        containers=[
                            V1Container(
                                name='traefik',
                                image='traefik:v2.0',
                                args=[
                                    '--api.insecure',
                                    '--accesslog',
                                    '--entrypoints.web.Address=:80',
                                    '--entrypoints.websecure.Address=:443',
                                    '--providers.kubernetescrd',
                                    '--certificatesresolvers.default.acme.tlschallenge',
                                    f'--certificatesresolvers.default.acme.email={admin_email}',
                                    '--certificatesresolvers.default.acme.storage=acme.json',
                                    # '--certificatesresolvers.default.acme.caserver=https://acme-staging-v02.api.letsencrypt.org/directory',
                                ],
                                ports=[
                                    V1ContainerPort(
                                        name='web',
                                        container_port=8000
                                    ),
                                    V1ContainerPort(
                                        name='websecure',
                                        container_port=4443
                                    ),
                                    V1ContainerPort(
                                        name='admin',
                                        container_port=8080
                                    ),
                                ]
                            )
                        ]
                    )
                )
            )
        ),
        name='traefik',
        namespace='default'
    )
    ensure_deployment(
        api=apps_v1,
        deployment=V1Deployment(
            api_version="apps/v1",
            metadata=V1ObjectMeta(
                name='traefik-forward-auth',
                labels={'app': 'traefik-forward-auth'}
            ),
            spec=V1DeploymentSpec(
                replicas=1,
                selector=V1LabelSelector(
                    match_labels={'app': 'traefik-forward-auth'}
                ),
                template=V1PodTemplateSpec(
                    metadata=V1ObjectMeta(
                        name='traefik-forward-auth',
                        labels={'app': 'traefik-forward-auth'}
                    ),
                    spec=V1PodSpec(
                        containers=[
                            V1Container(
                                name='traefik-forward-auth',
                                image='thomseddon/traefik-forward-auth:2',
                                ports=[
                                    V1ContainerPort(
                                        name='auth',
                                        container_port=4181
                                    ),
                                ],
                                env=[
                                    V1EnvVar(name='PROVIDERS_GOOGLE_CLIENT_ID', value=oauth_client_id),
                                    # V1EnvVar(name='LOG_LEVEL', value='trace'),
                                    V1EnvVar(name='PROVIDERS_GOOGLE_CLIENT_SECRET', value=oauth_client_secret),
                                    V1EnvVar(name='SECRET', value=oauth_secret),
                                    V1EnvVar(name='DOMAIN', value=oauth_domain),
                                    V1EnvVar(name='COOKIE_DOMAIN', value=domain),
                                    V1EnvVar(name='AUTH_HOST', value=f'auth.{domain}'),
                                ]
                            )
                        ]
                    )
                )
            )
        ),
        name='traefik-forward-auth',
        namespace='default'
    )
    ensure_custom_object(
        api=custom_api,
        custom_object={
            'apiVersion': 'traefik.containo.us/v1alpha1',
            'kind': 'IngressRoute',
            'metadata': {
                'name': 'traefik-forward-auth',
            },
            'spec': {
                'entryPoints': [
                    'websecure'
                ],
                'routes': [
                    {
                        'match': f'Host(`auth.{domain}`)',
                        'kind': 'Rule',
                        'services': [
                            {
                                'name': 'traefik-forward-auth',
                                'port': 4181
                            }
                        ],
                        'middlewares': [
                            {'name': 'traefik-forward-auth'}
                        ]
                    }
                ],
                'tls': {
                    'certResolver': 'default'
                }
            }
        },
        group='traefik.containo.us',
        plural='ingressroutes',
        version='v1alpha1',
        name='traefik-forward-auth',
        namespace='default'
    )
    ensure_custom_object(
        api=custom_api,
        custom_object={
            'apiVersion': 'traefik.containo.us/v1alpha1',
            'kind': 'Middleware',
            'metadata': {
                'name': 'traefik-forward-auth',
            },
            'spec': {
                'forwardAuth': {
                    'address': 'http://traefik-forward-auth:4181',
                    'authResponseHeaders': [
                        'X-Forwarded-User'
                    ],
                }
            }
        },
        group='traefik.containo.us',
        plural='middlewares',
        version='v1alpha1',
        name='traefik-forward-auth',
        namespace='default'
    )
    ensure_service(
        api=v1,
        service=V1Service(
            api_version="v1",
            metadata=V1ObjectMeta(
                name='traefik-forward-auth'
            ),
            spec=V1ServiceSpec(
                type='ClusterIP',
                ports=[
                    V1ServicePort(
                        protocol='TCP',
                        port=4181,
                        name='auth'
                    ),
                ],
                selector={'app': 'traefik-forward-auth'}
            )
        ),
        name='traefik-forward-auth',
        namespace='default'
    )
    ensure_deployment(
        api=apps_v1,
        deployment=V1Deployment(
            api_version="apps/v1",
            metadata=V1ObjectMeta(
                name='whoami',
                labels={'app': 'whoami'}
            ),
            spec=V1DeploymentSpec(
                replicas=2,
                selector=V1LabelSelector(
                    match_labels={'app': 'whoami'}
                ),
                template=V1PodTemplateSpec(
                    metadata=V1ObjectMeta(
                        name='whoami',
                        labels={'app': 'whoami'}
                    ),
                    spec=V1PodSpec(
                        containers=[
                            V1Container(
                                name='whoami',
                                image='containous/whoami',
                                ports=[
                                    V1ContainerPort(
                                        name='web',
                                        container_port=8000
                                    ),
                                ]
                            )
                        ]
                    )
                )
            )
        ),
        name='whoami',
        namespace='default'
    )
    ensure_custom_object(
        api=custom_api,
        custom_object={
            'apiVersion': 'traefik.containo.us/v1alpha1',
            'kind': 'IngressRoute',
            'metadata': {
                'name': 'whoami',
            },
            'spec': {
                'entryPoints': [
                    'websecure'
                ],
                'routes': [
                    {
                        'match': f'Host(`whoami.{domain}`)',
                        'kind': 'Rule',
                        'services': [
                            {
                                'name': 'whoami',
                                'port': 80
                            }
                        ],
                        'middlewares': [
                            {'name': 'traefik-forward-auth'}
                        ]
                    }
                ],
                'tls': {
                    'certResolver': 'default'
                }
            }
        },
        group='traefik.containo.us',
        plural='ingressroutes',
        version='v1alpha1',
        name='whoami',
        namespace='default'
    )

    ensure_service(
        api=v1,
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


def ensure_custom_object(api: client.CustomObjectsApi, custom_object, group, plural, version, namespace, name):
    if len(api.list_namespaced_custom_object(namespace=namespace,
                                             field_selector=f'metadata.name={name}', group=group,
                                             plural=plural, version=version)['items']) == 0:
        logger.info(f'creating custom object: {namespace}/{name}')
        api.create_namespaced_custom_object(
            body=custom_object,
            namespace=namespace,
            group=group,
            plural=plural,
            version=version
        )
    else:
        logger.info(f'custom object exists: {namespace}/{name}')


def ensure_deployment(api: client.AppsV1Api, deployment, namespace, name):
    if len(api.list_namespaced_deployment(namespace=namespace,
                                          field_selector=f'metadata.name={name}').items) == 0:
        logger.info(f'creating Deployment: {namespace}/{name}')
        api.create_namespaced_deployment(
            body=deployment,
            namespace=namespace
        )
    else:
        logger.info(f'Deployment exists: {namespace}/{name}')


def ensure_service(api: client.CoreV1Api, service, namespace, name):
    if len(api.list_namespaced_service(namespace=namespace,
                                       field_selector=f'metadata.name={name}').items) == 0:
        logger.info(f'creating Service: {namespace}/{name}')
        api.create_namespaced_service(
            body=service,
            namespace=namespace
        )
    else:
        logger.info(f'Service exists: {namespace}/{name}')


def ensure_service_account(api: client.CoreV1Api, account, name, namespace):
    if len(api.list_namespaced_service_account(namespace=namespace,
                                               field_selector=f'metadata.name={name}').items) == 0:
        logger.info(f'creating ServiceAccount: {name}')
        api.create_namespaced_service_account(
            namespace=namespace,
            body=account
        )
    else:
        logger.info(f'ServiceAccount exists: {name}')


def ensure_role(api: client.RbacAuthorizationV1beta1Api, role, name):
    if len(api.list_cluster_role(field_selector=f'metadata.name={name}').items) == 0:
        logger.info(f'creating ClusterRole: {name}')
        api.create_cluster_role(role)
    else:
        logger.info(f'ClusterRole exists: {name}')


def ensure_role_binding(api: client.RbacAuthorizationV1beta1Api, role_binding, name):
    if len(api.list_cluster_role_binding(field_selector=f'metadata.name={name}').items) == 0:
        logger.info(f'creating ClusterRoleBinding: {name}')
        api.create_cluster_role_binding(role_binding)
    else:
        logger.info(f'ClusterRoleBinding exists: {name}')


def ensure_crd(api, name, group, kind, plural, singular, scope):
    if len(api.list_custom_resource_definition(field_selector=f'metadata.name={name}').items) == 0:
        logger.info(f'creating CustomResourceDefinition: {name}')
        try:
            api.create_custom_resource_definition(V1beta1CustomResourceDefinition(
                api_version='apiextensions.k8s.io/v1beta1',
                kind='CustomResourceDefinition',
                metadata=V1ObjectMeta(name=name),
                spec=V1beta1CustomResourceDefinitionSpec(
                    group=group,
                    version='v1alpha1',
                    names={
                        'kind': kind,
                        'plural': plural,
                        'singular': singular
                    },
                    scope=scope
                ),
            ))
        except ValueError:
            # unforunate workaround due to client library bug
            # https://github.com/kubernetes-client/python/issues/415
            logger.warning(f'swallowed ValueError when creating CRD {name} to workaround API client issue')
            pass
    else:
        logger.info(f'CustomResourceDefinition exists: {name}')
