from kubernetes.client import V1ClusterRole, V1ObjectMeta, V1PolicyRule, V1ClusterRoleBinding, V1RoleRef, V1Subject, \
    V1Service, V1ServiceSpec, V1ServicePort, V1ServiceAccount, V1Deployment, V1DeploymentSpec, V1LabelSelector, \
    V1PodTemplateSpec, V1PodSpec, V1Container, V1ContainerPort, V1EnvVar

from nifi_web.k8s.general import ensure_crd, ensure_role, ensure_role_binding, ensure_service, ensure_service_account, \
    ensure_deployment, ensure_custom_object, ensure_single_container_deployment, ensure_ingress_routed_svc


def ensure_traefik(api_core_v1, api_ext_v1_beta1, api_apps_v1, api_custom, api_rbac_auth_v1_b1, admin_email, domain,
                   static_ip, oauth_client_id, oauth_client_secret, oauth_domain, oauth_secret):
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
        api=api_rbac_auth_v1_b1,
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
        api=api_rbac_auth_v1_b1,
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
        api=api_core_v1,
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
    ensure_service_account(
        api=api_core_v1,
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
        api=api_apps_v1,
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
        api=api_apps_v1,
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
        api=api_custom,
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
        api=api_custom,
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
        api=api_core_v1,
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
    ensure_whoami(api_apps_v1, api_core_v1, api_custom, domain)


def ensure_whoami(api_apps_v1, api_core_v1, api_custom, domain):
    name = 'whoami'
    port_name = 'web'
    ensure_single_container_deployment(
        api_apps_v1,
        V1Container(
            name=name,
            image='containous/whoami',
            ports=[V1ContainerPort(name=port_name,
                                   container_port=8000)]),
        name,
        'default'
    )
    ensure_ingress_routed_svc(
        api_core_v1,
        api_custom,
        domain,
        name,
        name,
        name,
        'default',
        port_name,
        80,
        8000)
