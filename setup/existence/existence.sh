#!/bin/bash

set -e

export DBP_2016="/dbpedia_16/"
export DBP_2022="/dbpedia/"
export WD="/wikidata/"
export TOUGHTABLES_GT_DBP="/benchmarks/toughtables/dbpedia/gt/cea_gt.csv"
export TOUGHTABLES_GT_WD="/benchmarks/toughtables/wikidata/gt/cea_gt.csv"
export HARDTABLES_GT="/benchmarks/semtab/HardTables/gt/cea_gt.csv"
export TFOOD_GT="/benchmarks/semtab/tfood/horizontal/gt/cea_gt.csv"
export WIKITABLES_2013_DBP="/benchmarks/wikitables_2013/gt/dbpedia/gt.csv"
export WIKITABLES_2013_WD="/benchmarks/wikitables_2013/gt/wikidata/gt.csv"
export WIKITABLES_2019_DBP="/benchmarks/wikitables_2019/gt/dbpedia/gt.csv"
export WIKITABLES_2019_WD="/benchmarks/wikitables_2019/gt/wikidata/gt.csv"

export TT_DBP_ENTS_UNI=".toughtables_dbp_entities_unique.tmp"
export TT_WD_ENTS_UNI=".toughtables_wd_entities_unique.tmp"
export HT_ENTS_UNI=".hardtables_entities_unique.tmp"
export TF_ENTS_UNI=".tfood_entities_unique.tmp"
export WT_2013_DBP_ENTS_UNI=".wikitables_2013_dbp_entities_unique.tmp"
export WT_2013_WD_ENTS_UNI=".wikitables_2013_wd_entities_unique.tmp"
export WT_2019_DBP_ENTS_UNI=".wikitables_2019_dbp_entities_unique.tmp"
export WT_2019_WD_ENTS_UNI=".wikitables_2019_wd_entities_unique.tmp"

#docker network inspect kg-lookup-network >/dev/null 2>&1 || docker network create kg-lookup-network
#docker run --rm --name vos_existence -d \
#           --network kg-lookup-network \
#           -v ${PWD}/../../kg-lookup/database:/database \
#           -v ${PWD}/../../kg-lookup/import:/import \
#           -t -p 1111:1111 -p 8890:8890 -i openlink/virtuoso-opensource-7:7

#sleep 2m

echo "Checking for ground truth entity existence"
echo "Checking in the KG dump files..."
#./existence_kg.sh

echo
echo "Done"
echo "Checking in the Virtuoso instance..."
#./existence_virtuoso.sh

echo
echo "Done"
echo "Checking in the Lucene indexes in the KG lookup service"
./existence_lucene.sh

echo
echo "Complete"
#docker stop vos_existence
