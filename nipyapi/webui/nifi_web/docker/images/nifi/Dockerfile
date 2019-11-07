# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

#FROM maven:3-jdk-8 AS build
FROM maven:3-jdk-8 AS build
ARG GIT_REPO
ARG GIT_BRANCH
RUN mkdir -p /usr/local/src && \
    cd /usr/local/src && \
    git clone ${GIT_REPO}
WORKDIR /usr/local/src/nifi
RUN git fetch --all
RUN git checkout ${GIT_BRANCH}
RUN mvn -T$(nproc) -DskipTests=true clean package
RUN mv nifi-assembly/target/nifi-*-SNAPSHOT-bin.zip nifi-bin.zip
RUN mv nifi-toolkit/nifi-toolkit-assembly/target/nifi-toolkit-*-SNAPSHOT-bin.zip nifi-toolkit-bin.zip


FROM openjdk:8-jre
LABEL maintainer="Apache NiFi <dev@nifi.apache.org>"
LABEL site="https://nifi.apache.org"

ARG UID=1000
ARG GID=1000

ENV NIFI_BASE_DIR=/opt/nifi
ENV NIFI_HOME ${NIFI_BASE_DIR}/nifi-current
ENV NIFI_TOOLKIT_HOME ${NIFI_BASE_DIR}/nifi-toolkit-current

ENV NIFI_PID_DIR=${NIFI_HOME}/run
ENV NIFI_LOG_DIR=${NIFI_HOME}/logs

COPY --from=build /usr/local/src/nifi/nifi-docker/dockerhub/sh ${NIFI_BASE_DIR}/scripts

# Setup NiFi user and create necessary directories
RUN groupadd -g ${GID} nifi || groupmod -n nifi `getent group ${GID} | cut -d: -f1` \
    && useradd --shell /bin/bash -u ${UID} -g ${GID} -m nifi \
    && mkdir -p ${NIFI_BASE_DIR} \
    && chown -R nifi:nifi ${NIFI_BASE_DIR} \
    && apt-get update \
    && apt-get install -y jq xmlstarlet procps

USER nifi

# Copy and expand Apache NiFi binary.
COPY --from=build /usr/local/src/nifi/nifi-bin.zip ${NIFI_BASE_DIR}/nifi-bin.zip
RUN unzip ${NIFI_BASE_DIR}/nifi-bin.zip -d ${NIFI_BASE_DIR} \
    && rm ${NIFI_BASE_DIR}/nifi-bin.zip \
    && mv ${NIFI_BASE_DIR}/nifi-* ${NIFI_HOME} \
    && mkdir -p ${NIFI_HOME}/conf \
    && mkdir -p ${NIFI_HOME}/database_repository \
    && mkdir -p ${NIFI_HOME}/flowfile_repository \
    && mkdir -p ${NIFI_HOME}/content_repository \
    && mkdir -p ${NIFI_HOME}/provenance_repository \
    && mkdir -p ${NIFI_HOME}/state \
    && mkdir -p ${NIFI_LOG_DIR}

# Copy and expand Apache NiFi Toolkit binary.
COPY --from=build /usr/local/src/nifi/nifi-toolkit-bin.zip ${NIFI_BASE_DIR}/nifi-toolkit-bin.zip
RUN unzip ${NIFI_BASE_DIR}/nifi-toolkit-bin.zip -d ${NIFI_BASE_DIR} \
    && rm ${NIFI_BASE_DIR}/nifi-toolkit-bin.zip \
    && mv ${NIFI_BASE_DIR}/nifi-toolkit-* ${NIFI_TOOLKIT_HOME}

VOLUME ${NIFI_LOG_DIR} \
       ${NIFI_HOME}/conf \
       ${NIFI_HOME}/database_repository \
       ${NIFI_HOME}/flowfile_repository \
       ${NIFI_HOME}/content_repository \
       ${NIFI_HOME}/provenance_repository \
       ${NIFI_HOME}/state

# Clear nifi-env.sh in favour of configuring all environment variables in the Dockerfile
RUN echo "#!/bin/sh\n" > $NIFI_HOME/bin/nifi-env.sh

# Web HTTP(s) & Socket Site-to-Site Ports
EXPOSE 8080 8443 10000

WORKDIR ${NIFI_HOME}

# Apply configuration and start NiFi
#
# We need to use the exec form to avoid running our command in a subshell and omitting signals,
# thus being unable to shut down gracefully:
# https://docs.docker.com/engine/reference/builder/#entrypoint
#
# Also we need to use relative path, because the exec form does not invoke a command shell,
# thus normal shell processing does not happen:
# https://docs.docker.com/engine/reference/builder/#exec-form-entrypoint-example
ENTRYPOINT ["../scripts/start.sh"]
