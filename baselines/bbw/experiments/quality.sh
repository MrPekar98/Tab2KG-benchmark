#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"

# SemTab HardTables
CORPUS="${BENCHMARK_DIR}semtab/HardTables/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    python bbwWrapper.py ${CORPUS} semtab_hardtables
fi

# tFood
CORPUS="${BENCHMARK_DIR}semtab/tfood/horizontal/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    python bbwWrapper.py ${CORPUS} tfood
fi

# Tough Tables
CORPUS="${BENCHMARK_DIR}toughtables/wikidata/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    python bbwWrapper.py ${CORPUS} toughtables_wd
fi

# Wikitables 2013
CORPUS="${BENCHMARK_DIR}wikitables_2013/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    python bbwWrapper.py ${CORPUS} wikitables_2013
fi

# Wikitables 2019
CORPUS="${BENCHMARK_DIR}wikitables_2019/tables_subset/"

if [[ -d ${CORPUS} ]]
then
    python bbwWrapper.py ${CORPUS} wikitables_2019
fi
