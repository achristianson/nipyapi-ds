#!/bin/bash

set -e

cd /opt/nipyapi/nipyapi/webui

python manage.py migrate
python manage.py process_tasks &
python manage.py runserver
