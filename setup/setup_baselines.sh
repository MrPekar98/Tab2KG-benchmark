#!bin/bash

set -e

echo "Setting up EmbLookup"
git clone https://github.com/MrPekar98/EmbLookup.git
mv EmbLookup/preprocess.py .
mv EmbLookup/utils.py .
mv EmbLookup/embedding_learner.py .
mv EmbLookup/gen_alias_list.py .
mkdir -p /baselines/emblookup/data/aliases
mkdir -p /baselines/emblookup/data/aliases_processed
mkdir -p /baselines/emblookup/data/index_mappings

python3 gen_alias_list.py 'dbpedia' tough_tables/dbpedia/labels_en.ttl /baselines/emblookup/data/aliases/alias_dbp10-2016.ttl
python3 gen_alias_list.py 'dbpedia' kg/dbpedia/labels_lang=en.ttl /baselines/emblookup/data/aliases/alias_dbp12-2022.ttl
python3 gen_alias_list.py 'wikidata' tough_tables/wikidata/ /baselines/emblookup/data/aliases/alias_wd.ttl
python3 preprocess.py /baselines/emblookup/data/aliases/alias_dbp10-2016.ttl /baselines/emblookup/data/aliases_processed/aliases_processed_dbp10-2016.csv /baselines/emblookup/data/index_mappings/kg_index_name_mapping_dbp10-2016.csv
python3 preprocess.py /baselines/emblookup/data/aliases/alias_dbp12-2022.ttl /baselines/emblookup/data/aliases_processed/aliases_processed_dbp12-2022.csv /baselines/emblookup/data/index_mappings/kg_index_name_mapping_dbp12-2022.csv
python3 preprocess.py /baselines/emblookup/data/aliases/alias_wd.ttl /baselines/emblookup/data/aliases_processed/aliases_processed_wd.csv /baselines/emblookup/data/index_mappings/kg_index_name_mapping_wd.csv

rm -rf EmbLookup gen_alias_list.py embedding_learner.py utils.py preprocess.py
