#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
TOUGH_TABLES_DBP=${BENCHMARK_DIR}toughtables/dbpedia/tables/
TOUGH_TABLES_WD=${BENCHMARK_DIR}toughtables/wikidata/tables/
WIKITABLES=${BENCHMARK_DIR}wikitables_2013/tables/
SLEEP=8h

# ToughTables - DBpedia
if [[ "${KG}" = "dbp_16" ]]
then
    RESULTS="/results/lexma/toughtables_dbp_scalability"
    mkdir -p ${RESULTS}

    python lexma.py dbpedia "${TOUGH_TABLES_DBP}" ${RESULTS} 10 "http://${ENDPOINT}:7000/" &
    PID=$1
    sleep ${SLEEP}
    kill ${PID}
fi

# ToughTables - Wikidata
if [[ "${KG}" = "wd" ]]
then
    RESULTS="/results/lexma/toughtables_wd_scalability"
    mkdir -p ${RESULTS}

    python lexma.py wikidata "${TOUGH_TABLES_WD}" ${RESULTS} 10 "http://${ENDPOINT}:7000/" &
    PID=$1
    sleep ${SLEEP}
    kill ${PID}
fi

# Wikitables
if [[ "${KG}" = "dbp_22" ]]
then
    RESULTS="/results/lexma/wikitables_dbp_2013_scalability"
    mkdir -p ${RESULTS}

    python lexma.py dbpedia "${WIKITABLES}" ${RESULTS} 10 "http://${ENDPOINT}:7000/" &
    PID=$1
    sleep ${SLEEP}
    kill ${PID}
fi
