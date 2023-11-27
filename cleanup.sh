#!/bin/bash

set -e

docker stop searx
docker network rm evaluation
docker rmi bbw

#docker rmi emblookup
