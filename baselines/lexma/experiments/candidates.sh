#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/"

if [[ "${KG}" = "dbp_16" ]]
then
    # Tough Tables - DBpedia
    mkdir -p ${RESULT_DIR}lexma/toughtables_dbp_candidates/
    CORPUS="${BENCHMARK_DIR}toughtables/dbpedia/tables_subset/"

    if [[ -d ${CORPUS} ]]
    then
        python lexma_candidates.py dbpedia ${CORPUS} ${RESULT_DIR}lexma/toughtables_dbp_candidates/ 10 "http://${ENDPOINT}:7000/"
    fi
fi

if [[ "${KG}" = "dbp_22" ]]
then
    # Wikitables 2019 - DBpedia
    mkdir -p ${RESULT_DIR}lexma/wikitables_2019_dbp_candidates/
    CORPUS="${BENCHMARK_DIR}wikitables_2019/tables_subset/"

    if [[ -d ${CORPUS} ]]
    then
        python lexma_candidates.py dbpedia ${CORPUS} ${RESULT_DIR}lexma/wikitables_2019_dbp_candidates/ 10 "http://${ENDPOINT}:7000/"
    fi
fi
