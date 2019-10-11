import logging
import pickle

import google.auth
from background_task import background
from google.cloud import container_v1
from nifi.models import K8sCluster
from kubernetes import client
logger = logging.getLogger(__name__)


def scan_clusters(client, project_id):
    zone = '-'
    response = client.list_clusters(project_id, zone)
    clusters = response.clusters
    for c in clusters:
        obj, created = K8sCluster.objects.get_or_create(name=c.name)
        obj.status = c.status
        obj.location = c.location
        obj.node_count = c.current_node_count
        obj.object = pickle.dumps(c)
        obj.save()
        if created:
            logger.info('Created cluster %s', obj.name)
        else:
            logger.info('Updated cluster %s', obj.name)
        cluster_endpoint = c.endpoint
        print("*** CLUSTER ENDPOINT ***")
        print(cluster_endpoint)

        cluster_master_auth = c.master_auth
        print("*** CLUSTER MASTER USERNAME PWD ***")
        print(c.master_auth)
        cluster_username = cluster_master_auth.username
        cluster_password = cluster_master_auth.password
        print("USERNAME : %s - PASSWORD : %s" % (cluster_username, cluster_password))


@background(schedule=0)
def perform_cloud_ops():
    # set GOOGLE_APPLICATION_CREDENTIALS env to credentials file
    # set GOOGLE_CLOUD_PROJECT env to project id
    credentials, project = google.auth.default()
    gcloud_client = container_v1.ClusterManagerClient(credentials=credentials)

    scan_clusters(gcloud_client, project)

    c = K8sCluster.objects.get(id=1)
    gc = pickle.loads(c.object)
    configuration = client.Configuration()
    configuration.host = f"https://{gc.endpoint}:443"
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + credentials.token}
    client.Configuration.set_default(configuration)

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    pods = v1.list_pod_for_all_namespaces(watch=False)
    for i in pods.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    # cluster = client.get_cluster(project, 'us-east4', 'dfa-1')
