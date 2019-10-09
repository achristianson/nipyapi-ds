from background_task import background
from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)


@background(schedule=5)
def notify_user(user_id):
    logger.error('hello from background task')
    print("HELLO")


def index(request):
    logger.error('hello from index view')
    notify_user(10)
    return render(request, 'frontend/index.html')
