#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/keyword-kg-linker/"
TOUGH_TABLES_DBP=${BENCHMARK_DIR}toughtables/dbpedia/tables/
TOUGH_TABLES_WD=${BENCHMARK_DIR}toughtables/wikidata/tables/
WIKITABLES=${BENCHMARK_DIR}wikitables_2013/tables/
SLEEP=8h
MAX_DURATION=3600

cd ..

# ToughTables - DBpedia
docker start neo4j_dbp16
sleep 2m

RESULTS=${RESULT_DIR}/toughtables_dbp_scalability/
mkdir -p ${RESULTS}/keyword/ ${RESULTS}/embedding/

START=${SECONDS}

for TABLE in ${TOUGH_TABLES_DBP} ;\
do
    ./linker.sh -table ${TABLE} -output ${RESULTS}/keyword/ -dir dbp_16/ -config config.json -type keyword
    DURATION=$((${SECONDS} - ${START}))

    if [[ DURATION > ${MAX_DURATION} ]]
    then
        break
    fi
done

START=${SECONDS}

for TABLE in ${TOUGH_TABLES_DBP} ;\
do
        ./linker.sh -table ${TABLE} -output ${RESULTS}/embedding/ -dir dbp_16/ -config config.json -type embedding
        DURATION=$((${SECONDS} - ${START}))

        if [[ DURATION > ${MAX_DURATION} ]]
        then
            break
        fi
done

docker stop neo4j_dbp16
sleep 1m

# ToughTables - Wikidata
docker start neo4j_wd
sleep 2m

RESULTS=${RESULT_DIR}/toughtables_wd_scalability/
mkdir -p ${RESULTS}/keyword/ ${RESULTS}/embedding/

START=${SECONDS}

for TABLE in ${TOUGH_TABES_WD} ;\
do
    ./linker.sh -table ${TABLE} -output ${RESULTS}/keyword/ -dir wd/ -config config -type keyword
    DURATION=$((${SECONDS} - ${START}))

    if [[ ${DURATION} > ${MAX_DURATION} ]]
    then
        break
    fi
done

docker stop neo4j_wd
sleep 1m

# Wikitables
docker start neo4j_dbp22
sleep 2m

RESULTS=${RESULT_DIR}/wikitables_dbp_scalability/
mkdir -p ${RESULTS}/keyword ${RESULTS}/embedding/

START=${SECONDS}

for TABLE in ${WIKITABLES} ;\
do
    ./linker.sh -table ${TABLE} -output ${RESULTS}/keyword/ -dir dbp_22/ -config confing.json -type keyword
    DURATION=$((${SECONDS} - ${START}))

    if [[ ${DURATION} > ${MAX_DURATION} ]]
    then
        break
    fi
done

START=${START}

for TABLE in ${WIKITABLES} ;\
do
    ./linker.sh -table ${TABLE} -output ${RESULTS}/embedding/ -dir dbp_22/ -config config.json -type embdding
    DURATION=$((${SECONDS} - ${START}))

    if [[ ${DURATION} > ${MAX_DURATION} ]]
    then
        break
    fi
done

docker stop neo4j_dbp22
sleep 1m

cd experiments/
