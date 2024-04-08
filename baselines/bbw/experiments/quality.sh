#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"

# SemTab HardTables
python bbwWrapper.py "${BENCHMARK_DIR}semtab/HardTables/tables_subset//" semtab_hardtables

# tFood
python bbwWrapper.py "${BENCHMARK_DIR}semtab/tfood/horizontal/tables_subset/" tfood

# Tough Tables
python bbwWrapper.py "${BENCHMARK_DIR}toughtables/wikidata/tables_subset/" toughtables_wd

# Wikitables 2013
python bbwWrapper.py "${BENCHMARK_DIR}wikitables_2013/tables_subset/" wikitables_2013

# Wikitables 2019
python bbwWrapper.py "${BENCHMARK_DIR}wikitables_2019/tables_subset/" wikitables_2019
