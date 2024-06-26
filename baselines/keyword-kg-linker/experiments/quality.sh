#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/keyword-kg-linker/"

cd ..
docker start neo4j_wd
sleep 20m

# SemTab HardTables
CORPUS="${BENCHMARK_DIR}/semtab/HardTables/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}/HardTables/keyword/ ${RESULT_DIR}/HardTables/embedding/
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/HardTables/keyword/ -dir wd/ -config config.json -type keyword
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/HardTables/embedding/ -dir wd/ -config config.json -type embedding
fi

# tFood
CORPUS="${BENCHMARK_DIR}/semtab/tfood/horizontal/test/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}/tfood/keyword/ ${RESULT_DIR}/tfood/embedding/
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/tfood/keyword/ -dir wd/ -config config.json -type keyword
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/tfood/embedding/ -dir wd/ -config config.json -type embedding
fi

# Tough Tables - Wikidata
CORPUS="${BENCHMARK_DIR}/toughtables/wikidata/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}/toughtables_wd/keyword/ ${RESULT_DIR}/toughtables_wd/embedding/
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/toughtables_wd/keyword/ -dir wd/ -config config.json -type keyword
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/toughtables_wd/embedding/ -dir wd/ -config config.json -type embedding

# Wikitables 2013 - Wikidata
CORPUS="${BENCHMARK_DIR}/wikitables_2013/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}/wikitables_2013_wd/keyword/ ${RESULT_DIR}/wikitables_2013_wd/embedding/
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/wikitables_2013_wd/keyword/ -dir wd/ -config config.json -type keyword
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/wikitables_2013_wd/embedding/ -dir wd/ -config config.json -type embedding
fi

# Wikitables 2019 - Wikidata
CORPUS="${BENCHMARK_DIR}/wikitables_2019/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}/wikitables_2019_wd/keyword/ ${RESULT_DIR}/wikitables_2019_wd/embedding/
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/wikitables_2019_wd/keyword/ -dir wd/ -config config.json -type keyword
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/wikitables_2019_wd/embedding/ -dir wd/ -config config.json -type embedding
fi

docker stop neo4j_wd
sleep 1m
docker start neo4j_dbp16
sleep 2m

# Tough Tables - DBpedia
CORPUS="${BENCHMARK_DIR}/toughtables/dbpedia/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}/toughtables_dbp/keyword/ ${RESULT_DIR}/toughtables_dbp/embedding/
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/toughtables_dbp/keyword/ -dir dbp_16/ -config config.json -type keyword
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/toughtables_dbp/embedding/ -dir dbp_16/ -config config.json -type embedding
fi

docker stop neo4j_dbp16
sleep 1m
docker start neo4j_dbp22
sleep 10m

# Wikitables 2013 - DBpedia
CORPUS="${BENCHMARK_DIR}/wikitables_2013/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    mkdir -p ${RESULTS_DIR}/wikitables_2013_dbp/keyword/ ${RESULTS_DIR}/wikitables_2013_dbp/embedding/
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/wikitables_2013_dbp/keyword/ -dir dbp_22/ -config config.json -type keyword
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/wikitables_2013_dbp/embedding/ -dir dbp_22/ -config config.json -type embedding
fi

# Wikitables 2019 - DBpedia
CORPUS="${BENCHMARK_DIR}/wikitables_2013/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}/wikitables_2019_dbp/keyword/ ${RESULT_DIR}/wikitables_2019_dbp/embedding/
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/wikitables_2019_dbp/keyword/ -dir dbp_22/ -config config.json -type keyword
    ./linker.sh -tables ${CORPUS} -output ${RESULT_DIR}/wikitables_2019_dbp/embedding/ -dir dbp_22/ -config config.json -type embedding
fi

docker stop neo4j_dbp22
sleep 1m
cd experiments/
