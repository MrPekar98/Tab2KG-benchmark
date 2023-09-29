#!/bin/bash

set -e

echo "WikiTables"
mkdir -p /benchmarks/dbpedia/wikitables_2013/
mkdir -p /benchmarks/dbpedia/wikitables_2019/
mkdir -p /benchmarks/wikidata/wikitables_2013/
mkdir -p /benchmarks/wikidata/wikitables_2019/

./kg/neo4j-dbpedia/bin/neo4j start
sleep 5m
python3 wikitables/wikitables_dbpedia.py 13
python3 wikitables/wikitables_dbpedia.py 19
python3 wikitables/wikitables_wikidata.py 13
python3 wikitables/wikitables_wikidata.py 19
./kg/neo4j-dbpedia/bin/neo4j stop
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

./kg/neo4j-dbpedia/bin/neo4j start
sleep 5m
python3 aliases.py dbpedia
./kg/neo4j-dbpedia/bin/neo4j stop
sleep 1m
./kg/neo4j-wikidata/bin/neo4j start
sleep 15m
python3 aliases.py wikidata
sleep 1m
