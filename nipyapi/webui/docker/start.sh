#!/bin/bash

set -e

cd /opt/nipyapi/nipyapi/webui

python3 manage.py migrate
python3 manage.py process_tasks &
python3 manage.py runserver 0.0.0.0:8000
