#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/"

# tFood
CORPUS="${BENCHMARK_DIR}semtab/tfood/horizontal/tables_subset/"

if [[ "${KG}" = "wd" && -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}magic/tfood_candidates/
    python3 main_candidates.py wikidata ${CORPUS} ${RESULT_DIR}magic/tfood_candidates/ ${ENDPOINT}
fi

# Tough Tables - DBpedia
CORPUS="${BENCHMARK_DIR}toughtables/dbpedia/tables_subset/"

if [[ "${KG}" = "dbp-10-2016" && -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}magic/tough_tables_dbp_candidates/
    python3 main_candidates.py dbpedia ${CORPUS} ${RESULT_DIR}magic/tough_tables_dbp_candidates/ ${ENDPOINT}
fi

# Wikitables 2013 - Wikidata
CORPUS="${BENCHMARK_DIR}wikitables_2013/tables_subset/"

if [[ "${KG}" = "wd" && -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}magic/wikitables-2013_wd_candidates/
    python3 main_candidates.py wikidata ${CORPUS} ${RESULT_DIR}magic/wikitables-2013_wd_candidates/ ${ENDPOINT}
fi
