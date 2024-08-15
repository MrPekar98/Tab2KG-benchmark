#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
TOUGH_TABLES_DBP=${BENCHMARK_DIR}toughtables/dbpedia/tables/
TOUGH_TABLES_WD=${BENCHMARK_DIR}toughtables/wikidata/tables/
WIKITABLES=${BENCHMARK_DIR}wikitables_2013/tables/
DATA_DIR="data/"
SLEEP=8h

# ToughTables - Wikidata
if [[ -d ${TOUGH_TABLES_WD} ]]
then
    mkdir -p /results/emblookup/toughtables_wd_scalability

    python3 main.py "${TOUGH_TABLES_WD}" "${DATA_DIR}aliases/alias_wd.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_wd.csv" "${DATA_DIR}aliases_processed/aliases_processed_wd.csv" -h &
    PID=$1
    sleep ${SLEEP}
    kill -9 ${PID}
fi

# Wikitables
if [[ -d ${WIKITABLES} ]]
then
    mkdir -p /results/emblookup/wikitables_dbp_2013_scalability

    python3 main.py "${WIKITABLES}" "${DATA_DIR}aliases/alias_dbp12-2022.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_dbp12-2022.csv" "${DATA_DIR}aliases_processed/aliases_processed_dbp12-2022.csv" -h &
    PID=$1
    sleep ${SLEEP}
    kill -9 ${PID}
fi
