#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/"
KG=$1	# TODO: Pass this as argument to main.py

# SemTab HardTables

if [[ "${KG}" = "wd" ]]
then
    mkdir -p ${RESULT_DIR}magic/HardTables/
    python3 main.py wikidata ${KG}.hdt ${BENCHMARK_DIR}semtab/HardTables/tables/ ${RESULT_DIR}magic/HardTables/
fi

# tFood

if [[ "${KG}" = "wd" ]]
then
    mkdir -p ${RESULT_DIR}magic/tfood/
    python3 main.py wikidata ${KG}.hdt ${BENCHMARK_DIR}semtab/tfood/horizontal/tables/ ${RESULT_DIR}magic/tfood/
fi

# Tough Tables - DBpedia

if [[ "${KG}" = "dbp-10-2016" ]]
then
    mkdir -p ${RESULT_DIR}magic/tough_tables_dbp/
    python3 main.py dbpedia ${KG}.hdt ${BENCHMARK_DIR}toughtables/dbpedia/tables/ ${RESULT_DIR}magic/tough_tables_dbp/
fi

# Tough Tables - Wikidata

if [[ "${KG}" = "wd" ]]
then
    mkdir -p ${RESULT_DIR}magic/tough_tables_wd/
    python3 main.py wikidata ${KG}.hdt ${BENCHMARK_DIR}toughtables/wikidata/tables/ ${RESULT_DIR}magic/tough_tables_wd/
fi

# Wikitables 2013 - DBpedia

if [[ "${KG}" = "dbp-12-2022" ]]
then
    mkdir -p ${RESULT_DIR}magic/wikitables-2013_dbp/
    python3 main.py dbpedia ${KG}.hdt ${BENCHMARK_DIR}wikitables_2013/tables_subset/ ${RESULT_DIR}magic/wikitables-2013_dbp/
fi

# Wikitables 2013 - Wikidata

if [[ "${KG}" = "wd" ]]
then
    mkdir -p ${RESULT_DIR}magic/wikitables-2013_wd/
    python3 main.py wikidata ${KG}.hdt ${BENCHMARK_DIR}wikitables_2013/tables_subset/ ${RESULT_DIR}magic/wikitables_2013_wd/
fi

# Wikitables 2019 - DBpedia

if [[ "${KG}" = "dbp-12-2022" ]]
then
    mkdir -p ${RESULT_DIR}magic/wikitables-2019_dbp/
    python3 main.py dbpedia ${KG}.hdt ${BENCHMARK_DIR}/wikitables_2019/tables_subset/ ${RESULT_DIR}magic/wikitables-2019_dbp/
fi

# Wikitables 2019 - Wikidata
if [[ "${KG}" = "wd" ]]
then
    mkdir -p ${RESULT_DIR}magic/wikitables-2019_wd/
    python3 main.py wikidata ${KG}.hdt ${BENCHMARK_DIR}/wikitables_2019/tables_subset/ ${RESULT_DIR}magic/wikitables-2019_wd/
fi
