#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/"

if [[ "${KG}" = "wd" ]]
then
    # HardTables
    mkdir -p ${RESULT_DIR}lexma/hardtables/
    python lexma.py wikidata ${BENCHMARK_DIR}semtab/HardTables/tables_subset/ ${RESULT_DIR}lexma/hardtables/ 10 "http://${ENDPOINT}:7000/"

    # tFood
    mkdir -o {RESULT_DIR}lexma/tfood/
    python lexma.py wikidata ${BENCHMARK_DIR}semtab/tfood/horizontal/tables_subset/ ${RESULT_DIR}lexma/tfood/ 10 "http://${ENDPOINT}:7000/"

    # Tough Tables - Wikidata
    mkdir -p ${RESULT_DIR}lexma/toughtables_wd/
    python lexma.py wikidata ${BENCHMARK_DIR}toughtables/wikidata/tables_subset/ ${RESULT_DIR}lexma/toughtables_wd/ 10 "http://${ENDPOINT}:7000/"

    # Wikitables 2013 - Wikidata
    mkdir -p ${RESULT_DIR}lexma/wikitables_2013_wd/
    python lexma.py wikidata ${BENCHMARK_DIR}wikitables_2013/tables_subset/ ${RESULT_DIR}lexma/wikitables_2013_wd/ 10 "http://${ENDPOINT}:7000/"

    # Wikitables 2019 - Wikidata
    mkdir -p ${RESULT_DIR}lexma/wikitables_2019_wd/
    python lexma.py wikidata ${BENCHMARK_DIR}wikitables_2013/tables_subset/ ${RESULT_DIR}lexma/wikitables_2019_wd/ 10 "http://${ENDPOINT}:7000/"
fi

if [[ "${KG}" = "dbp_16" ]]
then
    # Tough Tables - DBpedia
    mkdir -p ${RESULT_DIR}lexma/toughtables_dbp/
    python lexma.py dbpedia ${BENCHMARK_DIR}toughtables/dbpedia/tables_subset/ ${RESULT_DIR}lexma/toughtables_dbp/ 10 "http://${ENDPOINT}:7000/"
fi

if [[ "${KG}" = "dbp_22" ]]
then
    # Wikitables 2013 - DBpedia
    mkdir -p ${RESULT_DIR}lexma/wikitables_2013_dbp/
    python lexma.py dbpedia ${BENCHMARK_DIR}wikitables_2013/tables_subset/ ${RESULT_DIR}lexma/wikitables_2013_dbp/ 10 "http://${ENDPOINT}:7000/"

    # Wikitables 2019 - DBpedia
    mkdir -p ${RESULT_DIR}lexma/wikitables_2019_dbp/
    python lexma.py dbpedia ${BENCHMARK_DIR}wikitables_2019/tables_subset/ ${RESULT_DIR}lexma/wikitables_2019_dbp/ 10 "http://${ENDPOINT}:7000/"
fi
