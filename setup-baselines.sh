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
docker build -t magic_dbp-10-2016 -f ${MAGIC}magic.dockerfile --build-arg KG="dbp-10-2016" ${MAGIC}
docker build -t magic_dbp-03-2022 -f ${MAGIC}magic.dockerfile --build-arg KG="dbp-03-2022" ${MAGIC}
docker build -t magic_wd -f ${MAGIC}magic.dockerfile --build-arg KG="wd" ${MAGIC}
docker build -t lexma -f ${LEXMA}lexma.dockerfile ${LEXMA}
docker build -t emblookup -f ${EMBLOOKUP}emblookup.dockerfile ${EMBLOOKUP}

git clone https://github.com/MrPekar98/kg-lookup.git
cd kg-lookup/
echo "Loading DBpedia 2016..."
./load.sh ../setup/tough_tables/dbpedia/
mv tdb/ ../baselines/magic/tdb_dbp_2016/

echo "Loading DBpedia 2022..."
./load.sh ../setup/kg/dbpedia/
mv tdb/ ../baselines/magic/tdb_dbp_2022/

echo "Loading Wikidata..."
./load.sh ../setup/tough_tables/wikidata/
mv tdb/ ../baselines/lexma/tdb_wd/

docker build -t kg-lookup .
cd ..

mkdir -p baselines/magic/lucene_dbp_2016/
mkdir -p baselines/magic/lucene_dbp_2022/
mkdir -p baselines/lexma/lucene_wd/

docker run --rm -d -v ${PWD}/baselines/magic/tdb_dbp_2016/:/tdb -v ${PWD}/baselines/magic/lucene_dbp_2016/:/lucene -p 7000:7000 --name kg-lookup-service kg-lookup
sleep 2m
curl http://localhost:7000/index
docker stop kg-lookup-service

docker run --rm -d -v ${PWD}/baselines/magic/tdb_dbp_2022/:/tdb -v ${PWD}/baselines/magic/lucene_dbp_2022/:/lucene -p 7000:7000 --name kg-lookup-service kg-lookup
sleep 2m
curl http://localhost:7000/index
docker stop kg-lookup-service

docker run --rm -d -v ${PWD}/baselines/lexma/tdb_wd/:/tdb -v ${PWD}/baselines/lexma/lucene_wd/:/lucene -p 7000:7000 --name kg-lookup-service kg-lookup
sleep 2m
curl http://localhost:7000/index
docker stop kg-lookup-service
