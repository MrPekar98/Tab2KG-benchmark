#!/bin/bash

set -e

IPS="$(hostname -I)"
IP_ARRAY=(${IPS})
IP=${ARRAY[0]}

# EmbLookup
docker run --rm -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results emblookup

# bbw
docker run --rm -d -v ${PWD}/searx:/etc/searx --network evaluation --name searx -e BASE_URL=http://localhost:3030/ searx/searx
docker run --rm --name vos -d \
           --network evaluation \
           -v ${PWD}/kg-lookup/database:/database \
           -v ${PWD}/kg-lookup/import:/import \
           -t -p 1111:1111 -p 8890:8890 -i openlink/virtuoso-opensource-7:7
sleep 30s
VIRTUOSO_IP=$(docker exec vos bash -c "hostname -I")
docker run --rm -d --network evaluation \
        -v ${PWD}/baselines/lexma/lucene_wd/:/lucene \
        -p 7000:7000 \
        -e MEM=200g \
        -e GRAPH=wd \
        -e VIRTUOSO=${VIRUTOSO_IP} \
        --name kg-lookup-service kg-lookup
sleep 2m
docker run --rm --network evaluation -e ENDPOINT=${IP} -e VIRTUOSO=${VIRTUOSO_IP} -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results bbw
docker stop searx
docker stop vos

# Magic
docker run -it --rm -d --network kg-lookup-network \
           -v ${PWD}/baselines/magic/lucene_dbp_2016/:/lucene \
           -p 7000:7000 \
           -e MEM=200g \
           -e GRAPH=dbp_2016 \
           -e VIRTUOSO=$(docker exec vos bash -c "hostname -I") \
           --name kg-lookup-service kg-lookup
sleep 2m
docker run --rm --network kg-lookup-network -e ENDPOINT=${IP} -e KG="dbp-10-2016" -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/baselines/magic/:/hdt -v ${PWD}/results:/results magic
docker stop kg-lookup-service

docker run -it --rm -d --network kg-lookup-network \
           -v ${PWD}/baselines/magic/lucene_dbp_2022/:/lucene \
           -p 7000:7000 \
           -e MEM=200g \
           -e GRAPH=dbp_2022 \
           -e VIRTUOSO=$(docker exec vos bash -c "hostname -I") \
           --name kg-lookup-service kg-lookup
sleep 2m
docker run --rm --network kg-lookup-network -e ENDPOINT=${IP} -e KG="dbp-12-2022" -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/baselines/magic/:/hdt -v ${PWD}/results:/results magic
docker stop kg-lookup-service

docker run -it --rm -d --network kg-lookup-network \
           -v ${PWD}/baselines/lexma/lucene_wd/:/lucene \
           -p 7000:7000 \
           -e MEM=200g \
           -e GRAPH=wd \
           -e VIRTUOSO=$(docker exec vos bash -c "hostname -I") \
           --name kg-lookup-service kg-lookup
sleep 2m
docker run --rm --network evaluation -e ENDPOINT=${IP} -e KG="wd" -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/baselines/magic/:/hdt -v ${PWD}/results:/results magic
docker stop kg-lookup-service

# LexMa
docker run -it --rm -d --network kg-lookup-network \
           -v ${PWD}/baselines/magic/lucene_dbp_2016/:/lucene \
           -p 7000:7000 \
           -e MEM=200g \
           -e GRAPH=dbp_2016 \
           -e VIRTUOSO=$(docker exec vos bash -c "hostname -I") \
           --name kg-lookup-service kg-lookup
sleep 2m
docker run --rm --network kg-lookup-network -e ENDPOINT=${IP} -e KG=dbp_16 -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results lexma
docker stop kg-lookup-service

docker run -it --rm -d --network kg-lookup-network \
           -v ${PWD}/baselines/magic/lucene_dbp_2022/:/lucene \
           -p 7000:7000 \
           -e MEM=200g \
           -e GRAPH=dbp_2022 \
           -e VIRTUOSO=$(docker exec vos bash -c "hostname -I") \
           --name kg-lookup-service kg-lookup
sleep 2m
docker run --rm --network kg-lookup-network -e ENDPOINT=${IP} -e KG=dbp_22 -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results lexma
docker stop kg-lookip-service

docker run -it --rm -d --network kg-lookup-network \
           -v ${PWD}/baselines/lexma/lucene_wd/:/lucene \
           -p 7000:7000 \
           -e MEM=200g \
           -e GRAPH=wd \
           -e VIRTUOSO=$(docker exec vos bash -c "hostname -I") \
           --name kg-lookup-service kg-lookup
sleep 2m
docker run --rm --network kg-lookup-network -e ENDPOINT=${IP} -e KG=wd -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results lexma
docker stop kg-lookup-service

docker stop vos
