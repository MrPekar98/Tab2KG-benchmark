#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
DATA_DIR="data/"

echo "More training"
mv configs.json old_configs.json
mv more_training.json configs.json

# Tough Tables - Wikidata
mkdir -p /results/emblookup/toughtables_wd_more_training
CORPUS="${BENCHMARK_DIR}toughtables/wikidata/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    python3 main.py ${CORPUS} "${DATA_DIR}aliases/alias_wd.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_wd.csv" "${DATA_DIR}aliases_processed/aliases_processed_wd.csv" -h
    mv runtimes.csv /results/emblookup/toughtables_wd_more_training
    mv results.csv /results/emblookup/toughtables_wd_more_training
fi

# Wikitables 2019 - Wikidata
mkdir -p /results/emblookup/wikitables_2019_wd_more_training
CORPUS="${BENCHMARK_DIR}wikitables_2019/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    python3 main.py ${CORPUS} "${DATA_DIR}aliases/alias_wd.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_wd.csv" "${DATA_DIR}aliases_processed/aliases_processed_wd.csv" -h
    mv runtimes.csv /results/emblookup/wikitables_2019_wd_more_training
    mv results.csv /results/emblookup/wikitables_2019_wd_more_training
fi

echo "Less training"
mv configs.json more_training.json
mv less_training.json configs.json

# Tough Tables - Wikidata
mkdir -p /results/emblookup/toughtables_wd_less_training
CORPUS="${BENCHMARK_DIR}toughtables/wikidata/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    python3 main.py ${CORPUS} "${DATA_DIR}aliases/alias_wd.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_wd.csv" "${DATA_DIR}aliases_processed/aliases_processed_wd.csv" -h
    mv results.csv /results/emblookup/toughtables_wd_less_training
    mv results.csv /results/emblookup/toughtables_wd_less_training
fi

# Wikitables 2019 - Wikidata
mkdir -p /results/emblookup/wikitables_2019_wd_less_training
CORPUS="${BENCHMARK_DIR}wikitables_2019/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    python3 main.py ${CORPUS} "${DATA_DIR}aliases/alias_wd.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_wd.csv" "${DATA_DIR}aliases_processed/aliases_processed_wd.csv" -h
    mv results.csv /results/emblookup/wikitables_2019_wd_less_training
    mv results.csv /results/emblookup/wikitables_2019_wd_less_training
fi

mv configs.json less_training.json
mv old_configs.json configs.json
