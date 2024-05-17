#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
TOUGH_TABLES_DBP=${BENCHMARK_DIR}toughtables/dbpedia/tables/
TOUGH_TABLES_WD=${BENCHMARK_DIR}toughtables/wikidata/tables/
WIKITABLES=${BENCHMARK_DIR}wikitables_2013/tables/
SLEEP=8h

# ToughTables - DBpedia
if [[ "${KG}" = "dbp-10-2016" && -d ${TOUGH_TABLES_DBP} ]]
then
    RESULTS="/results/magic/toughtables_dbp_scalability"
    mkdir -p ${RESULTS}

    python3 main.py dbpedia "/hdt/${KG}.hdt" "${TOUGH_TABLES_DBP}" "${RESULTS}" ${ENDPOINT} &
    PID=$1
    sleep ${SLEEP}
    kill -9 ${PID}
fi

# ToughTables - Wikidata
if [[ "${KG}" = "wd" && -d ${TOUGH_TABLES_WD} ]]
then
    RESULTS="/results/magic/toughtables_wd_scalability"
    mkdir -p ${RESULTS}

    python3 main.py wikidata "/hdt/${KG}.hdt" "${TOUGH_TABLES_WD}" "${RESULTS}" ${ENDPOINT} &
    PID=$1
    sleep ${SLEEP}
    kill -9 ${PID}
fi

# Wikitables
if [[ "${KG}" = "dbp-12-2022" && -d ${WIKITABLES} ]]
then
    RESULTS="/results/magic/wikitables_dbp_2013_scalability"
    mkdir -p ${RESULTS}

    python3 main.py dbpedia "/hdt/${KG}.hdt" "${WIKITABLES}" "${RESULTS}" ${ENDPOINT} &
    PID=$1
    sleep ${SLEEP}
    kill -9 ${PID}
fi
