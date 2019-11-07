import logging
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webui.settings")

import django

django.setup()

from nifi_web.docker.img_builder import perform_build_ops

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    perform_build_ops()
