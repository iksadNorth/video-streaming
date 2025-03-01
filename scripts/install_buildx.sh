#!/bin/bash


export DOCKER_BUILDKIT=1 # 빌드킷 활성화
docker build --platform=local -o . https://github.com/docker/buildx.git
mkdir -p ~/.docker/cli-plugins
mv buildx ~/.docker/cli-plugins/docker-buildx
