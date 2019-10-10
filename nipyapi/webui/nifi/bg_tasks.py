import logging

from background_task import background
from google.cloud import container_v1

from nifi.models import K8sCluster

logger = logging.getLogger(__name__)


@background(schedule=0)
def perform_cloud_ops():
    client = container_v1.ClusterManagerClient()

    project_id = 'gcp-dim'
    zone = '-'

    response = client.list_clusters(project_id, zone)

    for c in response.clusters:
        obj, created = K8sCluster.objects.get_or_create(
            name=c.name,
            defaults={
                'status': c.status,
                'location': c.location,
                'node_count': c.current_node_count,
            }
        )
        if created:
            logger.info('Created cluster %s', obj.name)
        else:
            logger.info('Updated cluster %s', obj.name)
