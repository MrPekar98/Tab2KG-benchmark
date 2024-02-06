#!/bin/bash

set -e

HOME=${PWD}
NETWORK="evaluation"

BBW="baselines/bbw/"
KEYWORD_KG_LINKER="baselines/keyword-kg-linker/"
LEXMA="baselines/lexma/"
EMBLOOKUP="baselines/emblookup/"
MAGIC="baselines/magic/"

mkdir -p results/
mkdir -p results/bbw/
mkdir -p results/emblookup/
mkdir -p results/keyword-kg-linker/
mkdir -p results/lexma/
mkdir -p results/magic/

docker pull searx/searx
docker network inspect ${NETWORK} >/dev/null 2>&1 || docker network create ${NETWORK}

docker build -t bbw -f ${BBW}bbw.dockerfile ${BBW}
docker build -t magic -f ${MAGIC}magic.dockerfile ${MAGIC}
docker build -t lexma -f ${LEXMA}lexma.dockerfile ${LEXMA}
docker build -t emblookup -f ${EMBLOOKUP}emblookup.dockerfile ${EMBLOOKUP}

git clone https://github.com/MrPekar98/kg-lookup.git
cd kg-lookup/

echo "Loading DBpedia 2016..."
./load.sh ../setup/tough_tables/dbpedia/ dbp_2016
docker stop vos
rm -rf import/

echo "Loading DBpedia 2022..."
./load.sh ../setup/kg/dbpedia/ dbp_2022
docker stop vos
rm -rf import/

echo "Loading Wikidata..."
./load.sh ../setup/tough_tables/wikidata/ wd
rm -rf import/

docker build -t kg-lookup . --no-cache
cd ..

LUCENE_DBP_2016="baselines/magic/lucene_dbp_2016/"
LUCENE_DBP_2022="baselines/magic/lucene_dbp_2022/"
LUCENE_WD="baselines/lexma/lucene_wd/"

mkdir -p ${LUCENE_DBP_2016}
mkdir -p ${LUCENE_DBP_2022}
mkdir -p ${LUCENE_WD}

echo "Loading Lucene of DBpedia 2016"
docker run --rm -d --network kg-lookup-network \
           -v ${PWD}/${LUCENE_DBP_2016}:/lucene \
           -p 7000:7000 \
           -e MEM=200g \
           -e GRAPH=dbp_2016 \
           -e VIRTUOSO=$(docker exec vos bash -c "hostname -I") \
           --name kg-lookup-service kg-lookup
sleep 2m
curl http://localhost:7000/index
docker stop kg-lookup-service
sleep 2m

echo "Loading Lucene of DBpedia 2022"
docker run --rm -d --network kg-lookup-network \
           -v ${PWD}/${LUCENE_DBP_2022}:/lucene \
           -p 7000:7000 \
           -e MEM=200g \
           -e GRAPH=dbp_2022 \
           -e VIRTUOSO=$(docker exec vos bash -c "hostname -I") \
           --name kg-lookup-service kg-lookup
sleep 2m
curl http://localhost:7000/index
docker stop kg-lookup-service
sleep 2m

echo "Loading Lucene of Wikidata"
docker run --rm -d --network kg-lookup-network \
           -v ${PWD}/${LUCENE_WD}:/lucene \
           -p 7000:7000 \
           -e MEM=200g \
           -e GRAPH=wd \
           -e VIRTUOSO=$(docker exec vos bash -c "hostname -I") \
           --name kg-lookup-service kg-lookup
sleep 2m
curl http://localhost:7000/index
docker stop kg-lookup-service
docker stop vos
