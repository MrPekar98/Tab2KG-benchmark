#!/bin/bash

set -e

IPS="$(hostname -I)"
IP_ARRAY=(${IPS})
IP=${ARRAY[0]}

# EmbLookup
docker run --rm -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results emblookup

# bbw
docker run --rm -d -v ${PWD}/searx:/etc/searx --network evaluation --name searx -e BASE_URL=http://localhost:3030/ searx/searx
docker run --rm --network evaluation -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results bbw
docker stop searx

# Magic
docker run -d -v ${PWD}/baselines/magic/tdb_dbp_2016/:/tdb -v ${PWD}/baselines/magic/lucene_dbp_2016/:/lucene -p 7000:7000 --name kg-lookup-service kg-lookup
sleep 2m
docker run --rm --network evaluation -e ENDPOINT=${IP} -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results magic_dbp-10-2016
docker stop kg-lookup-service
docker container rm kg-lookup-service

docker run -d -v ${PWD}/baselines/magic/tdb_dbp_2022/:/tdb -v ${PWD}/baselines/magic/lucene_dbp_2022/:/lucene -p 7000:7000 --name kg-lookup-service kg-lookup
docker run --rm --network evaluation -e ENDPOINT=${IP} -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results magic_dbp-12-2022
docker stop kg-lookup-service
docker container rm kg-lookup-service

docker run --rm --network evaluation -e ENDPOINT=${IP} -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results magic_wd

# Keyword-kg-linker

# LexMa
