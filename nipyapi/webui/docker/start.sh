#!/bin/bash

set -e

gcloud config set project ${GOOGLE_CLOUD_PROJECT}
echo "" | gcloud auth configure-docker

cd /opt/nipyapi/nipyapi/webui

python3 manage.py migrate
python3 manage.py process_tasks &
python3 manage.py runserver 0.0.0.0:8000
