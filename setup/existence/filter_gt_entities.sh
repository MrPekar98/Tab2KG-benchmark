#!/bin/bash

set -e

# HardTables
echo "Filtering HardTables ground truth..."
./filter_gt_file.sh .hardtables_entities_unique.tmp .wikidata_entities_unique.tmp

#tFood
echo "Filtering tFood ground truth..."
./filter_gt_file.sh .tfood_entities_unique.tmp .wikidata_entities_unique.tmp

# ToughTables - DBpedia
echo "Filtering ToughTables - DBpedia ground truth..."
./filter_gt_file.sh .toughtables_dbp_entities_unique.tmp .dbpedia_2016_entities_unique.tmp

# ToughTables - Wikidata
echo "Filtering ToughTables - Wikidata ground truth..."
./filter_gt_file.sh .toughtables_wd_entities_unique.tmp .wikidata_entities_unique.tmp

# Wikitables 2013 - DBpedia
echo "Filtering Wikitables 2013 - DBpedia ground truth..."
./filter_gt_file.sh .wikitables_2013_dbp_entities_unique.tmp .dbpedia_2022_entities_unique.tmp

# Wikitables 2013 - Wikidata
echo "Filtering Wikitables 2013 - Wikidata ground truth..."
./filter_gt_file.sh .wikitables_2013_wd_entities_unique.tmp .wikidata_entities_unique.tmp

# Wikitables 2019 - DBpedia
echo "Filtering Wikitables 2019 - DBpedia ground truth..."
./filter_gt_file.sh .wikitables_2019_dbp_entities_unique.tmp .dbpedia_2022_entities_unique.tmp

# Wikitables 2019 - Wikdiata
echo "Filtering Wikitables 2019 - Wikidata ground truth..."
./filter_gt_file.sh .wikitables_2019_wd_entities_unique.tmp .wikidata_entities_unique.tmp

echo "Filtering done"
