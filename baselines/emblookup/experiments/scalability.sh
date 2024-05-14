#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
TOUGH_TABLES_DBP=${BENCHMARK_DIR}toughtables/dbpedia/tables/
TOUGH_TABLES_WD=${BENCHMARK_DIR}toughtables/wikidata/tables/
WIKITABLES=${BENCHMARK_DIR}wikitables_2013/tables/
DATA_DIR="data/"
SLEEP=8h

# ToughTables - DBpedia
mkdir -p /results/emblookup/toughtables_dbp_scalability

python3 main.py "${TOUGH_TABLES_DBP}" "${DATA_DIR}aliases/alias_dbp10-2016.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_dbp10-2016.csv" "${DATA_DIR}aliases_processed/aliases_processed_dbp10-2016.csv" -h &
PID=$1
sleep ${SLEEP}
kill -9 ${PID}

# ToughTables - Wikidata
mkdir -p /results/emblookup/toughtables_wd_scalability

python3 main.py "${TOUGH_TABLES_WD}" "${DATA_DIR}aliases/alias_wd.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_wd.csv" "${DATA_DIR}aliases_processed/aliases_processed_wd.csv" -h &
PID=$1
sleep ${SLEEP}
kill -9 ${PID}

# Wikitables
mkdir -p /results/emblookup/wikitables_dbp_2013_scalability

python3 main.py "${WIKITABLES}" "${DATA_DIR}aliases/alias_dbp12-2022.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_dbp12-2022.csv" "${DATA_DIR}aliases_processed/aliases_processed_dbp12-2022.csv" -h &
PID=$1
sleep ${SLEEP}
kill -9 ${PID}
