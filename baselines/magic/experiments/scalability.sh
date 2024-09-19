#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
TOUGH_TABLES_DBP=${BENCHMARK_DIR}toughtables/dbpedia/tables/
TOUGH_TABLES_WD=${BENCHMARK_DIR}toughtables/wikidata/tables/
WIKITABLES_2013=${BENCHMARK_DIR}wikitables_2013/tables/
WIKITABLES_2019=${BENCHMARK_DIR}wikitables_2019/tables/
SLEEP=8h

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

# Wikitables 2013
if [[ "${KG}" = "dbp-12-2022" && -d ${WIKITABLES_2013} ]]
then
    RESULTS="/results/magic/wikitables_dbp_2013_scalability"
    mkdir -p ${RESULTS}

    python3 main.py dbpedia "/hdt/${KG}.hdt" "${WIKITABLES_2013}" "${RESULTS}" ${ENDPOINT} &
    PID=$1
    sleep ${SLEEP}
    kill -9 ${PID}
fi

# Wikitables 2019
if [[ "${KG}" = "dbp-12-2022" && -d ${WIKITABLES_2019} ]]
then
    RESULTS="/results/magic/wikitables_dbp_2019_scalability"
    mkdir -p ${RESULTS}

    python3 main.py dbpedia "/hdt/${KG}.hdt" "${WIKITABLES_2019}" "${RESULTS}" ${ENDPOINT} &
    PID=$1
    sleep ${SLEEP}
    kill -9 ${PID}
fi
