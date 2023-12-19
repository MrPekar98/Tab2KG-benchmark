#!/bin/bash

docker stop searx
docker network rm evaluation
docker rmi bbw

docker rmi emblookup
docker rmi magic
docker rmi spotlight

rm -r kg-lookup/
