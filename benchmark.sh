#!/bin/bash

set -e

IPS="$(hostname -I)"
IP_ARRAY=(${IPS})
IP=${ARRAY[0]}

# EmbLookup
docker run --rm -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results emblookup

# bbw
docker run --rm -d -v ${PWD}/searx:/etc/searx --network evaluation --name searx -e BASE_URL=http://localhost:3030/ searx/searx
docker run --rm -d -v ${PWD}/baselines/lexma/tdb_wd/:/tdb --network evaluation --name fuseki-service fuseki
sleep 2s
FUSEKI_IP=$(docker exec fuseki-service hostname -I)
docker run --rm --network -e FUSEKI=${FUSEKI_IP} evaluation -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results bbw
docker stop searx
docker stop fuseki-service

# Magic
docker run --rm --network evaluation -d -v ${PWD}/baselines/magic/tdb_dbp_2016/:/tdb -v ${PWD}/baselines/magic/lucene_dbp_2016/:/lucene -p 7000:7000 -e MEM=200g --name kg-lookup-service kg-lookup
sleep 2m
docker run --rm --network evaluation -e ENDPOINT=${IP} -e KG="dbp-10-2016" -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/baselines/magic/:/hdt -v ${PWD}/results:/results magic
docker stop kg-lookup-service

docker run --rm --network evaluation -d -v ${PWD}/baselines/magic/tdb_dbp_2022/:/tdb -v ${PWD}/baselines/magic/lucene_dbp_2022/:/lucene -p 7000:7000 -e MEM=200g --name kg-lookup-service kg-lookup
sleep 2m
docker run --rm --network evaluation -e ENDPOINT=${IP} -e KG="dbp-12-2022" -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/baselines/magic/:/hdt -v ${PWD}/results:/results magic
docker stop kg-lookup-service

docker run --rm --network evaluation -e ENDPOINT=${IP} -e KG="wd" -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/baselines/magic/:/hdt -v ${PWD}/results:/results magic

# LexMa
docker run --rm --network evaluation -d -v ${PWD}/baselines/magic/tdb_dbp_2016/:/tdb -v ${PWD}/baselines/magic/lucene_dbp_2016/:/lucene -p 7000:7000 -e MEM=200g --name kg-lookup-service kg-lookup
sleep 2m
docker run --rm --network evaluation -e ENDPOINT=${IP} -e KG=dbp_16 -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results lexma
docker stop kg-lookup-service

docker run --rm --network evaluation -d -v ${PWD}/baselines/magic/tdb_dbp_2022/:/tdb -v ${PWD}/baselines/magic/lucene_dbp_2022/:/lucene -p 7000:7000 -e MEM=200g --name kg-lookup-service kg-lookup
sleep 2m
docker run --rm --network evaluation -e ENDPOINT=${IP} -e KG=dbp_22 -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results lexma
docker stop kg-lookip-service

docker run --rm --network evaluation -d -v ${PWD}/baselines/lexma/tdb_wd/:/tdb -v ${PWD}/baselines/lexma/lucene_wd/:/lucene -p 7000:7000 -e MEM=200g --name kg-lookup-service kg-lookup
sleep 2m
docker run --rm --network evaluation -e ENDPOINT=${IP} -e KG=wd -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results lexma
docker stop kg-lookup-service
