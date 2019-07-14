#!/bin/bash

CONTAINER_NAME="tw_streamer"
IMAGE_NAME="tw_streamer"

# docker build -t ${IMAGE_NAME} -f ../Dockerfile

docker stop ${CONTAINER_NAME}

docker rm ${CONTAINER_NAME}

docker run              \
    --name ${CONTAINER_NAME}  \
    -d                  \
    -e ACCESS_TOKEN=$ACCESS_TOKEN   \
    -e ACCESS_TOKEN_SECRET=$ACCESS_TOKEN_SECRET     \
    -e CONSUMER_KEY=$CONSUMER_KEY   \
    -e CONSUMER_SECRET=$CONSUMER_SECRET     \
    -e REDIS_HOST=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' redis-db) \
    --restart always \
    ${IMAGE_NAME}
