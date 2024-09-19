#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
TOUGH_TABLES_WD=${BENCHMARK_DIR}toughtables/wikidata/tables/
WIKITABLES_2013=${BENCHMARK_DIR}wikitables_2013/tables/
WIKITABLES_2019=${BENCHMARK_DIR}wikitables_2019/tables/
SLEEP=8h

# ToughTables - Wikidata
if [[ "${KG}" = "wd" && -d ${TOUGH_TABLES_WD} ]]
then
    RESULTS="/results/lexma/toughtables_wd_scalability"
    mkdir -p ${RESULTS}

    python lexma.py wikidata "${TOUGH_TABLES_WD}" ${RESULTS} 10 "http://${ENDPOINT}:7000/" &
    PID=$1
    sleep ${SLEEP}
    kill -9 ${PID}
fi

# Wikitables 2013
if [[ "${KG}" = "dbp_22" && -d ${WIKITABLES_2013} ]]
then
    RESULTS="/results/lexma/wikitables_dbp_2013_scalability"
    mkdir -p ${RESULTS}

    python lexma.py dbpedia "${WIKITABLES_2013}" ${RESULTS} 10 "http://${ENDPOINT}:7000/" &
    PID=$1
    sleep ${SLEEP}
    kill -9 ${PID}
fi

# Wikitables 2019
if [[ "${KG}" = "dbp_22" && -d ${WIKITABLES_2019} ]]
then
    RESULTS="/results/lexma/wikitables_dbp_2019_scalability"
    mkdir -p ${RESULTS}

    python lexma.py dbpedia "${WIKITABLES_2019}" ${RESULTS} 10 "http://${ENDPOINT}:7000/" &
    PID=$1
    sleep ${SLEEP}
    kill -9 ${PID}
fi
