#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
DATA_DIR="data/"

# Tough Tables - DBpedia
mkdir -p /results/emblookup/toughtables_dbp_candidates/
CORPUS="${BENCHMARK_DIR}toughtables/dbpedia/tables_subset/"
python3 main.py ${CORPUS} "${DATA_DIR}aliases/alias_dbp10-2016.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_dbp10-2016.csv" "${DATA_DIR}aliases_processed/aliases_processed_dbp10-2016.csv" -h
mv results.csv /results/emblookup/toughtables_dbp_candidates/

# Wikitables 2019 - DBpedia
mkdir -p /results/emblookup/wikitables_2019_dbp_candidates/
CORPUS="${BENCHMARK_DIR}wikitables_2019/tables_subset/"
python3 main.py ${CORPUS} "${DATA_DIR}aliases/alias_dbp12-2022.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_dbp12-2022.csv" "${DATA_DIR}aliases_processed/aliases_processed_dbp12-2022.csv" -h
mv results.csv /results/emblookup/wikitables_2019_dbp_candidates/
