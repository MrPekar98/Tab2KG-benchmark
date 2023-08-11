#!/bin/bash

set -e

cd kg/

echo "Downloading DBpedia"
./download_files.sh dbpedia_files.txt
mv files dbpedia

echo "Downloading Wikidata"
./download_files.sh wikidata_files.txt
mv files wikidata

echo "Installing Neo4J"
./install.sh
mkdir tmp
mv neo4j-server tmp
cp -r tmp/neo4j-server .
mv neo4j-server neo4j-dbpedia
cp -r tmp/neo4j-server .
mv neo4j-server neo4j-wikidata
rm -rf tmp

echo "Importing DBpedia"
./neo4j-dbpedia/bin/neo4j start
sleep 30s
./import.sh dbpedia neo4j-dbpedia
./neo4j-dbpdedia/bin/neo4j stop
sleep 30s

echo "Importing Wikidata"
./neo4j-wikidata/bin/neo4j start
sleep 30s
./import.sh wikidata neo4j-wikidata
./neo4j-wikidata/bin/neo4j stop
sleep 30s

cd ..
echo "Setting up benchmark"
echo

mkdir /benchmarks/dbpedia
mkdir /benchmarks/wikidata

echo "Setting up WikiTables"
mkdir /benchmarks/dbpedia/wikitables
mkdir /benchmarks/wikidata/wikitables

echo "Done"
