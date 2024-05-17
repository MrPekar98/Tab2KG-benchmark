#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/"

# SemTab HardTables
CORPUS="${BENCHMARK_DIR}semtab/HardTables/tables_subset/"

if [[ "${KG}" = "wd" && -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}magic/HardTables/
    python3 main.py wikidata /hdt/${KG}.hdt ${CORPUS} ${RESULT_DIR}magic/HardTables/ ${ENDPOINT}
fi

# tFood
CORPUS="${BENCHMARK_DIR}semtab/tfood/horizontal/tables_subset/"

if [[ "${KG}" = "wd" && -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}magic/tfood/
    python3 main.py wikidata /hdt/${KG}.hdt ${CORPUS} ${RESULT_DIR}magic/tfood/ ${ENDPOINT}
fi

# Tough Tables - DBpedia
CORPUS="${BENCHMARK_DIR}toughtables/dbpedia/tables_subset/"

if [[ "${KG}" = "dbp-10-2016" && -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}magic/tough_tables_dbp/
    python3 main.py dbpedia /hdt/${KG}.hdt ${CORPUS} ${RESULT_DIR}magic/tough_tables_dbp/ ${ENDPOINT}
fi

# Tough Tables - Wikidata
CORPUS="${BENCHMARK_DIR}toughtables/wikidata/tables_subset/"

if [[ "${KG}" = "wd" && -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}magic/tough_tables_wd/
    python3 main.py wikidata /hdt/${KG}.hdt ${CORPUS} ${RESULT_DIR}magic/tough_tables_wd/ ${ENDPOINT}
fi

# Wikitables 2013 - DBpedia
CORPUS="${BENCHMARK_DIR}wikitables_2013/tables_subset/"

if [[ "${KG}" = "dbp-12-2022" && -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}magic/wikitables-2013_dbp/
    python3 main.py dbpedia /hdt/${KG}.hdt ${CORPUS} ${RESULT_DIR}magic/wikitables-2013_dbp/ ${ENDPOINT}
fi

# Wikitables 2013 - Wikidata
CORPUS="${BENCHMARK_DIR}wikitables_2013/tables_subset/"

if [[ "${KG}" = "wd" && -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}magic/wikitables-2013_wd/
    python3 main.py wikidata /hdt/${KG}.hdt ${CORPUS} ${RESULT_DIR}magic/wikitables-2013_wd/ ${ENDPOINT}
fi

# Wikitables 2019 - DBpedia
CORPUS="${BENCHMARK_DIR}/wikitables_2019/tables_subset/"

if [[ "${KG}" = "dbp-12-2022" && -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}magic/wikitables-2019_dbp/
    python3 main.py dbpedia /hdt/${KG}.hdt ${CORPUS} ${RESULT_DIR}magic/wikitables-2019_dbp/ ${ENDPOINT}
fi

# Wikitables 2019 - Wikidata
CORPUS="${BENCHMARK_DIR}/wikitables_2019/tables_subset/"

if [[ "${KG}" = "wd" && -d ${CORPUS} ]]
then
    mkdir -p ${RESULT_DIR}magic/wikitables-2019_wd/
    python3 main.py wikidata /hdt/${KG}.hdt ${CORPUS} ${RESULT_DIR}magic/wikitables-2019_wd/ ${ENDPOINT}
fi
