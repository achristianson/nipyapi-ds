import logging

from kubernetes import client
from kubernetes.client import V1beta1CustomResourceDefinition, V1ObjectMeta, V1beta1CustomResourceDefinitionSpec, \
    V1Deployment, V1DeploymentSpec, V1LabelSelector, V1PodTemplateSpec, V1PodSpec, V1Service, V1ServiceSpec, \
    V1ServicePort, V1DeleteOptions, V1PersistentVolumeClaim, V1PersistentVolumeClaimSpec, V1ResourceRequirements
from nifi_web.models import K8sCluster

logger = logging.getLogger(__name__)


def auth_gcloud_k8s(credentials):
    c = K8sCluster.objects.get(id=1)
    configuration = client.Configuration()
    configuration.host = f"https://{c.endpoint}:443"
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + credentials.token}
    client.Configuration.set_default(configuration)


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


def destroy_custom_object(api: client.CustomObjectsApi, group, plural, version, namespace, name):
    if len(api.list_namespaced_custom_object(namespace=namespace,
                                             field_selector=f'metadata.name={name}', group=group,
                                             plural=plural, version=version)['items']) == 1:
        logger.info(f'destroying custom object: {namespace}/{name}')
        api.delete_namespaced_custom_object(
            namespace=namespace,
            group=group,
            plural=plural,
            version=version,
            name=name,
            body=V1DeleteOptions()
        )
    else:
        logger.info(f'cannot find custom object to destroy: {namespace}/{name}')


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


def ensure_statefulset(api: client.AppsV1Api, stateful_set, namespace, name):
    if len(api.list_namespaced_stateful_set(namespace=namespace,
                                            field_selector=f'metadata.name={name}').items) == 0:
        logger.info(f'creating StatefulSet: {namespace}/{name}')
        api.create_namespaced_stateful_set(
            body=stateful_set,
            namespace=namespace
        )
    else:
        logger.info(f'StatefulSet exists: {namespace}/{name}')


def destroy_deployment(api: client.AppsV1Api, namespace, name):
    if len(api.list_namespaced_deployment(namespace=namespace,
                                          field_selector=f'metadata.name={name}').items) == 1:
        logger.info(f'destroying Deployment: {namespace}/{name}')
        api.delete_namespaced_deployment(
            name=name,
            namespace=namespace
        )
    else:
        logger.info(f'cannot find Deployment to destroy: {namespace}/{name}')


def destroy_statefulset(api: client.AppsV1Api, core_api: client.CoreV1Api, namespace, name):
    for pvc in core_api.list_namespaced_persistent_volume_claim(namespace=namespace,
                                                                label_selector=f'app={name}').items:
        core_api.delete_namespaced_persistent_volume_claim(
            name=pvc.metadata.name,
            namespace='default'
        )
    if len(api.list_namespaced_stateful_set(namespace=namespace,
                                            field_selector=f'metadata.name={name}').items) == 1:
        logger.info(f'destroying StatefulSet: {namespace}/{name}')
        api.delete_namespaced_stateful_set(
            name=name,
            namespace=namespace
        )
    else:
        logger.info(f'cannot find StatefulSet to destroy: {namespace}/{name}')


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


def destroy_service(api: client.CoreV1Api, namespace, name):
    if len(api.list_namespaced_service(namespace=namespace,
                                       field_selector=f'metadata.name={name}').items) == 1:
        logger.info(f'destroying Service: {namespace}/{name}')
        api.delete_namespaced_service(
            name=name,
            namespace=namespace
        )
    else:
        logger.info(f'cannot find Service to destroy: {namespace}/{name}')


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


def ensure_secret(api: client.CoreV1Api, secret, name, namespace):
    if len(api.list_namespaced_secret(namespace=namespace,
                                      field_selector=f'metadata.name={name}').items) == 0:
        logger.info(f'creating secret: {name}')
        api.create_namespaced_secret(
            namespace=namespace,
            body=secret
        )
    else:
        logger.info(f'secret exists: {name}')


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


