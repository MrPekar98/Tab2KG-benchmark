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

export DBP_2016_ENTS_UNI=".dbpedia_2016_entities_unique.tmp"
export DBP_2022_ENTS_UNI=".dbpedia_2022_entities_unique.tmp"
export WD_ENTS_UNI=".wikidata_entities_unique.tmp"
export TT_DBP_ENTS_UNI=".toughtables_dbp_entities_unique.tmp"
export TT_WD_ENTS_UNI=".toughtables_wd_entities_unique.tmp"
export HT_ENTS_UNI=".hardtables_entities_unique.tmp"
export TF_ENTS_UNI=".tfood_entities_unique.tmp"
export WT_2013_DBP_ENTS_UNI=".wikitables_2013_dbp_entities_unique.tmp"
export WT_2013_WD_ENTS_UNI=".wikitables_2013_wd_entities_unique.tmp"
export WT_2019_DBP_ENTS_UNI=".wikitables_2019_dbp_entities_unique.tmp"
export WT_2019_WD_ENTS_UNI=".wikitables_2019_wd_entities_unique.tmp"

export VIRTUOSO_URL=$(docker exec vos_existence bash -c 'hostname -I')

echo "Checking for ground truth entity existence"
echo "Checking in the KG dump files..."
./existence_kg.sh

echo
echo "Done"
echo "Checking in the Virtuoso instance..."
./existence_virtuoso.sh

echo
echo "Done"
echo "Checking in the Lucene indexes in the KG lookup service"
./existence_lucene.sh

echo
echo "Filtering ground truth files from non-existent entities"
./filter_gt_entities.sh

echo
echo "Complete"
docker stop vos_existence
