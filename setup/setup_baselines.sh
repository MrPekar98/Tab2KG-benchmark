#!bin/bash

set -e

echo
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

echo
echo "Setting up T2K Match"

mkdir dbpedia-10-2016/
mkdir dbpedia-12-2022/
mkdir wikidata/

./kg/neo4j-dbpedia-10-2016/bin/neo4j start
sleep 1h
python3 t2kmatch_kg_gen.py tough_tables/dbpedia/ dbpedia-10-2016/ dbpedia
./kg/neo4j-dbpedia-10-2016/bin/neo4j stop
sleep 1m

./kg/neo4j-dbpedia-12-2022/bin/neo4j start
sleep 1h
python3 t2kmatch_kg_gen.py kg/dbpedia/ dbpedia-12-2022/ dbpedia
./kg/neo4j-dbpedia-12-2022/bin/neo4j stop
sleep 1m

./kg/neo4j-wikidata/bin/neo4j start
sleep 24h
python3 t2kmatch_kg_gen.py tough_tables/wikidata/ wikidata/ wikidata
./kg/neo4j-wikidata/bin/neo4j stop
sleep 1m

mv dbpedia-10-2016/ /baselines/t2kmatch/data
mv dbpedia-12-2022/ /baselines/t2kmatch/data
mv wikidata/ /baselines/t2kmatch/data

echo
echo "Setting up Magic"

mkdir -p /baselines/magic/dbpedia-10-2016
mkdir -p /baselines/magic/dbpedia-03-2022
wget https://sourceforge.net/projects/dbpedia-spotlight/files/2016-10/en/model/en.tar.gz/download -O dbp-10-2016.tar.gz
wget https://databus.dbpedia.org/dbpedia/spotlight/spotlight-model/2022.03.01/spotlight-model_lang=en.tar.gz -O dbp-03-2022.tar.gz
mv dbp-10-2016.tar.gz /baselines/magic
tar -xf /baselines/magic/dbp-10-2016.tar.gz
rm /baselines/magic/dbp-10-2016.tar.gz
mv /baselines/magic/en /baselines/magic/dbp-10-2016
mv dbp-03-2022.tar.gz /baselines/magic
tar -xf /baselines/magic/dbp-03-2022.tar.gz
rm /baselines/magic/dbp-03-2022.tar.gz
mv /baselines/magic/en /baselines/magic/dbp-03-2022
ttl-merge -i kg/dbpedia/*.ttl > dbp-12-2022.ttl
mv tough_tables/dbpedia/freebase_links_en.ttl tough_tables/
ttl-merge -i tough_tables/dbpedia/*.ttl > dbp-10-2016.ttl
mv tough_tables/freebase_links_en.ttl tough_tables/dbpedia/
git clone https://github.com/rdfhdt/hdt-cpp.git
docker build -t hdt -f hdt-cpp/Dockerfile hdt-cpp/
mkdir hdt-cpp/kg_data/
mv dbp-12-2022.ttl hdt-cpp/kg_data/
mv dbp-10-2016.ttl hdt-cpp/kg_data/
docker run --rm -v ${PWD}/hdt-cpp/:/workdir hdt cd workdir && rdf2hdt -f turtle kg_data/dbp-10-2016.ttl kg_data/dbp-10-2016.hdt
docker run --rm -v ${PWD}/hdt-cpp/:/workdir hdt cd workdir && rdf2hdt -f turtle kg_data/dbp-12-2022.ttl kg_data/dbp-12-2022.hdt
mv hdt-cpp/kg_data/*.hdt /baselines/magic
rm -rf hdt-cpp/
