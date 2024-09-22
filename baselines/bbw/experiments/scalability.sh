#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
TOUGH_TABLES_WD=${BENCHMARK_DIR}toughtables/wikidata/tables/
WIKITABLES_2013=${BENCHMARK_DIR}wikitables_2013/tables/
WIKITABLES_2019=${BENCHMARK_DIR}wikitables_2019/tables/
SLEEP=8h

# Tough Tables - Wikidata
if [[ -d ${TOUGH_TABLES_WD} ]]
then
    python main.py ${TOUGH_TABLES_WD} /results/bbw/toughtables_wd_scalability/ ${ENDPOINT} ${VIRTUOSO} &
    PID=$1
    sleep ${SLEEP}
    kill ${PID}
fi

# Wikitables 2013
if [[ -d ${WIKITABLES_2013} ]]
then
    python main.py ${WIKITABLES_2013} /results/bbw/wikitables_2013_scalability/ ${ENDPOINT} ${VIRTUOSO} &
    PID=$1
    sleep ${SLEEP}
    kill ${PID}
fi

# Wikitables 2019
if [[ -d ${WIKITABLES_2019} ]]
then
    python main.py ${WIKITABLES_2019} /results/bbw/wikitables_2019_scalability/ ${ENDPOINT} ${VIRTUOSO} &
    PID=$1
    sleep ${SLEEP}
    kill ${PID}
fi
