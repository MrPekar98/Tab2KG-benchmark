#!/bin/bash

set -e

#echo "Downloading DBpedia"
#mkdir -p kg/dbpedia/
#./kg/download-files.sh kg/dbpedia_files.txt
#mv files/* kg/dbpedia
#rmdir files

#echo
#echo "Installing Neo4J"
#./kg/install.sh
#mkdir tmp
#mv neo4j-server tmp
#cp -r tmp/neo4j-server .
#mv neo4j-server kg/neo4j-dbpedia
#cp -r tmp/neo4j-server .
#mv neo4j-server kg/neo4j-wikidata
#rm -rf tmp

#echo "dbms.memory.heap.initial_size=50g" >> kg/neo4j-dbpedia/conf/neo4j.conf
#echo "dbms.memory.heap.max_size=150g" >> kg/neo4j-dbpedia/conf/neo4j.conf
#echo "dbms.memory.heap.initial_size=50g" >> kg/neo4j-wikidata/conf/neo4j.conf
#echo "dbms.memory.heap.max_size=150g" >> kg/neo4j-wikidata/conf/neo4j.conf

echo
echo "Setting up benchmark"
echo
echo "Downloading benchmarks"
./download_benchmarks.sh

echo
echo "Processing benchmarks"
#./process_benchmarks.sh

echo
echo "Done"
