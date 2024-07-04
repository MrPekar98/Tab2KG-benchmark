#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"

# SemTab HardTables
CORPUS="${BENCHMARK_DIR}semtab/HardTables/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    python main.py ${CORPUS} /results/bbw/semtab_hardtables/ ${ENDPOINT} ${VIRTUOSO}
fi

# tFood
CORPUS="${BENCHMARK_DIR}semtab/tfood/horizontal/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    python main.py ${CORPUS} /results/bbw/tfood/ ${ENDPOINT} ${VIRTUOSO}
fi

# Tough Tables
CORPUS="${BENCHMARK_DIR}toughtables/wikidata/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    python main.py ${CORPUS} /results/bbw/toughtables_wd/ ${ENDPOINT} ${VIRTUOSO}
fi

# Wikitables 2013
CORPUS="${BENCHMARK_DIR}wikitables_2013/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    python main.py ${CORPUS} /results/bbw/wikitables_2013/ ${ENDPOINT} ${VIRTUOSO}
fi

# Wikitables 2019
CORPUS="${BENCHMARK_DIR}wikitables_2019/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    python main.py ${CORPUS} /results/bbw/wikitables_2019/ ${ENDPOINT} ${VIRTUOSO}
fi
