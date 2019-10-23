#!/bin/bash

set -e

nipy_dir="$(readlink -f "$(dirname "$0")/../../..")"

cd "${nipy_dir}"/nipyapi/webui/docker
mkdir -p build
cd build
mkdir -p ./nipyapi
rsync -avr \
      --exclude nipyapi/webui/docker \
      "${nipy_dir}"/ ./nipyapi/
docker build -t nipyapi-webui -f ../Dockerfile .
