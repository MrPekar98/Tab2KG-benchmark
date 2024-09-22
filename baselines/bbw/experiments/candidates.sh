#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/"

mkdir -p ${RESULT_DIR}bbw/toughtables_candidates/
CORPUS="${BENCHMARK_DIR}toughtables/wikidata/tables_subset/"
python candidates_main.py ${CORPUS} ${RESULT_DIR}bbw/toughtables_candidates/ ${ENDPOINT} ${VIRTUOSO}

mkdir -p ${RESULT_DIR}bbw/wikitables_2013_candidates/
CORPUS="${BENCHMARK_DIR}wikitables_2013/tables_subset/"
python candidates_main.py ${CORPUS} ${RESULT_DIR}bbw/wikitables_2013_candidates/ ${ENDPOINT} ${VIRTUOSO}

mkdir -p ${RESULT_DIR}bbw/wikitables_2019_candidates/
CORPUS="${BENCHMARK_DIR}wikitables_2019/tables_subset/"
python candidates_main.py ${CORPUS} ${RESULT_DIR}bbw/wikitables_2019_candidates/ ${ENDPOINT} ${VIRTUOSO}
