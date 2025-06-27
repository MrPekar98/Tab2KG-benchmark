#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/"

if [[ "${KG}" = "dbp16" ]]
then
    # Tough Tables - DBpedia
    mkdir -p ${RESULT_DIR}citysti/toughtables_dbp/
    CORPUS="${BENCHMARK_DIR}toughtables/dbpedia/tables_subset/"
    python gemini_main.py ${API_KEY} dbpedia ${CORPUS} ${RESULT_DIR}citysti/toughtables_dbp/
fi

if [[ "${KG}" = "dbp22" ]]
then
    # Wikitables 2013 - DBpedia
    mkdir -p ${RESULT_DIR}citysti/wikitables_2013_dbp/
    CORPUS="${BENCHMARK_DIR}wikitables_2013/tables_subset/"
    python gemini_main.py ${API_KEY} dbpedia ${CORPUS} ${RESULT_DIR}citysti/wikitables_2013_dbp/

    # Wikitables 2019 - DBpedia
    mkdir -p ${RESULT_DIR}citysti/wikitables_2019_dbp/
    CORPUS="${BENCHMARK_DIR}wikitables_2019/tables_subset/"
    python gemini_main.py ${API_KEY} dbpedia ${CORPUS} ${RESULT_DIR}citysti/wikitables_2019_dbp/
fi

if [[ "${KG}" = "wd" ]]
then
    # HardTables
    mkdir -p ${RESULT_DIR}citysti/hardtables/
    CORPUS="${BENCHMARK_DIR}semtab/HardTables/tables_subset/"
    python gemini_main.py ${API_KEY} wikidata ${CORPUS} ${RESULT_DIR}citysti/hardtables/

    # tFood
    mkdir -p ${RESULT_DIR}citysti/tfood/
    CORPUS="${BENCHMARK_DIR}toughtables/wikidata/tables_subset/"
    python gemini_main.py ${API_KEY} wikidata ${CORPUS} ${RESULT_DIR}citysti/tfood/

    # Tough Tables - Wikidata
    mkdir -p ${RESULT_DIR}citysti/toughtables_wd/
    CORPUS="${BENCHMARK_DIR}toughtables/wikidata/tables_subset/"
    python gemini_main.py ${API_KEY} wikidata ${CORPUS} ${RESULT_DIR}citysti/toughtables_wd/

    # Wikitables 2013 - Wikidata
    mkdir -p ${RESULT_DIR}citysti/wikitables_2013_wd/
    CORPUS="${BENCHMARK_DIR}wikitables_2013/tables_subset/"
    python gemini_main.py ${API_KEY} wikidata ${CORPUS} ${RESULT_DIR}citysti/wikitables_2013_wd/

    # Wikitables 2019 - Wikidata
    mkdir -p ${RESULT_DIR}citysti/wikitables_2019_wd/
    CORPUS="${BENCHMARK_DIR}wikitables_2019/tables_subset/"
    python gemini_main.py ${API_KEY} wikidata ${CORPUS} ${RESULT_DIR}citysti/wikitables_2019_wd/
fi
