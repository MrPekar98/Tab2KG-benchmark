#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
TOUGH_TABLES_DBP=${BENCHMARK_DIR}toughtables/dbpedia/tables/
TOUGH_TABLES_WD=${BENCHMARK_DIR}toughtables/wikidata/tables/
WIKITABLES=${BENCHMARK_DIR}wikitables_2013/tables/
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

# Wikitables
if [[ "${KG}" = "dbp_22" && -d ${WIKITABLES} ]]
then
    RESULTS="/results/lexma/wikitables_dbp_2013_scalability"
    mkdir -p ${RESULTS}

    python lexma.py dbpedia "${WIKITABLES}" ${RESULTS} 10 "http://${ENDPOINT}:7000/" &
    PID=$1
    sleep ${SLEEP}
    kill -9 ${PID}
fi
