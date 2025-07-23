#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/"

if [[ "${KG}" = "wd" ]]
then
    # Tough Tables - Wikidata
    #mkdir -p ${RESULT_DIR}citysti/toughtables_wd_candidates/
    #CORPUS="${BENCHMARK_DIR}toughtables/wikidata/tables_subset/"
    #python gemini_candidates.py ${API_KEY} wikidata ${CORPUS} ${RESULT_DIR}citysti/toughtables_wd_candidates/ ${ENDPOINT}

    # HardTables
    #mkdir -p ${RESULT_DIR}citysti/hardtables_candidates/
    #CORPUS="${BENCHMARK_DIR}semtab/HardTables/tables_subset/"
    #python gemini_candidates.py ${API_KEY} wikidata ${CORPUS} ${RESULT_DIR}citysti/hardtables_candidates/ ${ENDPOINT}

    # Wikitables 2019 - Wikidata
    mkdir -p ${RESULT_DIR}citysti/wikitables_2019_wd_candidates/
    CORPUS="${BENCHMARK_DIR}wikitables_2019/tables_subset/"
    python gemini_candidates.py ${API_KEY} wikidata ${CORPUS} ${RESULT_DIR}citysti/wikitables_2019_wd_candidates/ ${ENDPOINT}
fi
