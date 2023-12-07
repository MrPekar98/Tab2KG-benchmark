#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"

# Tough Tables
python3 bbwWrapper.py "${BENCHMARK_DIR}toughtables/wikidata/tables/" toughtables_wd

# SemTab HardTables
python3 bbwWrapper.py "${BENCHMARK_DIR}semtab/HardTables/tables/" semtab_hardtables

# Wikitables 2013
python3 bbwWrapper.py "${BENCHMARK_DIR}wikitables_2013/tables_subset/" wikitables_2013

# Wikitables 2019
python3 bbwWrapper.py "${BENCHMARK_DIR}wikitables_2019/tables_subset/" wikitables_2019
