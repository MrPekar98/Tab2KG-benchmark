#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/"

if [[ "${KG}" = "wd" ]]
then
    # HardTables
    mkdir -p ${RESULT_DIR}lexma/hardtables/
    CORPUS="${BENCHMARK_DIR}semtab/HardTables/tables_subset/"

    if [[ -d ${CORPUS} ]]
    then
        python lexma.py wikidata ${CORPUS} ${RESULT_DIR}lexma/hardtables/ 10 "http://${ENDPOINT}:7000/"
    fi

    # tFood
    mkdir -p ${RESULT_DIR}lexma/tfood/
    CORPUS="${BENCHMARK_DIR}semtab/tfood/horizontal/tables_subset/"

    if [[ -d ${CORPUS} ]]
    then
        python lexma.py wikidata ${CORPUS} ${RESULT_DIR}lexma/tfood/ 10 "http://${ENDPOINT}:7000/"
    fi

    # Tough Tables - Wikidata
    mkdir -p ${RESULT_DIR}lexma/toughtables_wd/
    CORPUS="${BENCHMARK_DIR}toughtables/wikidata/tables_subset/"

    if [[ -d ${CORPUS} ]]
    then
        python lexma.py wikidata ${CORPUS} ${RESULT_DIR}lexma/toughtables_wd/ 10 "http://${ENDPOINT}:7000/"
    fi

    # Wikitables 2013 - Wikidata
    mkdir -p ${RESULT_DIR}lexma/wikitables_2013_wd/
    CORPUS="${BENCHMARK_DIR}wikitables_2013/tables_subset/"

    if [[ -d ${CORPUS} ]]
    then
        python lexma.py wikidata ${CORPUS} ${RESULT_DIR}lexma/wikitables_2013_wd/ 10 "http://${ENDPOINT}:7000/"
    fi

    # Wikitables 2019 - Wikidata
    mkdir -p ${RESULT_DIR}lexma/wikitables_2019_wd/
    CORPUS="${BENCHMARK_DIR}wikitables_2019/tables_subset/"

    if [[ -d ${CORPUS} ]]
    then
        python lexma.py wikidata ${CORPUS} ${RESULT_DIR}lexma/wikitables_2019_wd/ 10 "http://${ENDPOINT}:7000/"
    fi
fi

if [[ "${KG}" = "dbp_16" ]]
then
    # Tough Tables - DBpedia
    mkdir -p ${RESULT_DIR}lexma/toughtables_dbp/
    CORPUS="${BENCHMARK_DIR}toughtables/dbpedia/tables_subset/"

    if [[ -d ${CORPUS} ]]
    then
        python lexma.py dbpedia ${CORPUS} ${RESULT_DIR}lexma/toughtables_dbp/ 10 "http://${ENDPOINT}:7000/"
    fi
fi

if [[ "${KG}" = "dbp_22" ]]
then
    # Wikitables 2013 - DBpedia
    mkdir -p ${RESULT_DIR}lexma/wikitables_2013_dbp/
    CORPUS="${BENCHMARK_DIR}wikitables_2013/tables_subset/"

    if [[ -d ${CORPUS} ]]
    then
        python lexma.py dbpedia ${CORPUS} ${RESULT_DIR}lexma/wikitables_2013_dbp/ 10 "http://${ENDPOINT}:7000/"
    fi

    # Wikitables 2019 - DBpedia
    mkdir -p ${RESULT_DIR}lexma/wikitables_2019_dbp/
    CORPUS="${BENCHMARK_DIR}wikitables_2019/tables_subset/"

    if [[ -d ${CORPUS} ]]
    then
        python lexma.py dbpedia ${CORPUS} ${RESULT_DIR}lexma/wikitables_2019_dbp/ 10 "http://${ENDPOINT}:7000/"
    fi
fi
