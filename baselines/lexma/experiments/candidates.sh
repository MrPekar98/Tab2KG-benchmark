#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/"

if [[ "${KG}" = "wd" ]]
then
    # tFood
    mkdir -p ${RESULT_DIR}lexma/tfood_candidates/
    CORPUS="${BENCHMARK_DIR}semtab/tfood/horizontal/tables_subset/"

    if [[ -d ${CORPUS} ]]
    then
        python lexma_candidates.py wikidata ${CORPUS} ${RESULT_DIR}lexma/tfood_candidates/ 10 "http://${ENDPOINT}:7000/"
    fi

    # Wikitables 2013 - Wikidata
    mkdir -p ${RESULT_DIR}lexma/wikitables_2013_wd_candidates/
    CORPUS="${BENCHMARK_DIR}wikitables_2013/tables_subset/"

    if [[ -d ${CORPUS} ]]
    then
        python lexma_candidates.py wikidata ${CORPUS} ${RESULT_DIR}lexma/wikitables_2013_wd_candidates/ 10 "http://${ENDPOINT}:7000/"
    fi
fi

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
