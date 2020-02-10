import logging
import os

import docker
from background_task import background
from nifi_web.models import ImageMirrorJob

logger = logging.getLogger(__name__)


@background(schedule=0, remove_existing_tasks=True)
def perform_mirror_ops_bg():
    perform_mirror_ops()


def perform_mirror_ops():
    logger.info('performing docker mirror ops')
    client = docker.from_env()

    for job in ImageMirrorJob.objects.filter(state='PENDING_MIRROR'):
        try:
            logger.info(f'starting build {job.id}')
            job.state = 'MIRRORING'
            job.save()
            job.state = 'MIRROR_FAILED'

            # pull img
            logger.info(f'mirroring image from {job.mirror.from_image} to {job.mirror.to_image}')
            if job.mirror.auth is not None:
                logger.info(f'logging in')
                client.login(username=job.mirror.auth.username,
                             password=job.mirror.auth.password)
            logger.info(f'pulling image {job.mirror.from_image}')
            if job.mirror.auth is not None:
                img = client.images.pull(job.mirror.from_image)
            else:
                img = client.images.pull(job.mirror.from_image)

            if isinstance(img, list):
                img = img[0]

            img.tag(job.mirror.to_image)
            job.docker_id = img.id

            # push img
            job.state = 'PUSHING'
            job.save()
            job.state = 'PUSH_FAILED'
            logger.info(f'pushing {job.mirror.to_image}')
            client.images.push(job.mirror.to_image)
            job.state = 'PUSHED'
        finally:
            job.save()
