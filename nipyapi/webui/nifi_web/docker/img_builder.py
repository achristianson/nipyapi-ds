import logging
import os

import docker
from background_task import background
from nifi_web.models import NifiImageBuild

logger = logging.getLogger(__name__)


@background(schedule=0, remove_existing_tasks=True)
def perform_build_ops_bg():
    perform_build_ops()


def perform_build_ops():
    logger.info('performing docker build ops')
    client = docker.from_env()
    for build in NifiImageBuild.objects.filter(state='PENDING_BUILD'):
        logger.info(f'starting build {build.id}')
        build.state = 'BUILDING'
        build.save()
        # build img
        docker_path = f'{os.path.dirname(os.path.realpath(__file__))}/images/nifi'
        logger.info(f'building docker in {docker_path} with tag {build.image.tag}')
        # push img
        im, _ = client.images.build(
            path=docker_path,
            tag=build.image.tag,
            buildargs={
                'GIT_REPO': build.image.git_repo,
                'GIT_BRANCH': build.image.branch
            }
        )
        logger.info(f'successfully built docker image in {docker_path} with tag {build.image.tag}')
        build.docker_id = im.id
        build.state = 'PUSHING'
        build.save()
        logger.info(f'pushing {build.image.tag}')
        client.images.push(build.image.tag)
        build.state = 'PUSHED'
        build.save()
