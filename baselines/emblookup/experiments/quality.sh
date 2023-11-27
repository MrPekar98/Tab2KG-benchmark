#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
DATA_DIR="data/"

# SemTab HardTables
mkdir -p /results/emblookup/semtab_hardtables

python3 main.py "${BENCHMARK_DIR}semtab/HardTables/tables/" "${DATA_DIR}aliases/alias_wd.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_wd.csv" "${DATA_DIR}aliases_processed/aliases_processed_wd.csv" -h
mv runtimes.csv /results/emblookup/semtab_hardtables
mv results.csv /results/emblookup/semtab_hardtables

# SemTab BioDivTab - Dbpedia
mkdir -p /results/emblookup/semtab_biodivtab_dbp

python3 main.py "${BENCHMARK_DIR}semtab/biodivtab/dbpedia/tables/" "${DATA_DIR}aliases/alias_dbp12-2022.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_dbp12-2022.csv" "${DATA_DIR}aliases_processed/aliases_processed_dbp12-2022.csv" -h
mv runtimes.csv /results/emblookup/semtab_biodivtab_dbp
mv results.csv /results/emblookup/semtab_biodivtab_dbp

# SemTab BiodDivTab - Wikidata
mkdir -p /results/emblookup/semtab_biodivtab_wd

python3 main.py "${BENCHMARK_DIR}semtab/biodivtab/wikidata/tables/" "${DATA_DIR}aliases/alias_wd.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_wd.csv" "${DATA_DIR}aliases_processed/aliases_processed_wd.csv" -h
mv runtimes.csv /results/emblookup/semtab_biodivtab_wd
mv results.csv /results/emblookup/semtab_biodivtab_wd

# Tough Tables - DBpedia
mkdir -p /results/emblookup/toughtables_dbp

python3 main.py "${BENCHMARK_DIR}toughtables/dbpedia/tables/" "${DATA_DIR}aliases/alias_dbp10-2016.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_dbp10-2016.csv" "${DATA_DIR}aliases_processed/aliases_processed_dbp10-2016.csv" -h
mv runtimes.csv /results/emblookup/toughtables_dbp
mv results.csv /results/emblookup/toughtables_dbp

# Tough Tables - Wikidata
mkdir -p /results/emblookup/toughtables_wd

python3 main.py "${BENCHMARK_DIR}toughtables/wikidata/tables" "${DATA_DIR}aliases/alias_wd.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_wd.csv" "${DATA_DIR}aliases_processed/aliases_processed_wd.csv" -h
mv runtimes.csv /results/emblookup/toughtables_wd
mv results.csv /results/emblookup/toughtables_wd

# Wikitables 2013 - DBpedia
mkdir -p /results/emblookup/wikitables_2013_dbp

python3 main.py "${BENCHMARK_DIR}wikitables_2013/tables/" "${DATA_DIR}aliases/alias_dbp12-2022.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_dbp12-2022.csv" "${DATA_DIR}aliases_processed/aliases_processed_dbp12-2022.csv" -h
mv runtimes.csv /results/emblookup/wikitables_2013-dbp/
mv results.csv /results/emblookup/wikitables_2013-dbp/

# Wikitables 2013 - Wikidata
mkdir -p /results/emblookup/wikitables_2013_wd

python3 main.py "${BENCHMARK_DIR}wikitables_2013/tables/" "${DATA_DIR}aliases/alias_wd.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_wd.csv" "${DATA_DIR}aliases_processed/aliases_processed_wd.csv" -h
mv runtimes.csv /results/emblookup/wikitables_2013_wd
mv results.csv /results/emblookup/wikitables_2013_wd

# Wikitables 2019 - DBpedia
mkdir -p /results/emblookup/wikitables_2019_dbp

python3 main.py "${BENCHMARK_DIR}wikitables_2019/tables/" "${DATA_DIR}aliases/alias_dbp12-2022.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_dbp12-2022.csv" "${DATA_DIR}aliases_processed/aliases_processed_dbp12-2022.csv" -h
mv runtimes.csv /results/emblookup/wikitables_2019_dbp
mv results.csv /results/emblookup/wikitables_2019_dbp

# Wikitables 2019 - Wikidata
mkdir -p /results/emblookup/wikitables_2019_wd

python3 main.py "${BENCHMARK_DIR}wikitables_2019/tables/" "${DATA_DIR}aliases/alias_wd.ttl" "${DATA_DIR}index_mappings/kg_index_name_mapping_wd.csv" "${DATA_DIR}aliases_processed/aliases_processed_wd.csv" -h
mv runtimes.csv /results/emblookup/wikitables_2019_wd
mv results.csv /results/emblookup/wikitables_2019_wd
