#!/bin/bash

set -e

BENCHMARK_DIR="/benchmarks/"
RESULT_DIR="/results/keyword-kg-linker/"

cd ..
docker start neo4j_wd
sleep 2m

# SemTab HardTables
mkdir -p ${RESULT_DIR}/HardTables/keyword/ ${RESULT_DIR}/HardTables/embedding/

for TABLE in ${BENCHMARK_DIR}/semtab/HardTables/tables_subset/* ;\
do
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/HardTables/keyword/ -dir wd/ -config config.json -type keyword
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/HardTables/embedding/ -dir wd/ -config config.json -type embedding
done

# tFood
mkdir -p ${RESULT_DIR}/tfood/keyword/ ${RESULT_DIR}/tfood/embedding/

for TABLE in ${BENCHMARK_DIR}/semtab/tfood/horizontal/test/tables_subset/ ;\
do
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/tfood/keyword/ -dir wd/ -config config.json -type keyword
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/tfood/embedding/ -dir wd/ -config config.json -type embedding
done

# Tough Tables - Wikidata
mkdir -p ${RESULT_DIR}/toughtables_wd/keyword/ ${RESULT_DIR}/toughtables_wd/embedding/

for TABLE in ${BENCHMARK_DIR}/toughtables/wikidata/tables_subset/ ;\
do
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/toughtables_wd/keyword/ -dir wd/ -config config.json -type keyword
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/toughtables_wd/embedding/ -dir wd/ -config config.json -type embedding
done

# Wikitables 2013 - Wikidata
mkdir -p ${RESULT_DIR}/wikitables_2013_wd/keyword/ ${RESULT_DIR}/wikitables_2013_wd/embedding/

for TABLE in ${BENCHMARK_DIR}/wikitables_2013/tables_subset/ ;\
do
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/wikitables_2013_wd/keyword/ -dir wd/ -config config.json -type keyword
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/wikitables_2013_wd/embedding/ -dir wd/ -config config.json -type embedding
done

# Wikitables 2019 - Wikidata
mkdir -p ${RESULT_DIR}/wikitables_2019_wd/keyword/ ${RESULT_DIR}/wikitables_2019_wd/embedding/

for TABLE in ${BENCHMARK_DIR}/wikitables_2019/tables_subset/ ;\
do
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/wikitables_2019_wd/keyword/ -dir wd/ -config config.json -type keyword
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/wikitables_2019_wd/embedding/ -dir wd/ -config config.json -type embedding
done

docker stop neo4j_wd
sleep 1m
docker start neo4j_dbp16
sleep 2m

# Tough Tables - DBpedia
mkdir -p ${RESULT_DIR}/toughtables_dbp/keyword/ ${RESULT_DIR}/toughtables_dbp/embedding/

for TABLE in ${BENCHMARK_DIR}/toughtables/dbpedia/tables_subset/ ;\
do
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/toughtables_dbp/keyword/ -dir dbp_16/ -config config.json -type keyword
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/toughtables_dbp/embedding/ -dir dbp_16/ -config config.json -type embedding
done

docker stop neo4j_dbp16
sleep 1m
docker start neo4j_dbp22
sleep 2m

# Wikitables 2013 - DBpedia
mkdir -p ${RESULTS_DIR}/wikitables_2013_dbp/keyword/ ${RESULTS_DIR}/wikitables_2013_dbp/embedding/

for TABLE in ${BENCHMARK_DIR}/wikitables_2013/tables_subset/ ;\
do
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/wikitables_2013_dbp/keyword/ -dir dbp_22/ -config config.json -type keyword
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/wikitables_2013_dbp/embedding/ -dir dbp_22/ -config config.json -type embedding
done

# Wikitables 2019 - DBpedia
mkdir -p ${RESULT_DIR}/wikitables_2019_dbp/keyword/ ${RESULT_DIR}/wikitables_2019_dbp/embedding/

for TABLE in ${BENCHMARK_DIR}/wikitables_2013/tables_subset/ ;\
do
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/wikitables_2019_dbp/keyword/ -dir dbp_22/ -config config.json -type keyword
    ./linker.sh -table ${TABLE} -output ${RESULT_DIR}/wikitables_2019_dbp/embedding/ -dir dbp_22/ -config config.json -type embedding
done

docker stop neo4j_dbp22
sleep 1m
cd experiments/
