from kubernetes import client
from kubernetes.client import V1beta1CustomResourceDefinition, V1ObjectMeta, V1beta1CustomResourceDefinitionSpec
import logging
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
