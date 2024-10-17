#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/"

if [[ "${KG}" = "wd" ]]
then
    # Tough Tables - Wikidata
    CORPUS="${BENCHMARK_DIR}toughtables/wikidata/tables_subset/"
    CELLS="${BENCHMARK_DIR}toughtables/wikidata/gt/entity_cells.txt"

    mkdir -p ${RESULT_DIR}magic/tough_tables_wd_non_rec/
    python3 main_non_rec.py wikidata /hdt/${KG}.hdt ${CORPUS} ${RESULT_DIR}magic/tough_tables_wd_non_rec/ ${ENDPOINT} ${CELLS}

    # Wikitables 2019 - Wikidata
    CORPUS="${BENCHMARK_DIR}/wikitables_2019/tables_subset/"
    CELLS="${BENCHMARK_DIR}wikitables_2019/gt/wikidata/entity_cells.txt"

    mkdir -p ${RESULT_DIR}magic/wikitables-2019_wd_non_rec/
    python3 main_non_rec.py wikidata /hdt/${KG}.hdt ${CORPUS} ${RESULT_DIR}magic/wikitables-2019_wd_non_rec/ ${ENDPOINT} ${CELLS}
fi
