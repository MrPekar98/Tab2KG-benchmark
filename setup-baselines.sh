#!/bin/bash

set -e

HOME=${PWD}
NETWORK="evaluation"

BBW="baselines/bbw/"
LEXMA="baselines/lexma/"
EMBLOOKUP="baselines/emblookup/"
MAGIC="baselines/magic/"
CITYSTI="baselines/citysti/"

mkdir -p results/
mkdir -p results/bbw/
mkdir -p results/emblookup/
mkdir -p results/lexma/
mkdir -p results/magic/
mkdir -p results/musted/
mkdir -p results/citysti/

docker pull searx/searx
docker network inspect ${NETWORK} >/dev/null 2>&1 || docker network create ${NETWORK}

docker build -t bbw -f ${BBW}bbw.dockerfile ${BBW}
docker build -t magic -f ${MAGIC}magic.dockerfile ${MAGIC}
docker build -t lexma -f ${LEXMA}lexma.dockerfile ${LEXMA}
docker build -t emblookup -f ${EMBLOOKUP}emblookup.dockerfile ${EMBLOOKUP}
docker build -t citysti -f ${CITYSTI}citysti.dockerfile ${CITYSTI}

tar -xf entity_cells_tt_wd.txt.tar.gz
gzip -d entity_cells_wt_wd.txt.gz
tar -xf entity_cells_ht.txt.tar.gz
mv entity_cells.txt benchmarks/toughtables/wikidata/gt/entity_cells.txt
mv entity_cells_wt_wd.txt benchmarks/wikitables_2019/gt/wikidata/entity_cells.txt
mv entity_cells_ht.txt.tar.gz benchmarks/semtab/HardTables/gt/entity_cells.txt

DBP_16_DIR="setup/tough_tables/dbpedia/"
DBP_22_DIR="setup/kg/dbpedia/"
WD_DIR="setup/tough_tables/wikidata/"

git clone https://github.com/MrPekar98/kg-lookup.git
cd kg-lookup/

echo "Loading DBpedia 2016..."
./load.sh ../${DBP_16_DIR} dbp_2016
docker stop vos
rm -rf import/

echo "Loading DBpedia 2022..."
./load.sh ../${DBP_22_DIR} dbp_2022
docker stop vos
rm -rf import/

echo "Loading Wikidata..."
./load.sh ../${WD_DIR} wd
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
           -v ${PWD}/${DBP_16_DIR}:/kg \
           -p 7000:7000 \
           -e MEM=200g \
           -e GRAPH=dbp_2016 \
           -e VIRTUOSO=$(docker exec vos bash -c "hostname -I") \
           --name kg-lookup-service kg-lookup
sleep 2m
curl http://localhost:7000/index?domain=dbpedia
docker stop kg-lookup-service
sleep 2m

echo "Loading Lucene of DBpedia 2022"
docker run --rm -d --network kg-lookup-network \
           -v ${PWD}/${LUCENE_DBP_2022}:/lucene \
           -v ${PWD}/${DBP_22_DIR}:/kg \
           -p 7000:7000 \
           -e MEM=200g \
           -e GRAPH=dbp_2022 \
           -e VIRTUOSO=$(docker exec vos bash -c "hostname -I") \
           --name kg-lookup-service kg-lookup
sleep 2m
curl http://localhost:7000/index?domain=dbpedia
docker stop kg-lookup-service
sleep 2m

echo "Loading Lucene of Wikidata"
docker run --rm -d --network kg-lookup-network \
           -v ${PWD}/${LUCENE_WD}:/lucene \
           -v ${PWD}/${WD_DIR}:/kg \
           -p 7000:7000 \
           -e MEM=200g \
           -e GRAPH=wd \
           -e VIRTUOSO=$(docker exec vos bash -c "hostname -I") \
           --name kg-lookup-service kg-lookup
sleep 2m
curl http://localhost:7000/index?domain=wikidata
docker stop kg-lookup-service
docker stop vos
