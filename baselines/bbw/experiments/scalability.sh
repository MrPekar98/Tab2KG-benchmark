#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
TOUGH_TABLES_WD=${BENCHMARK_DIR}toughtables/wikidata/tables/
WIKITABLES=${BENCHMARK_DIR}wikitables_2013/tables/
SLEEP=8h

# Tough Tables - Wikidata
python bbwWrapper.py ${TOUGH_TABLES_WD} toughtables_wd_scalability &
PID=$1
sleep ${SLEEP}
kill -9 ${PID}

# Wikitables
python bbwWrapper.py ${WIKITABLES} wikitables_scalability &
PID=$1
sleep ${SLEEP}
kill -9 ${PID}
