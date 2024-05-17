#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/keyword-kg-linker/"
TOUGH_TABLES_DBP=${BENCHMARK_DIR}toughtables/dbpedia/tables/
TOUGH_TABLES_WD=${BENCHMARK_DIR}toughtables/wikidata/tables/
WIKITABLES=${BENCHMARK_DIR}wikitables_2013/tables/
SLEEP=8h

cd ..

# ToughTables - DBpedia
if [[ -d ${TOUGH_TABLES_DBP} ]]
then
    RESULTS=${RESULT_DIR}/toughtables_dbp_scalability/
    mkdir -p ${RESULTS}/keyword/ ${RESULTS}/embedding/

    docker start neo4j_dbp16
    sleep 10m

    ./linker.sh -tables ${TOUGH_TABLES_DBP} -output ${RESULTS}/keyword/ -dir dbp_16/ -config config.json -type keyword &
    sleep ${SLEEP}
    docker stop keyword-kg-linker-container

    ./linker.sh -tables ${TOUGH_TABLES_DBP} -output ${RESULTS}/embedding/ -dir dbp_16/ -config config.json -type embedding
    sleep ${SLEEP}
    docker stop keyword-kg-linker-container

    docker stop neo4j_dbp16
    sleep 1m
fi

# ToughTables - Wikidata
if [[ -d ${TOUGH_TABLES_WD} ]]
then
    RESULTS=${RESULT_DIR}/toughtables_wd_scalability/
    mkdir -p ${RESULTS}/keyword/ ${RESULTS}/embedding/

    docker start neo4j_wd
    sleep 20m

    ./linker.sh -tables ${TOUGH_TABLES_WD} -output ${RESULTS}/keyword/ -dir wd/ -config config.json -type keyword
    sleep ${SLEEP}
    docker stop keyword-kg-linker-container

    ./linker.sh -tables ${TOUGH_TABLES_WD} -output ${RESULTS}/embedding/ -dir wd/ -config config.json -type embedding
    sleep ${SLEEP}
    docker stop keyword-kg-linker-container
fi

# Wikitables - Wikidata
if [[ -d ${WIKITABLES} ]]
then
    RESULTS=${RESULTS_DIR}/wikitables_wd_scalability/
    mkdir -p ${RESULTS}/keyword/ ${RESULTS}/embedding/

    ./linker.sh -tables ${WIKITABLES} -output ${RESULTS}/keyword -dir wd/ -config config.json -type keyword
    sleep ${SLEEP}
    docker stop keyword-kg-linker-container

    ./linker.sh -tables ${WIKITABLES} -output ${RESULTS}/embedding/ -dir wd/ -config config.json -type embdding
    sleep ${SLEEP}
    docker stop keyword-kg-linker-container

    docker stop neo4j_wd
    sleep 1m

    # Wikitables - DBpedia
    RESULTS=${RESULT_DIR}/wikitables_dbp_scalability/
    mkdir -p ${RESULTS}/keyword/ ${RESULTS}/embedding/

    docker start neo4j_dbp22
    sleep 10m

    ./linker.sh -tables ${WIKITABLES} -output ${RESULTS}/keyword/ -dir dbp_22/ -config config.json -type keyword
    sleep ${SLEEP}
    docker stop keyword-kg-linker-container

    ./linker.sh -tables ${WIKITABLES} -output ${RESULTS}/embedding/ -dir dbp_22/ -config config.json -type embedding
    sleep ${SLEEP}
    docker stop keyword-kg-linker-container

    docker stop neo4j_dbp22
    sleep 1m
fi

cd experiments/
