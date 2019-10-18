import logging

from django.shortcuts import render
from nifi_web import bg_tasks

logger = logging.getLogger(__name__)


def index(request):
    bg_tasks.perform_cloud_ops()
    logger.info('hello from index view')
    return render(request, 'frontend/index.html')
