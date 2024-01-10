#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
TOUGH_TABLES_DBP=${BENCHMARK_DIR}toughtables/dbpedia/tables/
TOUGH_TABLES_WD=${BENCHMARK_DIR}toughtables/wikidata/tables/
WIKITABLES=${BENCHMARK_DIR}/tables/
SLEEP=8h

# Tough Tables - DBpedia
python bbwWrapper.py ${TOUGH_TABLES_DBP} toughtables_dbp_scalability &
PID=$!
sleep ${SLEEP}
kill ${PID}

# Tough Tables - Wikidata
python bbwWrapper.py ${TOUGH_TABLES_WD} toughtables_wd_scalability &
PID=$1
sleep ${SLEEP}
kill ${PID}

# Wikitables
python bbwWrapper.py ${WIKITABLES} wikitables_scalability &
PID=$1
sleep ${SLEEP}
kill ${PID}
