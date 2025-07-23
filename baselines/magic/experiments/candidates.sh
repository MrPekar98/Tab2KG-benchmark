#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/"

# Tough Tables - DBpedia
CORPUS="${BENCHMARK_DIR}toughtables/dbpedia/tables_subset/"

if [[ "${KG}" = "dbp-10-2016" && -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}magic/tough_tables_dbp_candidates/
    python3 main_candidates.py dbpedia ${CORPUS} ${RESULT_DIR}magic/tough_tables_dbp_candidates/ ${ENDPOINT}
fi

# Wikitables 2013 - DBpedia
CORPUS="${BENCHMARK_DIR}wikitables_2013/tables_subset/"

if [[ "${KG}" = "dbp-12-2022" && -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}magic/wikitables-2013_dbp_candidates/
    python3 main_candidates.py dbpedia ${CORPUS} ${RESULT_DIR}magic/wikitables-2013_dbp_candidates/ ${ENDPOINT}
fi

# Wikitables 2019 - DBpedia
CORPUS="${BENCHMARK_DIR}wikitables_2019/tables_subset/"

if [[ "${KG}" = "dbp-12-2022" && -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}magic/wikitables-2019_dbp_candidates/
    python3 main_candidates.py dbpedia ${CORPUS} ${RESULT_DIR}magic/wikitables-2019_dbp_candidates/ ${ENDPOINT}
fi

# HardTables - Wikidata
CORPUS="${BENCHMARK_DIR}semtab/HardTables/tables_subset/"

if [[ "${KG}" = "wd" && -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}magic/hardtables_candidates/
    python3 main_candidates.py wikidata ${CPRPUS} ${RESULT_DIR}magic/hardtables_candidates/ ${ENDPOINT}
fi