def ensure_storage_class(api: client.StorageV1Api, cls, name):
    if len(api.list_storage_class(field_selector=f'metadata.name={name}').items) == 0:
        logger.info(f'creating StorageClass: {name}')
        api.create_storage_class(cls)
    else:
        logger.info(f'StorageClass exists: {name}')


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


def ensure_single_container_deployment(api_apps_v1, container, name, replicas=1):
    ensure_deployment(
        api=api_apps_v1,
        deployment=V1Deployment(
            api_version="apps/v1",
            metadata=V1ObjectMeta(
                name=name,
                labels={'app': name}
            ),
            spec=V1DeploymentSpec(
                replicas=replicas,
                selector=V1LabelSelector(
                    match_labels={'app': name}
                ),
                template=V1PodTemplateSpec(
                    metadata=V1ObjectMeta(
                        name=name,
                        labels={'app': name}
                    ),
                    spec=V1PodSpec(
                        containers=[
                            container
                        ]
                    )
                )
            )
        ),
        name=name,
        namespace='default'
    )


def ensure_ingress_routed_svc(api_core_v1, api_custom, domain, name, port_name, svc_port, target_port):
    ensure_service(
        api=api_core_v1,
        service=V1Service(
            api_version="v1",
            metadata=V1ObjectMeta(
                name=name
            ),
            spec=V1ServiceSpec(
                type='ClusterIP',
                ports=[
                    V1ServicePort(
                        protocol='TCP',
                        port=svc_port,
                        name=port_name,
                        target_port=target_port
                    ),
                ],
                selector={'app': name}
            )
        ),
        name=name,
        namespace='default'
    )
    ensure_custom_object(
        api=api_custom,
        custom_object={
            'apiVersion': 'traefik.containo.us/v1alpha1',
            'kind': 'IngressRoute',
            'metadata': {
                'name': name,
            },
            'spec': {
                'entryPoints': [
                    'websecure'
                ],
                'routes': [
                    {
                        'match': f'Host(`{name}.{domain}`)',
                        'kind': 'Rule',
                        'services': [
                            {
                                'name': name,
                                'port': svc_port
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
        name=name,
        namespace='default'
    )


def destroy_ingress_routed_svc(api_core_v1, api_custom, name):
    destroy_service(
        api=api_core_v1,
        name=name,
        namespace='default'
    )
    destroy_custom_object(
        api=api_custom,
        group='traefik.containo.us',
        plural='ingressroutes',
        version='v1alpha1',
        name=name,
        namespace='default'
    )


def ensure_statefulset_with_containers(api_apps_v1, name, containers, volume_paths, replicas=1, init_containers=None,
                                       volumes=None):
    if volumes is None:
        volumes = []
    if init_containers is None:
        init_containers = []
    volume_claim_templates = [V1PersistentVolumeClaim(
        metadata=V1ObjectMeta(
            name=path[0]
        ),
        spec=V1PersistentVolumeClaimSpec(
            access_modes=['ReadWriteOnce'],
            resources=V1ResourceRequirements(
                requests={
                    'storage': path[2]
                }
            ),
            storage_class_name=path[3]
        )
    ) for path in volume_paths]
    ss = client.V1StatefulSet(
        api_version="apps/v1",
        kind="StatefulSet",
        metadata=client.V1ObjectMeta(
            name=name,
            labels={'app': name}
        ),
        spec=client.V1StatefulSetSpec(
            replicas=replicas,
            service_name=name,
            template=V1PodTemplateSpec(
                metadata=V1ObjectMeta(labels={"app": name}),
                spec=V1PodSpec(
                    containers=containers,
                    volumes=volumes,
                    init_containers=init_containers
                )
            ),
            selector={'matchLabels': {'app': name}},
            volume_claim_templates=volume_claim_templates
        )
    )
    ensure_statefulset(
        api_apps_v1,
        stateful_set=ss,
        namespace='default',
        name=name
    )
