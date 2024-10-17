#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/"

if [[ "${KG}" = "wd" ]]
then
    # Tough Tables - Wikidata
    mkdir -p ${RESULT_DIR}lexma/toughtables_wd_non_rec/
    CORPUS="${BENCHMARK_DIR}toughtables/wikidata/tables_subset/"
    CELLS="${BENCHMARK_DIR}toughtables/wikidata/gt/entity_cells.txt"

    python lexma_non_rec.py wikidata ${CORPUS} ${RESULT_DIR}lexma/toughtables_wd_non_rec/ 10 "http://${ENDPOINT}:7000/" ${CELLS}

    # Wikitables 2019 - Wikidata
    mkdir -p ${RESULT_DIR}lexma/wikitables_2019_wd_non_rec/
    CORPUS="${BENCHMARK_DIR}wikitables_2019/tables_subset/"
    CELLS="${BENCHMARK_DIR}wikitables_2019/gt/wikidata/entity_cells.txt"

    python lexma_non_rec.py wikidata ${CORPUS} ${RESULT_DIR}lexma/wikitables_2019_wd_non_rec/ 10 "http://${ENDPOINT}:7000/" ${CELLS}
fi
