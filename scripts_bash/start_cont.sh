#!/bin/bash

docker run              \
    --name tw_streamer  \
    -d                  \
    -e ACCESS_TOKEN=$ACCESS_TOKEN   \
    -e ACCESS_TOKEN_SECRET=$ACCESS_TOKEN_SECRET     \
    -e CONSUMER_KEY=$CONSUMER_KEY   \
    -e CONSUMER_SECRET=$CONSUMER_SECRET     \
    -e REDIS_HOST=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' redis-db) \
    --restart always \
    tw_streamer