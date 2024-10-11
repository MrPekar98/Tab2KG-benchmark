#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
TOUGH_TABLES_DBP=${BENCHMARK_DIR}toughtables/dbpedia/tables/
TOUGH_TABLES_WD=${BENCHMARK_DIR}toughtables/wikidata/tables/
WIKITABLES_2013=${BENCHMARK_DIR}wikitables_2013/tables/
WIKITABLES_2019=${BENCHMARK_DIR}wikitables_2019/tables/
DATA_DIR="data/"
TIME_LIMIT=480 # minutes

# ToughTables - Wikidata
if [[ -d ${TOUGH_TABLES_WD} ]]
then
    mkdir -p /results/emblookup/toughtables_wd_scalability
    python3 main.py "${TOUGH_TABLES_WD}" "${DATA_DIR}aliases/alias_wd.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_wd.csv" "${DATA_DIR}aliases_processed/aliases_processed_wd.csv" -h -T ${TIME_LIMIT}
    mv results.csv /results/emblookup/toughtables_wd_scalability
    mv runtimes.csv /results/emblookup/toughtables_wd_scalability
fi

# Wikitables 2013
if [[ -d ${WIKITABLES_2013} ]]
then
    mkdir -p /results/emblookup/wikitables_dbp_2013_scalability
    python3 main.py "${WIKITABLES_2013}" "${DATA_DIR}aliases/alias_dbp12-2022.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_dbp12-2022.csv" "${DATA_DIR}aliases_processed/aliases_processed_dbp12-2022.csv" -h -T ${TIME_LIMIT}
    mv results.csv /results/emblookup/wikitables_dbp_2013_scalability
    mv runtimes.csv /results/emblookup/wikitables_dbp_2013_scalability
fi

# Wikitables 2019
if [[ -d ${WIKITABLES_2019} ]]
then
    mkdir -p /results/emblookup/wikitables_dbp_2019_scalability
    python3 main.py "${WIKITABLES_2019}" "${DATA_DIR}aliases/alias_dbp12-2022.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_dbp12-2022.csv" "${DATA_DIR}aliases_processed/aliases_processed_dbp12-2022.csv" -h -T ${TIME_LIMIT}
    mv results.csv /results/emblookup/wikitables_dbp_2019_scalability
    mv runtimes.csv /results/emblookup/wikitables_dbp_2019_scalability
fi
