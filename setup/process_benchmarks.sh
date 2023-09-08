#!/bin/bash

set -e

echo "WikiTables"
mkdir -p /benchmarks/dbpedia/wikitables/
mkdir -p /benchmarks/dbpedia/wikitables/

./kg/neo4j-dbpedia/bin/neo4j start
sleep 20m
python3 wikitables/wikitables_dbpedia.py
python3 wikitables/wikitables_wikidata.py
./kg/neo4j-wikidata/bin/neo4j stop
sleep 1m

echo
echo "SemTab 2023"
mkdir -p /benchmarks/dbpedia/semtab/
mkdir -p /benchmarks/wikidata/semtab/

python3 semtab/semtab_dbpedia.py
python3 semtab/semtab_wikidata.py

echo
echo "Tough Tables"
mkdir -p /benchmarks/dbpedia/tough_tables/
mkdir -p /benchmarks/wikidata/tough_tables/

python3 tough_tables/tough_tables_dbpedia.py
python3 tough_tables/tough_tables_wikidata.py

echo
echo "WebCommons"
mkdir -p /benchmarks/dbpedia/webcommons/
mkdir -p /benchmarks/wikidata/webcommons/

python3 webcommons/webcommons_dbpedia.py
python3 webcommons/webcommons_wikidata.py
