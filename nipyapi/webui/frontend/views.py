import logging

from django.shortcuts import render
from nipyapi.webui.nifi import bg_tasks

logger = logging.getLogger(__name__)


def index(request):
    bg_tasks.perform_cloud_ops()
    logger.error('hello from index view')
    return render(request, 'frontend/index.html')
