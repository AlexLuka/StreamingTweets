#!/bin/bash

docker run -p 6379:6379 -d --name redis-db --restart always redis
