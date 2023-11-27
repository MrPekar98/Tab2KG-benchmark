#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"

# Tough Tables
python3 bbwWrapper.py "${BENCHMARK_DIR}toughtables/wikidata/tables/" toughtables_wd

# SemTab HardTables
python3 bbwWrapper.py "${BENCHMARK_DIR}semtab/HardTables/tables/" semtab_hardtables

# SemTab BioDivTab
python3 bbwWrapper.py "${BENCHMARK_DIR}semtab/biodivtab/wikidata/tables/" semtab_biodivtab_wd

# Wikitables 2013
python3 bbwWrapper.py "${BENCHMARK_DIR}wikitables_2013/tables/" wikitables_2013

# Wikitables 2019
python3 bbwWrapper.py "${BENCHMARK_DIR}wikitables_2019/tables/" wikitables_2019
